/* Drugy Drip: shopping cart.
   Customer product add karta hai, phir poori list WhatsApp pe chali jaati hai.
   Cart browser mein (localStorage) save rehta hai, website pe kuch store nahi hota. */
(function () {
  "use strict";

  var WHATSAPP = window.DD_WHATSAPP || "";
  var KEY = "drugydrip-cart-v1";

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function money(n) { return "$" + Number(n).toFixed(2); }

  /* ---------- storage ---------- */
  function load() {
    try {
      var d = JSON.parse(localStorage.getItem(KEY) || "null");
      if (d && Array.isArray(d.items)) return d;
    } catch (e) { /* private mode etc. */ }
    return { items: [], note: "", name: "", place: "" };
  }
  var state = load();
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* ignore */ }
    render();
  }

  function optText(opts) {
    return Object.keys(opts).map(function (k) { return k + ": " + opts[k]; }).join(" | ");
  }
  function count() { return state.items.reduce(function (n, it) { return n + it.qty; }, 0); }
  function total() { return state.items.reduce(function (n, it) { return n + it.qty * (it.price || 0); }, 0); }

  /* ---------- add from a product card ---------- */
  function addFromCard(card) {
    var opts = {};
    try { opts = JSON.parse(card.dataset.fixed || "{}"); } catch (e) { opts = {}; }
    $$("select[data-opt]", card).forEach(function (s) { opts[s.dataset.opt] = s.value; });
    var key = card.dataset.pid + "|" + JSON.stringify(opts);
    var existing = state.items.filter(function (it) { return it.key === key; })[0];
    if (existing) existing.qty = Math.min(99, existing.qty + 1);
    else state.items.push({ key: key, name: card.dataset.name, price: Number(card.dataset.price) || 0, img: card.dataset.img || "", opts: opts, qty: 1 });
    save();
    bump();
    toast(card.dataset.name + " (" + (opts.Size || "") + ") added");
  }

  document.addEventListener("click", function (e) {
    var add = e.target.closest("[data-add]");
    if (add) { addFromCard(add.closest("[data-pid]")); return; }
    if (e.target.closest("[data-cart-open]")) openDrawer();
  });

  /* ---------- header badge ---------- */
  function bump() {
    $$("[data-cart-count]").forEach(function (b) {
      b.classList.remove("is-bump");
      void b.offsetWidth;
      b.classList.add("is-bump");
    });
  }

  /* ---------- toast ---------- */
  var toastEl = null, toastTimer = null;
  function toast(msg) {
    if (!toastEl) {
      toastEl = document.createElement("div");
      toastEl.className = "toast";
      toastEl.setAttribute("role", "status");
      toastEl.innerHTML = '<span data-toast-msg></span><button type="button" data-cart-open>View cart</button>';
      document.body.appendChild(toastEl);
    }
    $("[data-toast-msg]", toastEl).textContent = msg;
    toastEl.classList.add("is-show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove("is-show"); }, 3200);
  }

  /* ---------- drawer ---------- */
  var drawer = document.createElement("div");
  drawer.className = "cart";
  drawer.innerHTML =
    '<div class="cart__backdrop" data-cart-close></div>' +
    '<aside class="cart__panel" role="dialog" aria-modal="true" aria-labelledby="cart-title">' +
    '  <div class="cart__head"><h2 id="cart-title">YOUR CART <span data-cart-total></span></h2>' +
    '    <button class="cart__close" type="button" data-cart-close aria-label="Close cart"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>' +
    '  <div class="cart__body">' +
    '    <ul class="cart__items" data-cart-items></ul>' +
    '    <div class="cart__empty" data-cart-empty><p><b>Your cart is empty.</b></p><p>Pick a size on any product and press <b>Add to cart</b>.</p></div>' +
    '    <div class="cart__form" data-cart-form>' +
    '      <label><span>Your name <span class="req">*</span></span><input type="text" data-field="name" autocomplete="name"><small class="cart__err" data-err-name hidden>Please write your name.</small></label>' +
    '      <label><span>City</span><input type="text" data-field="place" autocomplete="address-level2"></label>' +
    '      <label><span>Note (anything else)</span><textarea data-field="note" rows="2"></textarea></label>' +
    "    </div>" +
    "  </div>" +
    '  <div class="cart__foot" data-cart-foot>' +
    '    <p class="cart__total"><span>Subtotal</span><span data-cart-sum></span></p>' +
    '    <button class="btn btn--wa cart__send" type="button" data-cart-send><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2z"/><path d="M16.6 14.1c-.3-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.8-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 2.9 2.9 0 0 0-.9 2.2 5 5 0 0 0 1.1 2.7 11.5 11.5 0 0 0 4.4 3.9c1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.8-.3z"/></svg> Send order on WhatsApp</button>' +
    '    <p class="cart__hint">We confirm stock, delivery and final price on WhatsApp.</p>' +
    '    <button class="cart__clear" type="button" data-cart-clear>Clear cart</button>' +
    "  </div>" +
    "</aside>";
  document.body.appendChild(drawer);

  var lastFocus = null;
  function openDrawer() {
    lastFocus = document.activeElement;
    drawer.classList.add("is-open");
    document.body.classList.add("no-scroll");
    setTimeout(function () { $(".cart__close", drawer).focus(); }, 60);
  }
  function closeDrawer() {
    drawer.classList.remove("is-open");
    document.body.classList.remove("no-scroll");
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  drawer.addEventListener("click", function (e) {
    if (e.target.closest("[data-cart-close]")) closeDrawer();
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && drawer.classList.contains("is-open")) closeDrawer(); });

  $("[data-cart-items]", drawer).addEventListener("click", function (e) {
    var li = e.target.closest("[data-key]");
    if (!li) return;
    var it = state.items.filter(function (x) { return x.key === li.dataset.key; })[0];
    if (!it) return;
    if (e.target.closest("[data-remove]")) {
      state.items = state.items.filter(function (x) { return x !== it; });
    } else if (e.target.closest("[data-inc]")) {
      it.qty = Math.min(99, it.qty + parseInt(e.target.closest("[data-inc]").dataset.inc, 10));
      if (it.qty < 1) state.items = state.items.filter(function (x) { return x !== it; });
    } else return;
    save();
  });

  $$("[data-field]", drawer).forEach(function (f) {
    f.addEventListener("input", function () {
      state[f.dataset.field] = f.value;
      if (f.dataset.field === "name" && f.value.trim()) $("[data-err-name]", drawer).hidden = true;
      try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* ignore */ }
    });
  });

  $("[data-cart-clear]", drawer).addEventListener("click", function () {
    if (!state.items.length) return;
    if (!confirm("Remove all items from the cart?")) return;
    state.items = [];
    save();
  });

  $("[data-cart-send]", drawer).addEventListener("click", function () {
    if (!state.items.length) return;
    if (!state.name || !state.name.trim()) {
      $("[data-err-name]", drawer).hidden = false;
      $('[data-field="name"]', drawer).focus();
      return;
    }
    var lines = ["*New order from Drugy Drip website*", ""];
    state.items.forEach(function (it, n) {
      lines.push((n + 1) + ". *" + it.name + "*");
      lines.push("    " + optText(it.opts) + " | Qty: " + it.qty + " | " + money(it.price * it.qty));
    });
    lines.push("", "Subtotal: " + money(total()));
    lines.push("", "Name: " + state.name.trim());
    if (state.place && state.place.trim()) lines.push("City: " + state.place.trim());
    if (state.note && state.note.trim()) lines.push("Note: " + state.note.trim());
    window.open("https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(lines.join("\n")), "_blank", "noopener");
  });

  /* ---------- render ---------- */
  function render() {
    var n = count();
    $$("[data-cart-count]").forEach(function (b) { b.textContent = n; b.hidden = n === 0; });
    $("[data-cart-total]", drawer).textContent = n ? "(" + n + ")" : "";
    $("[data-cart-sum]", drawer).textContent = money(total());
    $("[data-cart-items]", drawer).innerHTML = state.items.map(function (it) {
      return '<li class="cart-item" data-key="' + esc(it.key) + '">' +
        '<span class="cart-item__img">' + (it.img ? '<img src="' + esc(it.img) + '" alt="">' : "") + "</span>" +
        '<span class="cart-item__info"><b>' + esc(it.name) + "</b>" +
        "<small>" + esc(optText(it.opts)) + "</small>" +
        '<span class="cart-item__price">' + money(it.price * it.qty) + "</span>" +
        '<span class="cart-item__qty"><button type="button" data-inc="-1" aria-label="Less">&minus;</button><span>' + it.qty + '</span><button type="button" data-inc="1" aria-label="More">+</button></span></span>' +
        '<button class="cart-item__remove" type="button" data-remove aria-label="Remove ' + esc(it.name) + '"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 13a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1l1-13M9 7V4h6v3"/></svg></button>' +
        "</li>";
    }).join("");
    var empty = state.items.length === 0;
    $("[data-cart-empty]", drawer).hidden = !empty;
    $("[data-cart-form]", drawer).hidden = empty;
    $("[data-cart-foot]", drawer).hidden = empty;
    $$("[data-field]", drawer).forEach(function (f) { if (document.activeElement !== f) f.value = state[f.dataset.field] || ""; });
  }
  render();

  // keep tabs in sync
  window.addEventListener("storage", function (e) { if (e.key === KEY) { state = load(); render(); } });
})();
