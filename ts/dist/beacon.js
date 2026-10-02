// bft beacon: read "now" the house way. Our beacon first, mempool.space to verify, else nothing.
// No height means dashes downstream, never a guess. The core never calls this: it is the one network door.

export const BEACON_URL = "https://time.pacsarcade.org/height";
export const MEMPOOL_URL = "https://mempool.space/api/blocks/tip/height";

                                                              

                      
                        
                                      
                        
                         
                     
               
 

export const defaultFetch          = async (url) => {
  try {
    const r = await fetch(url, { cache: "no-store", signal: AbortSignal.timeout(8000) });
    if (!r.ok) return null;
    const body = JSON.parse((await r.text()).trim());
    const n = typeof body === "object" && body !== null ? body.height : body;
    return Number.isSafeInteger(n) && n >= 0 ? n : null;
  } catch {
    return null;
  }
};

export async function tip(fetcher          = defaultFetch)               {
  const [beacon, mempool] = await Promise.all([fetcher(BEACON_URL), fetcher(MEMPOOL_URL)]);
  const gap = beacon !== null && mempool !== null ? Math.abs(beacon - mempool) : null;
  if (beacon !== null) {
    const note = gap === null ? "beacon only (mempool unreachable)"
      : gap <= 1 ? "beacon and mempool agree" : "GAP of " + gap + " blocks: our node may be behind";
    return { height: beacon, source: "beacon", beacon, mempool, gap, note };
  }
  if (mempool !== null) return { height: mempool, source: "mempool", beacon, mempool, gap, note: "beacon unreachable: public height stands in" };
  return { height: null, source: null, beacon, mempool, gap, note: "no source reachable: dashes" };
}
