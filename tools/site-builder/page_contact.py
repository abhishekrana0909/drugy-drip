"""Contact page (contact.html): message form that opens WhatsApp, how to order, size help."""
from html import escape

from config import BRAND, CITY, EMAIL, INSTAGRAM, INSTAGRAM_HANDLE, PHONE_DISPLAY
from layout import ICON, footer, head, header, page_banner, socials, wa_link


def build():
    rows = [f'<li>{ICON["wa"]}<span><b>WhatsApp</b><a href="{wa_link("Hi " + BRAND + "!")}" target="_blank" rel="noopener">{escape(PHONE_DISPLAY)}</a></span></li>']
    if INSTAGRAM:
        rows.append(f'<li>{ICON["insta"]}<span><b>Instagram</b><a href="{escape(INSTAGRAM)}" target="_blank" rel="noopener">{escape(INSTAGRAM_HANDLE)}</a></span></li>')
    if EMAIL:
        rows.append(f'<li>{ICON["mail"]}<span><b>Email</b><a href="mailto:{escape(EMAIL)}">{escape(EMAIL)}</a></span></li>')
    if CITY:
        rows.append(f'<li>{ICON["pin"]}<span><b>Based in</b>{escape(CITY)}</span></li>')

    body = f"""{page_banner("Talk to us", "CONTACT", "detail-print-2.webp")}
<section class="section">
  <div class="container contact">
    <div class="contact__info">
      <h2 class="title-shadow">HIT US UP</h2>
      <p>Questions about a size, a colour or your order? Send a message and we'll reply on WhatsApp.</p>
      <ul class="contact__list">{"".join(rows)}</ul>
      <div class="footer__social contact__social">{socials()}</div>
    </div>
    <form class="contact__form" data-contact-form novalidate>
      <label><span>Your name *</span><input name="name" type="text" autocomplete="name" required></label>
      <label><span>Phone</span><input name="phone" type="tel" autocomplete="tel" inputmode="tel"></label>
      <label><span>Message *</span><textarea name="message" rows="5" required placeholder="e.g. Is the Oversized Leaf Hoodie available in XL?"></textarea></label>
      <p class="form-err" data-form-err hidden>Please fill in your name and message.</p>
      <button class="btn btn--wa" type="submit">{ICON["wa"]} Send on WhatsApp</button>
    </form>
  </div>
</section>

<section class="section section--grain" id="order">
  <div class="container">
    <div class="section-head section-head--center"><h2 class="title-brush">HOW TO ORDER</h2></div>
    <ol class="steps">
      <li><span>01</span><h3>Pick your fit</h3><p>Choose size and colour on any product and press <b>Add to cart</b>.</p></li>
      <li><span>02</span><h3>Send the cart</h3><p>Open the cart, add your name and city, and press <b>Send order on WhatsApp</b>.</p></li>
      <li><span>03</span><h3>We confirm</h3><p>We reply with stock, final price and delivery details. Pay once it's confirmed.</p></li>
    </ol>
  </div>
</section>

<section class="section" id="sizes">
  <div class="container size-help">
    <div>
      <h2 class="title-shadow">SIZE HELP</h2>
      <p>Everything is cut <b>oversized</b> on purpose. Take your usual size for the baggy look, or one size down for a closer fit.</p>
      <p>Not sure? Send us your <b>height and weight</b> on WhatsApp and we'll tell you which size to pick.</p>
      <a class="btn btn--dark" href="{wa_link("Hi! Which size should I take? My height is ___ and weight is ___")}" target="_blank" rel="noopener">{ICON["wa"]} Ask for my size</a>
    </div>
    <img src="images/stock/outfit-6.webp" alt="" loading="lazy" width="600" height="1420">
  </div>
</section>
"""
    return (head(f"Contact | {BRAND}", f"Contact {BRAND} on WhatsApp for orders, sizes and new drops.")
            + header("contact") + body + footer())
