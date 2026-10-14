---
name: query
description: Answer a question against the wiki. Read index.md to find relevant pages, read them, answer in layers with citations, and offer to file the answer back as a page so explorations compound. Invoke when the user types `/query <question>` or asks any substantive question about the wiki's contents.
---

# /query

**Answer from the wiki, with citations, in layers — and file the good answers back so they compound.**

## The short version

1. Read `wiki/index.md` first. Never answer from memory.
2. Read the relevant pages; follow wikilinks.
3. Answer in layers: the direct answer first, then support, then caveats.
4. Cite claims that need backing — not as decoration.
5. Offer to file the answer as a page. Don't pre-write it into the reply.

## Layout

```
./
├── CLAUDE.md
├── raw/                        # immutable sources; never write here
└── wiki/
    ├── index.md                # catalog — always start here
    ├── log.md                  # append-only history
    ├── <slug>.md               # subject pages — the default bucket
    ├── people/<slug>.md        # one page per human
    ├── sources/<slug>.md       # one page per thing read
    ├── desk/<slug>.md          # pages with a status or an expiry
    │   └── archived/<slug>.md  # retired desk pages
    └── assets/                 # non-markdown only
```

**Filing, in order:** is it a human → `people/`; is it your reading of one
thing read → `sources/`; does it have something to do on it or an expiry → `desk/`;
otherwise it goes loose in `wiki/`. **Never create a directory that isn't in the tree
above** — no `concepts/`, `topics/`, `entities/`, or `synthesis/`.

**Links:** prefixed for foldered pages (`[[people/x]]`, `[[sources/y]]`, `[[desk/z]]`),
bare for root subject pages (`[[x]]`). Exact, case-sensitive filename match; pipe an
alias for prose (`[[people/jane-doe|Jane Doe]]`). Filenames must be unique across the
wiki. No `![[transclusion]]`.

## Procedure

**1. Read the index.** It's the catalog and it's cheap. Identify candidates.

**2. Read the pages.** Follow wikilinks aggressively — the wiki is small and dense, so the cost is low. If wiki coverage is thin, fall back to the `raw/` original the source page points at, and cite it explicitly (`per raw/<filename>`).

For questions touching 5+ pages, delegate the read pass to the **wiki-researcher** subagent to keep the main context clean.

**3. Answer in layers.**

- The direct answer in one or two sentences.
- Then the supporting detail.
- Then caveats and uncertainty.

Don't restage the derivation chain or list every page consulted. Lead with the answer; the user should be able to stop after the first two sentences.

**4. Pick the right form.** Prose, a comparison table, a Mermaid diagram, a draw.io file, a chart, a deck. **If the answer is fundamentally about structure or sequence, draw it rather than describing it.**

**5. Be honest about gaps.** If the wiki doesn't answer the question, say what's missing rather than filling from training data. Suggest a page to create or a source to ingest.

**6. Surface contradictions.** If two pages disagree, name both rather than silently picking a winner.

**7. Offer to file it.** A comparison, an analysis, a connection found — these shouldn't evaporate into chat history. Ask before writing, then:

- File it as a **root subject page** if it's about a thing or a question.
- File it under **`desk/`** if it has actions or an expiry.
- Set `derived: true` and `derived_from: [...]` if an agent could rebuild it from other pages.
- Update `wiki/index.md` and append a `query` entry to `wiki/log.md`.

## Chat answers are not wiki pages

Wikilink syntax is for files. In a chat reply write plain names — "Jane Doe", not `[[people/jane-doe]]`. Mention a path only when the point is where the page lives.
