// ragite-demo: small global enhancements for every page (extra_js_urls in metadata.yml).
// Progressive: without it, Datasette's pages still work; the stylesheet does the visual work.
(function () {
  "use strict";
  const MARK = '<svg viewBox="0 0 64 64" aria-hidden="true" focusable="false">' +
    '<defs><clipPath id="rd-doc"><path d="M13 16H33A7 7 0 0 1 40 23V51A7 7 0 0 1 33 58H13A7 7 0 0 1 6 51V23A7 7 0 0 1 13 16Z"/></clipPath></defs>' +
    '<path fill="var(--rg-logo-doc)" d="M13 16H33A7 7 0 0 1 40 23V51A7 7 0 0 1 33 58H13A7 7 0 0 1 6 51V23A7 7 0 0 1 13 16Z"/>' +
    '<path fill="var(--rg-logo-lens)" d="M24 23A17 17 0 1 0 58 23A17 17 0 1 0 24 23Z"/>' +
    '<path fill="var(--rg-logo-hit)" clip-path="url(#rd-doc)" d="M24 23A17 17 0 1 0 58 23A17 17 0 1 0 24 23Z"/></svg>';
  const LINKS = [["/search", "Search", true], ["/demo/doc_info", "Documents"], ["/demo#queries", "Queries"], ["/demo", "SQL"],
                 ["https://github.com/pihme/ragite-demo", "GitHub"]];

  function header() {
    const nav = document.querySelector("header nav");
    if (!nav || nav.querySelector(".rd-brand")) return;
    const brand = document.createElement("a");
    brand.className = "rd-brand"; brand.href = "/";
    brand.innerHTML = MARK + '<span>ragite<span class="rd-suffix">-demo</span></span>';
    brand.setAttribute("aria-label", "ragite-demo home");
    const sep = document.createElement("span"); sep.className = "rd-sep"; sep.setAttribute("aria-hidden", "true");
    nav.prepend(brand, sep);
    const crumbs = nav.querySelector(".crumbs");
    // "home" alone repeats the brand link: drop it, keep deeper crumbs (database / table)
    if (crumbs && crumbs.querySelectorAll("a").length <= 1) { crumbs.remove(); sep.remove(); }
    const links = document.createElement("nav");
    links.className = "rd-links"; links.setAttribute("aria-label", "Demo");
    const here = location.pathname.replace(/\/$/, "") || "/";
    links.innerHTML = LINKS.filter(([href]) => !(href === "/search" && here === "/search")).map(([href, label, cta]) =>
      '<a href="' + href + '"' + (cta ? ' class="rd-cta"' : "") + (href.split("#")[0] === here && !href.includes("#") ? ' aria-current="page"' : "") + ">" + label + "</a>").join("");
    nav.appendChild(links);
  }

  // Canned query pages use the whole SQL as <title>; use the visible heading instead.
  function title() {
    const h1 = document.querySelector("section.content h1");
    if (h1 && document.title.length > 80) document.title = h1.textContent.trim() + " · ragite-demo";
  }

  // Home: "4 tables, 14 hidden tables" is storage noise from ragite's shadow tables.
  function homeCounts() {
    if (!document.body.classList.contains("index")) return;
    document.querySelectorAll("section.content > p").forEach((p) => {
      if (/hidden tables?/.test(p.textContent)) p.textContent = p.textContent.replace(/,?\s*[\d,]+ hidden tables?/, "").trim();
    });
  }

  function ready() { header(); title(); homeCounts(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", ready); else ready();
})();
