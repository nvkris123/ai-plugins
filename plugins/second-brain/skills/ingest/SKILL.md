---
name: ingest
description: Process a new source into the wiki. Read it, discuss takeaways with the user, write a source page, ripple updates across affected pages, update index.md, and append a log entry. Invoke when the user types `/ingest <path-or-url>` or asks to "process", "ingest", "add to the wiki", or "summarize and file" a source.
---

# /ingest

**Read one source, integrate it into the wiki, and leave the wiki richer than a flat archive would.**

## The short version

1. Acquire and read the source.
2. **Discuss takeaways with the user before writing anything.** Never skip this.
3. Read `wiki/index.md` and the adjacent pages.
4. Write the source page — full or thin.
5. Ripple updates across every affected page (commonly 5-15 of them).
6. Update `wiki/index.md`.
7. Append to `wiki/log.md`.
8. Report in ~5 lines.

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

## 1. Acquire and read

- **Under `raw/`** — read directly.
- **Elsewhere on disk** — ask whether to copy into `raw/` (preferred) or leave in place.
- **URL** — fetch it. Offer to save a snapshot at `raw/<YYYY-MM-DD>-<slug>.md` for durability; the web changes, the wiki should not.
- **PDF / long transcript** — read in chunks.

Pick the source slug now: kebab-case and distinctive (`pd-overview-2026-06-24`, not `meeting`). Dated slugs are the convention for meetings and talks.

## 2. Discuss takeaways FIRST

Before writing anything, surface the key takeaways in chat as 5-10 bullets, then ask:

- Which of these matter most?
- Anything to challenge, flag uncertain, or dig into?
- What deserves its own page versus a mention?

**This is the most important step.** The user's reactions calibrate emphasis, and skipping it is the most common way ingestion goes wrong.

## 3. Read the index and neighbours

Read `wiki/index.md` to know what exists. Read the clearly relevant pages. This is what makes ingestion *compound* rather than accumulate.

## 4. Write the source page

Path: `wiki/sources/<slug>.md`.

**Thin** when the raw file is already clean markdown prose — don't re-summarize what's already tight. Keep frontmatter, citation, a link to the raw file, key takeaways, entities mentioned.

**Full** for transcripts, audio, PDFs, web pages, data, books:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
sensitive: true          # if applicable
---

# <Source Title>

**Citation**: <author/speaker>, <where>, <date>. `raw/<path>` or <url>
**Type**: paper | article | book | talk | meeting | thread | dataset | other
**Read on**: YYYY-MM-DD

**One bold sentence saying what this source is and why it matters.**

## The short version
- 3-6 bullets carrying the whole source. A reader who stops here knows what a
  two-hour meeting was about.

## Key takeaways
- 5-10 items, each citing a section where applicable.

## Entities mentioned
- [[people/<slug>]] — context
- [[<subject-slug>]] — context

## Quotes & passages
> "..." — section/timestamp

## Open questions
- What this source raises but doesn't answer; follow-up sources worth finding.
```

There is **no `type:` frontmatter field** — the folder says it. Add a diagram when the source describes a sequence, hierarchy, or architecture.

## 5. Ripple updates

For each person, subject, or desk item the source touches:

- **Page exists** — update it, citing `... per [[sources/<slug>]]`. If the source **contradicts** existing content, add a `## Contradictions` section with both views. Never silently overwrite.
- **Page missing but warranted** — create it, at minimum a stub with frontmatter and a one-line description plus a backlink.
- **Bump `updated:`** on every page touched.

A single ingest commonly touches 5-15 pages. That's the point.

## 6. Update `wiki/index.md`

Add the source and any new pages under the right groupings, each with a one-line summary. Keep the "start here" preamble at the top accurate.

## 7. Append to `wiki/log.md`

```markdown
## [YYYY-MM-DD] ingest | <Source Title>

- Source: [[sources/<slug>]]
- New pages: [[people/x]], [[y]] (or "none")
- Updated: [[z]], [[people/w]]
- Contradictions: <if any, with link>
- Follow-ups: <open questions worth pursuing>
```

## 8. Report

Source page written, N pages updated, M stubs created, contradictions flagged, suggested follow-ups. About five lines.

## Notes

- If the source is sprawling, propose a focused ingest rather than a thin pass over everything.
- Be honest about what the source doesn't cover — open questions feed `/lint`.
- **Never edit `raw/`.**
