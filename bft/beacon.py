"""
bft.beacon -- read "now" the house way: our beacon first, mempool.space to verify, else nothing.

    tip()  ->  {"height": N or None, "source": "beacon"|"mempool"|None,
                "beacon": N or None, "mempool": N or None, "gap": int or None, "note": str}

No height means dashes downstream, never a guess (the dashes-over-estimates law). The core
never calls this; it is the one network door and lives apart so the core stays pure.
`fetch(url) -> int|None` is injectable for tests.
"""

from __future__ import annotations

import json
import urllib.request
from typing import Any, Callable, Dict, Optional

BEACON_URL = "https://time.pacsarcade.org/height"
MEMPOOL_URL = "https://mempool.space/api/blocks/tip/height"


def _fetch(url: str, timeout: float = 8.0) -> Optional[int]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "bitcoin-federated-time"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read().decode("utf-8").strip()
        n = json.loads(body)
        if isinstance(n, dict):
            n = n.get("height")
        n = int(n) if isinstance(n, (int, str)) and not isinstance(n, bool) else None
        return n if n is not None and n >= 0 else None
    except Exception:
        return None


def tip(fetch: Optional[Callable[[str], Optional[int]]] = None) -> Dict[str, Any]:
    f = fetch or _fetch
    beacon, pub = f(BEACON_URL), f(MEMPOOL_URL)
    gap = abs(beacon - pub) if beacon is not None and pub is not None else None
    if beacon is not None:
        height, source = beacon, "beacon"
        note = "" if gap is None else ("beacon and mempool agree" if gap <= 1
                                        else "GAP of %d blocks: our node may be behind" % gap)
        if gap is None:
            note = "beacon only (mempool unreachable)"
    elif pub is not None:
        height, source, note = pub, "mempool", "beacon unreachable: public height stands in"
    else:
        height, source, note = None, None, "no source reachable: dashes"
    return {"height": height, "source": source, "beacon": beacon, "mempool": pub,
            "gap": gap, "note": note}
