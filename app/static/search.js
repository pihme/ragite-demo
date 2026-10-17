// Search page for the ragite demo. Calls the hybrid canned query `search` (metadata.yml) through
// Datasette's JSON API and renders the rows as cards. No external dependencies.
(function () {
  "use strict";

  const root = document.getElementById("ragite-search");
  const db = root.dataset.db;
  const form = document.getElementById("rs-form");
  const input = document.getElementById("rs-q");
  const collection = document.getElementById("rs-collection");
  const status = document.getElementById("rs-status");
  const results = document.getElementById("rs-results");
  const sqlLink = document.getElementById("rs-sql");

  const COLLECTION_LABEL = { "sqlite-docs": "SQLite docs", wikipedia: "Wikipedia", "ragite-docs": "ragite docs" };

  function words(q) {
    return (q.match(/[\p{L}\p{N}_]+/gu) || []);
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  function highlight(text, q) {
    const terms = words(q).filter((w) => w.length > 2).map((w) => w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
    const safe = escapeHtml(text);
    if (!terms.length) return safe;
    return safe.replace(new RegExp("(?<![\\p{L}\\p{N}])(" + terms.join("|") + ")(?![\\p{L}\\p{N}])", "giu"), "<mark>$1</mark>");
  }

  function headingPath(json) {
    try {
      const path = JSON.parse(json || "[]");
      return Array.isArray(path) ? path.join(" › ") : "";
    } catch (e) {
      return "";
    }
  }

  function card(row, q) {
    const li = document.createElement("li");
    li.className = "rs-card";
    const path = headingPath(row.heading_path);
    li.innerHTML =
      '<div class="rs-card-head">' +
        '<a class="rs-card-title" href="' + escapeHtml(row.url) + '">' + escapeHtml(row.title) + "</a>" +
        '<span class="rs-badge rs-badge-' + escapeHtml(row.collection) + '">' +
          escapeHtml(COLLECTION_LABEL[row.collection] || row.collection) + "</span>" +
      "</div>" +
      (path ? '<div class="rs-card-path">' + escapeHtml(path) + "</div>" : "") +
      '<p class="rs-card-text">' + highlight(row.chunk || "", q) + "</p>" +
      '<div class="rs-card-meta"><span class="rs-card-source">' + escapeHtml(row.url) + "</span>" +
        '<span class="rs-score" title="Reciprocal Rank Fusion score, higher is better">score ' +
        Number(row.score).toFixed(4) + "</span></div>";
    return li;
  }

  async function run(pushState) {
    const q = input.value.trim();
    const coll = collection.value;
    const params = new URLSearchParams();
    if (q) params.set("q", q);
    if (coll) params.set("collection", coll);
    if (pushState) history.pushState(null, "", "?" + params.toString());

    results.innerHTML = "";
    sqlLink.textContent = "";
    if (!q) {
      status.textContent = "";
      return;
    }
    const api = new URLSearchParams({ q: q, collection: coll });
    const page = db + "/search?" + api.toString();
    status.textContent = "Searching…";
    const started = performance.now();
    try {
      const resp = await fetch(db + "/search.json?" + api.toString() + "&_shape=objects");
      const data = await resp.json();
      if (!resp.ok || data.ok === false) throw new Error(data.error || resp.statusText);
      const rows = data.rows || [];
      const ms = Math.round(performance.now() - started);
      status.textContent = rows.length
        ? rows.length + " passage" + (rows.length === 1 ? "" : "s") + " in " + ms + " ms"
        : "No passages found.";
      rows.forEach((row) => results.appendChild(card(row, q)));
      sqlLink.innerHTML = '<a href="' + escapeHtml(page) + '">Show this search as SQL</a> · ';
    } catch (err) {
      status.textContent = "Search failed: " + err.message;
    }
  }

  function fromUrl() {
    const params = new URLSearchParams(location.search);
    input.value = params.get("q") || "";
    collection.value = params.get("collection") || "";
    run(false);
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    run(true);
  });
  collection.addEventListener("change", () => input.value.trim() && run(true));
  window.addEventListener("popstate", fromUrl);
  fromUrl();
})();
