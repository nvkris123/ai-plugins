---
name: lint
description: Health-check the wiki — link integrity, structure, graph health, content drift, readability, and gaps. Reports findings grouped by severity and proposes fixes. Invoke when the user types `/lint`, or asks for a wiki health check, audit, or cleanup pass.
---

# /lint

**Find what has rotted, propose fixes, and apply nothing until the user approves.**

## The short version

- Six check groups: **links, structure, graph, content, readability, gaps**.
- Report findings grouped by severity; skip empty categories rather than padding.
- Propose fixes; apply only on approval.
- Append a `lint` entry to `wiki/log.md` when done.

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

## Link integrity

Replicate the Markdown server's resolution order: **exact path → walk up from the linking file's directory → basename fallback, only when the target has no slash.**

- **L1** Every wikilink resolves to an existing file.
- **L2** Every *unprefixed* link resolves to a file inside **this brain**. A bare link to a missing page can silently resolve into a sibling repo through the basename fallback — this check turns that back into a visible error.
- **L3** No two files in the wiki share a basename. A duplicate makes bare links silently resolve to the wrong page, with no error.
- **L4** Link form is correct: prefixed for `people/`, `sources/`, `desk/`, `desk/archived/`; bare for root subject pages.
- **L5** No `![[transclusion]]` syntax anywhere — it renders as a plain link, not an embed.
- **L6** Every `[[page#Section]]` anchor points at a heading that exists.
- **L7** Report broken links in `log.md` **separately and informationally**. It's append-only history and legitimately references renamed or never-created pages. **Never rewrite `log.md` to fix them.**

## Structure

- **S1** Frontmatter is valid: `kind` from the allowed set and on subject pages only, dates well-formed, every slug in `sources:` exists, `derived_from:` present whenever `derived: true`. **Flag any `type:` field** — it means an agent reintroduced a folder-duplicating field.
- **S2** No directories outside the tree above. Flag and stop — do not reorganize on your own.
- **S3** Every page appears in `index.md` exactly once, and no index entry points at a page that no longer exists.
- **S4** Pages over ~400 lines — propose a split.
- **S5** `assets/` contains no markdown; page folders contain no binaries.

## Graph

- **G1** Orphans — pages with no inbound link from any other page. `index.md` and `log.md` are exempt.
- **G2** Missing pages — something named repeatedly across pages with no page of its own. Propose a stub.
- **G3** Missing cross-references — page A mentions the title or a listed alias of page B in prose without linking it.

## Content

- **C1** Contradictions between pages not recorded in a `## Contradictions` section.
- **C2** Stale claims — a claim a newer source supersedes. Compare a page's `updated:` against the newest source that touches it.
- **C3** Non-trivial claims with no citation.
- **C4** Derived drift — for every page with `derived: true`, re-derive it from `derived_from:` and report divergence.
- **C5** Desk hygiene — desk pages past their `expires:` date or whose actions all read as complete. Propose moving them to `desk/archived/` **with `/second-brain:move`, never by hand**.

## Readability

The layering rules are not garnish — a correct page in the wrong shape is unusable.

- **R1** Every page opens with an H1 followed by one bold sentence saying what it is.
- **R2** Every page over ~40 lines has a `## The short version` that summarizes rather than introduces.
- **R3** No paragraph over 4 lines; no section over ~40 lines without subheadings.
- **R4** No bullet nested more than two deep.
- **R5** Pages whose subject has a shape — sequence, hierarchy, timeline, comparison, relational structure — but no diagram. Propose one and say which kind.
- **R6** Diagrams that only restate the prose around them. Propose deleting.
- **R7** Pages that have grown into walls of text. Propose a **re-layer, not a trim** — move detail down a layer or out to a linked page, never cut facts.

## Gaps

- **X1** Questions the wiki raises but doesn't answer.
- **X2** Sources worth acquiring, or facts worth a web search.
- **X3** Good follow-up questions to investigate.

## Reporting

Group by severity: **broken** (L1-L6, S1-S3) first, then **drift** (C1-C5), then **shape** (R1-R7), then **opportunities** (G2, X1-X3). For each finding give the file, the problem in one line, and the proposed fix.

Apply nothing until the user approves. Then append:

```markdown
## [YYYY-MM-DD] lint | <scope>

- Checked: <N pages>
- Fixed: <what>
- Outstanding: <what the user declined or deferred>
```
