/* Drugy Drip: menu, hero slider, best-seller tabs, shop filters, contact form. */
(function () {
  "use strict";

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }

  /* ---------- mobile menu ---------- */
  var nav = $("#site-nav");
  var opener = $("[data-nav-open]");
  function setNav(open) {
    if (!nav) return;
    nav.classList.toggle("is-open", open);
    document.body.classList.toggle("no-scroll", open);
    if (opener) opener.setAttribute("aria-expanded", open ? "true" : "false");
  }
  document.addEventListener("click", function (e) {
    if (e.target.closest("[data-nav-open]")) setNav(true);
    else if (e.target.closest("[data-nav-close]")) setNav(false);
    else if (nav && nav.classList.contains("is-open") && (e.target.closest(".nav a") || !e.target.closest(".nav"))) setNav(false);
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setNav(false); });

  /* ---------- hero slider ---------- */
  var slider = $("[data-slider]");
  if (slider) {
    var slides = $$("[data-slide]", slider);
    var dots = $$("[data-dot]", slider);
    var cur = 0, timer = null;
    var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var show = function (i) {
      cur = (i + slides.length) % slides.length;
      slides.forEach(function (s, n) { s.classList.toggle("is-active", n === cur); s.setAttribute("aria-hidden", n === cur ? "false" : "true"); });
      dots.forEach(function (d, n) { if (n === cur) d.setAttribute("aria-current", "true"); else d.removeAttribute("aria-current"); });
    };
    var play = function () {
      clearInterval(timer);
      if (!still) timer = setInterval(function () { show(cur + 1); }, 6000);
    };
    slider.addEventListener("click", function (e) {
      if (e.target.closest("[data-prev]")) show(cur - 1);
      else if (e.target.closest("[data-next]")) show(cur + 1);
      else if (e.target.closest("[data-dot]")) show(parseInt(e.target.closest("[data-dot]").dataset.dot, 10));
      else return;
      play();
    });
    slider.addEventListener("mouseenter", function () { clearInterval(timer); });
    slider.addEventListener("mouseleave", play);
    // swipe on phones
    var x0 = null;
    slider.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    slider.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) { show(cur + (dx < 0 ? 1 : -1)); play(); }
      x0 = null;
    });
    show(0);
    play();
  }

  /* ---------- best-seller tabs ---------- */
  $$("[role=tablist]").forEach(function (list) {
    var section = list.closest("section");
    list.addEventListener("click", function (e) {
      var tab = e.target.closest("[data-tab]");
      if (!tab) return;
      $$("[data-tab]", list).forEach(function (t) { t.setAttribute("aria-selected", t === tab ? "true" : "false"); });
      $$("[data-panel]", section).forEach(function (p) { p.hidden = p.dataset.panel !== tab.dataset.tab; });
    });
  });

  /* ---------- shop: filter, search, sort ---------- */
  var shop = $("[data-shop]");
  if (shop) {
    var grid = $("[data-grid]", shop);
    var cards = $$(".card", grid);
    var search = $("[data-search]", shop);
    var sort = $("[data-sort]", shop);
    var filter = "all";
    cards.forEach(function (c, i) { c.dataset.order = i; });

    var apply = function () {
      var q = (search.value || "").trim().toLowerCase();
      var shown = 0;
      cards.forEach(function (c) {
        var okCat = filter === "all" || c.dataset.cat === filter || (" " + c.dataset.tags + " ").indexOf(" " + filter + " ") > -1;
        var okText = !q || (c.dataset.name + " " + c.dataset.cat).toLowerCase().indexOf(q) > -1;
        c.hidden = !(okCat && okText);
        if (!c.hidden) shown++;
      });
      var by = sort.value;
      cards.slice().sort(function (a, b) {
        if (by === "low") return a.dataset.price - b.dataset.price;
        if (by === "high") return b.dataset.price - a.dataset.price;
        return a.dataset.order - b.dataset.order;
      }).forEach(function (c) { grid.appendChild(c); });
      $("[data-count]", shop).textContent = shown + (shown === 1 ? " product" : " products");
      $("[data-empty]", shop).hidden = shown > 0;
    };
    var setFilter = function (f) {
      filter = f;
      $$("[data-filter]", shop).forEach(function (b) { b.classList.toggle("is-on", b.dataset.filter === f); });
      apply();
    };
    shop.addEventListener("click", function (e) {
      var chip = e.target.closest("[data-filter]");
      if (chip) {
        setFilter(chip.dataset.filter);
        history.replaceState(null, "", chip.dataset.filter === "all" ? location.pathname : "#" + chip.dataset.filter);
      }
    });
    search.addEventListener("input", apply);
    sort.addEventListener("change", apply);

    // shop.html#hoodies, #new or #search from other pages
    var fromHash = function () {
      var h = location.hash.slice(1);
      if (h === "search") { search.focus(); return; }
      if (h && $('[data-filter="' + h + '"]', shop)) setFilter(h);
    };
    window.addEventListener("hashchange", fromHash);
    fromHash();
  }

  /* ---------- contact form -> WhatsApp ---------- */
  var form = $("[data-contact-form]");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = form.name.value.trim(), msg = form.message.value.trim(), phone = form.phone.value.trim();
      var err = $("[data-form-err]", form);
      if (!name || !msg) { err.hidden = false; (name ? form.message : form.name).focus(); return; }
      err.hidden = true;
      var text = "*Message from Drugy Drip website*\n\nName: " + name + (phone ? "\nPhone: " + phone : "") + "\n\n" + msg;
      window.open("https://wa.me/" + (window.DD_WHATSAPP || "") + "?text=" + encodeURIComponent(text), "_blank", "noopener");
    });
  }

  /* ---------- back to top + year ---------- */
  var up = $("[data-to-top]");
  if (up) {
    window.addEventListener("scroll", function () { up.classList.toggle("is-show", window.scrollY > 700); }, { passive: true });
    up.addEventListener("click", function () { window.scrollTo({ top: 0 }); });
  }
  $$("[data-year]").forEach(function (y) { y.textContent = new Date().getFullYear(); });
})();
