// Search page for ragite-demo. Calls the hybrid canned query `search` (metadata.yml) through
// Datasette's JSON API and renders the rows as cards. No external dependencies.
// Source chips, "show more" paging, heading hits without duplicate text, readable relevance,
// whole-word highlights, links into the demo data.
(function () {
  "use strict";

  const root = document.getElementById("ragite-search");
  const db = root.dataset.db;
  const form = document.getElementById("rs-form");
  const input = document.getElementById("rs-q");
  const chips = document.getElementById("rs-chips");
  const status = document.getElementById("rs-status");
  const results = document.getElementById("rs-results");
  const more = document.getElementById("rs-more");
  const empty = document.getElementById("rs-empty");
  const filterHint = document.getElementById("rs-filter-hint");
  const ISSUE_49 = "https://github.com/pihme/ragite/issues/49";
  const FEW = 5;
  const PAGE = 5;
  // RRF with k = 60 and 50 candidates per ranking: a passage found by only one ranking scores at most
  // 1/61; one found by both scores at least 2/110. So score > 1/61 means "both rankings found it".
  const ONE_LIST_MAX = 1 / 61;

  const COLLECTION_LABEL = { "sqlite-docs": "SQLite docs", wikipedia: "Wikipedia", "ragite-docs": "ragite docs" };

  let cache = {};   // q -> { coll -> rows }
  let shown = PAGE;

  function words(q) {
    return (q.match(/[\p{L}\p{N}_]+/gu) || []);
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  // Match the query words on the raw chunk text and escape each piece afterwards, so a word like
  // "amp" or "quot" can never match inside an entity that escaping added. Neighbouring hits that are
  // only separated by spaces or hyphens become one mark ("Write-Ahead Logging", not three pieces).
  function highlight(text, q) {
    const terms = words(q).filter((w) => w.length > 2).map((w) => w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
    if (!terms.length) return escapeHtml(text);
    // A term must start a word and takes the whole word with it ("vacuum" marks "auto_vacuum"
    // and "VACUUMs", never the tail of "xvacuum"), so a highlight never stops mid-identifier.
    const re = new RegExp("(?<![\\p{L}\\p{N}_])((?:[\\p{L}\\p{N}]+_)*(?:" + terms.join("|") + ")[\\p{L}\\p{N}_]*)", "giu");
    const parts = text.split(re);
    let out = "";
    for (let i = 0; i < parts.length; i++) {
      if (i % 2) {
        let run = parts[i];
        while (i + 2 < parts.length && /^[\s\-‐]+$/.test(parts[i + 1]) && parts[i + 1].length <= 2) {
          run += parts[i + 1] + parts[i + 2];
          i += 2;
        }
        out += "<mark>" + escapeHtml(run) + "</mark>";
      } else {
        out += escapeHtml(parts[i]);
      }
    }
    return out;
  }

  // Control characters (NUL above all) cannot be part of a search; SQLite would reject the query
  // with an "unterminated string" error, so they become spaces before the query is sent.
  function cleanQuery(q) {
    return q.replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g, " ").trim();
  }

  function parseList(json) {
    try {
      const v = JSON.parse(json || "[]");
      return Array.isArray(v) ? v : [];
    } catch (e) {
      return [];
    }
  }

  function headingPath(json) {
    return parseList(json).join(" › ");
  }

  // A short hit (often a bare heading) comes with the next chunks of its section as context
  // (column `context`, a JSON array of chunk texts; see the `search` query in metadata.yml).
  function contextHtml(json, q) {
    const ctx = parseList(json);
    if (!ctx.length) return "";
    return '<div class="rs-card-context" title="The text that follows this passage in the document">' +
      ctx.map((t) => '<p class="rs-card-text">' + highlight(String(t), q) + "</p>").join("") + "</div>";
  }

  // ragite fuses a fixed number of candidates over all sources first; the source filter only sees
  // those (pihme/ragite#49). Say so whenever a filter is active, louder when it leaves few rows.
  function filterHintHtml(coll, count) {
    if (!coll) return "";
    const name = escapeHtml(COLLECTION_LABEL[coll] || coll);
    const link = '<a href="' + ISSUE_49 + '">ragite#49</a>';
    if (count < FEW) {
      return "<strong>" + (count ? "Only " + count + (count === 1 ? " passage" : " passages") : "No passages") +
        " from " + name + " made it into ragite's top candidates.</strong> More may match: the source filter is applied " +
        "after ragite has picked its best candidates from all sources. Search all sources, or rephrase the question (" + link + ").";
    }
    return "Filtered to " + name + ": ragite picks its best candidates from all sources first, so passages that rank lower " +
      "overall are not shown here (" + link + ").";
  }

  const norm = (s) => String(s || "").trim().toLowerCase().replace(/[\s:.]+$/, "");

  // Relevance for people: a bar relative to the best card of this search, plus whether both
  // rankings (meaning and keywords) found the passage. The raw RRF score stays in the tooltip.
  function relevanceHtml(row, best, index) {
    const score = Number(row.score);
    const both = score > ONE_LIST_MAX + 1e-9;
    const pct = best > 0 ? Math.max(6, Math.round((score / best) * 100)) : 0;
    const label = index === 0 ? "Best match" : pct >= 95 ? "Very close" : pct >= 85 ? "Close" : "Related";
    const tip = "Reciprocal Rank Fusion score " + score.toFixed(4) + (both
      ? " (found by both the meaning and the keyword ranking)"
      : " (found by one ranking: meaning or keywords)") + "; " + pct + "% of the best card";
    return '<span class="rs-rel" title="' + escapeHtml(tip) + '"><span class="rs-meter" aria-hidden="true"><i style="width:' + pct + '%"></i></span>' +
      label + (both ? ' <span class="rs-both">meaning + keywords</span>' : "") + "</span>";
  }

  // The row page of the chunk in docs_chunks (the search query returns its rowid as chunk_id).
  function chunkUrl(row) {
    return db + "/docs_chunks/" + encodeURIComponent(row.chunk_id);
  }

  function shortUrl(u) {
    try {
      const x = new URL(u);
      return x.hostname.replace(/^www\./, "") + x.pathname.replace(/\/$/, "");
    } catch (e) {
      return u;
    }
  }

  function card(row, q, best, index) {
    const li = document.createElement("li");
    const path = parseList(row.heading_path);
    const ctx = contextHtml(row.context, q);
    const chunk = row.chunk || "";
    // A short hit with context is usually a bare heading: show it as part of the path, and the text
    // that follows as the body, instead of repeating the title or heading as the passage.
    const isSection = !!ctx && chunk.length < 80;
    const repeatsTitle = norm(chunk) === norm(row.title) || (path.length && norm(chunk) === norm(path[path.length - 1]));
    const crumbs = path.map(escapeHtml);
    if (isSection && !repeatsTitle) crumbs.push("<b>" + highlight(chunk, q) + "</b>");
    li.className = "rs-card" + (isSection ? " rs-card--section" : "") + (index === 0 ? " is-top" : "");
    li.innerHTML =
      '<div class="rs-card-kicker"><span class="rs-src">' + escapeHtml(COLLECTION_LABEL[row.collection] || row.collection) + "</span></div>" +
      '<a class="rs-card-title" href="' + escapeHtml(row.url) + '">' + escapeHtml(row.title || "") + "</a>" +
      (crumbs.length ? '<div class="rs-card-path">' + crumbs.join(" › ") + "</div>" : "") +
      (isSection ? "" : '<p class="rs-card-text">' + highlight(chunk, q) + "</p>") + ctx +
      '<div class="rs-card-foot">' + relevanceHtml(row, best, index) +
        '<span class="rs-links">' +
          '<a href="' + escapeHtml(row.url) + '" title="' + escapeHtml(row.url) + '">' + escapeHtml(shortUrl(row.url)) + " ↗</a>" +
          '<a href="' + escapeHtml(db + "/doc_info/" + row.doc_id) + '">Document</a>' +
          '<a href="' + escapeHtml(chunkUrl(row)) + '">Chunk</a>' +
        "</span></div>";
    return li;
  }

  async function fetchRows(q, coll) {
    const api = new URLSearchParams({ q: q, collection: coll });
    const resp = await fetch(db + "/search.json?" + api.toString() + "&_shape=objects");
    const data = await resp.json();
    if (!resp.ok || data.ok === false) throw new Error(data.error || resp.statusText);
    return data.rows || [];
  }

  function currentColl() {
    const c = chips.querySelector("input:checked");
    return c ? c.value : "";
  }

  function setColl(v) {
    const c = [...chips.querySelectorAll("input")].find((i) => i.value === (v || "")) || chips.querySelector('input[value=""]');
    c.checked = true;
  }

  function render(q, coll, ms) {
    const rows = (cache[q] && cache[q][coll]) || [];
    const best = rows.length ? Number(rows[0].score) : 0;
    results.innerHTML = "";
    rows.slice(0, shown).forEach((row, i) => results.appendChild(card(row, q, best, i)));
    const left = rows.length - Math.min(shown, rows.length);
    more.hidden = left <= 0;
    more.textContent = "Show " + Math.min(PAGE, left) + " more · " + left + " left";
    const page = db + "/search?" + new URLSearchParams({ q: q, collection: coll }).toString();
    status.innerHTML = rows.length
      ? escapeHtml(rows.length + " passage" + (rows.length === 1 ? "" : "s") + (ms != null ? " · " + ms + " ms" : "")) +
        ' · <a href="' + escapeHtml(page) + '">Show this search as SQL</a>'
      : "No passages found.";
    filterHint.innerHTML = filterHintHtml(coll, rows.length);
    filterHint.hidden = !coll;
  }

  async function run(pushState) {
    const q = cleanQuery(input.value);
    const coll = currentColl();
    const params = new URLSearchParams();
    if (q) params.set("q", q);
    if (coll) params.set("collection", coll);
    if (pushState) history.pushState(null, "", "?" + params.toString());
    shown = PAGE;
    results.innerHTML = "";
    more.hidden = true;
    filterHint.hidden = true;
    empty.hidden = !!q;
    if (!q) {
      status.textContent = "";
      return;
    }
    if (cache[q] && cache[q][coll]) {
      render(q, coll, null);
      return;
    }
    status.textContent = "Searching…";
    const started = performance.now();
    cache[q] = cache[q] || {};
    try {
      cache[q][coll] = await fetchRows(q, coll);
      render(q, coll, Math.round(performance.now() - started));
    } catch (err) {
      status.textContent = "Search failed: " + err.message;
    }
  }

  function fromUrl() {
    const params = new URLSearchParams(location.search);
    input.value = params.get("q") || "";
    setColl(params.get("collection") || "");
    run(false);
  }

  // Exposed for the browser checks in tests/screenshot.py.
  window.ragiteSearch = { highlight: highlight, cleanQuery: cleanQuery, contextHtml: contextHtml, filterHintHtml: filterHintHtml };

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    run(true);
  });
  chips.addEventListener("change", () => input.value.trim() ? run(true) : null);
  more.addEventListener("click", () => {
    shown += PAGE;
    render(cleanQuery(input.value), currentColl(), null);
    const next = results.children[shown - PAGE];
    if (next) next.querySelector("a").focus({ preventScroll: true });
  });
  window.addEventListener("popstate", fromUrl);
  fromUrl();
})();
