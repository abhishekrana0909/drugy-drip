# Drugy Drip website

Static website for "Drugy Drip", a baggy streetwear clothing brand. Owner/user: Abhishek Rana. Theme: black + leaf green, layout modelled on a streetwear template the user shared (bold black-box headings, grunge hero, product grid). Built the same way as the user's `ranapaint` project.

- The `.html` files are GENERATED. Edit `tools/site-builder/*.py` (products in `products.py`, contact details in `config.py`, header/footer/card in `layout.py`), then run `python tools/site-builder/build.py`. Hand edits to `.html` get overwritten.
- `css/style.css`, `js/main.js`, `js/cart.js` are edited directly; bump `ASSET_VERSION` in `config.py` after changing them.
- Cart: product cards have size/colour selects + Add to cart (`js/cart.js`, localStorage). The cart sends the order with prices to WhatsApp.
- Prices are in USD, one per category in `products.py`: tees 29.99, lowers 39.99, hoodies 79.99 (user's numbers). Jackets 79.99 and accessories 24.99 are my guesses. Contact details in `config.py` are DEMO values (+1 555 number, @drugydrip, hello@drugydrip.com).
- All clothing photos are cropped from the user's mockup sheets (`images/source/`) by `tools/crop_mockups.py` into `images/products/` and `images/stock/`. Only `images/stock/concrete.webp` (hero background) is from Unsplash.
- Header shows the logo big (hangs below the header bar) with the brand name "DRUGY DRIP" next to it, as the user asked.
- The user asked NOT to add a "40% off" offer section.
- Logo in use: the user's own `images/logo/source/druggy-drip-original.jpg` (it says "DRUGGY" with two Gs; brand name is "Drugy" with one G, user will fix the logo later). Earlier generated logo options live in `images/logo/` and `tools/logo/`.
- Preview: `python -m http.server 5501`, then open http://localhost:5501.
- Repo: https://github.com/abhishekrana0909/drugy-drip (public, `main`). Live (GitHub Pages, main/root): https://abhishekrana0909.github.io/drugy-drip/. Deploy = commit + `git push`. Commits use the GitHub noreply email (the account blocks pushes that expose the private email).

The user talks in Hinglish and is learning Python. Explain steps simply in Hinglish. When giving requirements they like to send all details first and say "START" before anything is built.
