# BFT inscription convention (draft)

DRAFT. Not inscribed. Inscribing costs sats and is the Admiral's call.

## What gets inscribed

`js/bft.js`, one 276-byte pure function, as a JavaScript inscription (content type `text/javascript`):

```js
const bft=h=>{...};   // the exact file, see js/bft.js
```

It takes a height, returns `YYYY.MM.DD HH:MM a₿`, and throws on anything that is not a non-negative safe integer. It reads no clock and calls no network. It passes all 42 forward vectors, the 8 inverse and the 9 invalid inputs (`js/bft.test.mjs`).

## How another inscription uses it

The page gets the height from the ordinals recursive endpoint and passes it in:

```html
<script type="module">
  const h = Number(await (await fetch("/r/blockheight")).text());
  const src = await (await fetch("/content/<BFT_INSCRIPTION_ID>")).text();
  const bft = new Function(src + ";return bft")();
  document.body.textContent = bft(h);
</script>
```

`/r/blockheight` and `/content/<id>` are documented recursive endpoints (https://docs.ordinals.com/inscriptions/recursion.html). Verify them on the target `ord` version before inscribing.

## Rules of the convention

1. The function is never modified. A change is a new inscription and a new spec version.
2. The inscription id is recorded in this repository (`spec/README.md`) once it exists, with the date and the spec version.
3. A page without a real height shows the dash face, not a guess.
4. Anything else (sky, anchors, ladder) stays outside the inscription.
