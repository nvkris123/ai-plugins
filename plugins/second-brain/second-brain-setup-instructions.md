I am setting up this folder to be my second brain repo (for all information on .....).
You are going to act as my second brain agent.

Your task at the end of this document is to write the CLAUDE.md for this repo.
Read the whole thing first.

STANDING RULE — ASK, DON'T INVENT.
Everything below is deliberate. Where this document specifies a structure, a name,
or a rule, follow it exactly. Where it leaves something genuinely open, ask me
rather than inventing a convention. Do not add directories,page types,
or frontmatter fields that aren't listed here.


# Initial idea

Based on the raw documents (sources) I add, you incrementally build and maintain a
persistent wiki — a structured, interlinked collection of markdown files that sits
between me and the raw sources. When I add a new source, you don't just index it for
later retrieval. You read it, extract the key information, and integrate it into the
existing wiki — updating pages, revising summaries, noting where new data contradicts
old claims, strengthening or challenging what's already there. The knowledge is
compiled once and then kept current, not re-derived on every query.

That's the key difference: the wiki is a persistent, compounding artifact. The
cross-references are already there. The contradictions have already been flagged.
The wiki keeps getting richer with every source I add and every question I ask.


# Architecture — three layers

1. raw/     Immutable source documents. Articles, papers, transcripts, audio, PDFs,
            images, data files. You read from them and NEVER modify them. Ground truth.
            If I want a source fixed, I edit it myself.

2. wiki/    The markdown wiki. You own this layer end to end — you create pages,
            update them when new sources arrive, maintain cross-references, keep
            everything consistent. I read; you write.

3. CLAUDE.md for claude code, AGENTS.md for codex:  The schema. It tells you how the wiki is structured, what the
            conventions are, and what to do when ingesting, querying, or linting.
            This is what makes you a disciplined wiki maintainer rather than a
            generic chatbot. We co-evolve it: when you discover a convention worth
            keeping, propose an edit rather than acting on it silently.


# Directory structure

Use exactly this. Do not add subdirectories unless I explicitly tell you to.

  ./
  ├── CLAUDE.md for claude code, AGENTS.md for codex
  ├── raw/                       immutable sources; never write here
  └── wiki/
      ├── index.md               content catalog — every page, one-line summary
      ├── log.md                 append-only chronological record
      ├── <slug>.md              subject pages — the default bucket
      ├── people/<slug>.md       one page per human
      ├── sources/<slug>.md      one page per thing I read
      ├── desk/<slug>.md         pages with a status or an expiry
      │   └── archived/<slug>.md retired desk pages
      └── assets/                non-markdown only: images, .drawio, .svg
          └── people/<slug>.jpg  profile photos

WHY THE FOLDERS ARE WHAT THEY ARE. A folder may exist only if its membership test is
a yes/no question with one correct answer that needs no judgment. "Is this a human?"
qualifies. "Is this a concept or a topic?" does not — that needs arbitration, and an
agent arbitrates differently on every run. That is why there is no concepts/,
topics/, entities/, synthesis/, notes/, or analyses/ folder, and why you must not
create one.

FILING IS THREE POSITIVE QUESTIONS, IN ORDER:
  1. Is it a human?                        → people/
  2. Is it my reading of one thing I read? → sources/
  3. Does it have a status or an expiry?   → desk/
  If all three are no, it goes loose in wiki/. There is no fourth category, so there
  is nothing to arbitrate. Anything that is a named thing in the world OR an idea OR
  a subject area OR a comparison OR a derived table is just a subject page at the
  root of wiki/.

DESK. A desk page is one with something to do on it, or a date after which it stops
mattering: plans, trackers, briefings, checklists, prep documents. Subject pages
never retire — they just stop being updated. Desk pages do: when the work is done or
the date has passed, the page moves to desk/archived/.

ASSETS. Only non-markdown files. Reference them by relative path from the page —
e.g. from wiki/people/, a photo is ![Name](../assets/people/<slug>.jpg).


# Page conventions

FILENAMES. kebab-case ASCII, e.g. large-language-models.md, not LLMs.md. The H1
inside the page can be the human-readable title. Filenames must be unique across the
whole wiki — see the link rules for why.

FRONTMATTER. Every wiki page carries:

  ---
  kind: org | product | idea | place | program | event   # subject pages only
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  sources: [source-slug, ...]        # omit on source pages
  aliases: [other names]             # optional
  derived: true                      # optional — see below
  derived_from: [page-slug, ...]     # required when derived: true
  expires: YYYY-MM-DD                # optional, desk pages only
  sensitive: true                    # optional
  ---

There is deliberately NO `type:` field. The folder already says whether a page is a
person, a source, or a desk item, and a duplicated field only creates something that
can drift out of agreement with the path.

`kind` is descriptive only, and it exists precisely because it is NOT a folder.
Nothing in any workflow branches on it, so a wrong value is a one-word edit rather
than a misfiled page.

`expires` is the date after which a desk page stops mattering. Set it whenever the
page has a natural end date; lint uses it to propose archiving.

`derived: true` means an agent could rebuild this page from scratch by reading the
pages in `derived_from` — a calendar, an org chart, a timeline, a roll-up table.
Lint re-derives these and reports drift; hand edits to them are a bug. Test: could I
delete this and regenerate it losslessly?

`sensitive: true` marks personal or private material. Use it normally when working
for me — that's the point of the wiki. But be discreet when summarizing or exporting
anything that could be shared, and never post a sensitive page's content to an
external service without asking me first, per request.

CITATIONS. When a page makes a non-trivial claim, link the source:
"... per [[sources/some-paper-2025]]". A page without citations is a smell.

CONTRADICTIONS. When a new source disagrees with an existing claim, do NOT silently
overwrite. Add a `## Contradictions` section recording both views, who said what, and
which is more recent or authoritative. Flag it in the log entry too.

STUBS. If you reference something that warrants its own page but doesn't have one,
create a stub — frontmatter plus a one-line description. Better a stub than a
dangling link.

UNCERTAINTY. When a claim rests on thin evidence, say so in the page:
> [uncertain: only one source supports this — see [[sources/x]]]
Never guess to fill a gap. "I don't know" and "no source covers this" are correct
answers and belong in the wiki as readily as facts do.

PAGE SHAPE. Every page follows the layered structure in "# Page shape" below. That
section is not stylistic garnish — it is how I read, and a correct page in the wrong
shape is a page I can't use.


# Source pages

One source page per thing I read. This is not duplication of raw/ — it is the
citation layer and the join between a raw file and the wiki graph. Most raw files
aren't readable prose (transcripts, audio, PDFs, data), and some sources have no raw
file at all (a web page you read but never saved). Subject pages cite the source
page, never the raw file.

Every source page carries: a citation line (author/speaker, date, and either the
raw/ path or the URL), what kind of source it is, the date read, and an "entities
mentioned" list of wikilinks — that list is what wires the source into the graph.

TWO DEPTHS:
- FULL source page — for transcripts, audio, PDFs, web pages, data files, books.
  Summary, key takeaways, entities mentioned, notable quotes.
- THIN source page — when the raw file is ALREADY clean markdown prose (a note I
  wrote, a tight summary). Don't re-summarize what's already tight: frontmatter,
  citation, a link to the raw file, key takeaways, entities mentioned. Keep the
  citation target and the graph edges; skip the redundant prose.

Source pages layer like every other page: citation block, then one bold sentence
saying what this source is and why it matters, then `## The short version`, then the
detail. On a long transcript the layering matters most — I should be able to learn
what a two-hour meeting was about in fifteen seconds.


# Link conventions

These files are read through a local Markdown server that resolves [[wikilinks]] by
exact path first, then by walking up from the linking file's directory, then — only
if the target contains no slash — by filename across the whole index. Every rule
below follows from that resolution order.

- PREFIX links to foldered pages: [[people/jane-doe]], [[sources/some-talk-2026]],
  [[desk/outreach-plan]], [[desk/archived/old-plan]].
- NO PREFIX for subject pages at the wiki root: [[kubernetes]]. These resolve by
  walk-up and stay scoped to this brain.
  The convention is self-documenting: a prefix means a special kind of page; no
  prefix means an ordinary subject page.
- Matching is EXACT and CASE-SENSITIVE against the filename. [[Jane Doe]] does not
  find jane-doe.md. Always link the exact slug and pipe an alias for prose:
  [[people/jane-doe|Jane Doe]]. Without an alias the raw slug is what renders.
- FILENAMES MUST BE UNIQUE across the wiki. Two files with the same basename make a
  bare link silently resolve to the wrong one — no error, no broken-link marker.
- NO TRANSCLUSION. ![[page]] renders as a plain link, not an embed. Don't use it.
- Section anchors work: [[deploy-pipeline#Open questions]].
- NEVER MOVE OR RENAME A PAGE BY HAND. Moving a page breaks every prefixed inbound
  link. Always move with the plugin's `move` skill (`/second-brain:move`), whose
  script relocates the file and rewrites all inbound [[old/path]] references in
  the same pass.

CHAT ANSWERS ARE NOT WIKI PAGES. Wikilink syntax is for files. In a chat reply, write
names as plain text — "Jane Doe", not [[people/jane-doe]]. Mention a path only when
the point is where the page lives. The moment you're writing into a wiki page,
wikilinks are required again.


# index.md and log.md

index.md is CONTENT-ORIENTED — a catalog of every page: link, one-line summary,
optionally a date or source count. Group it by whatever categories actually fit this
domain, and regroup as the wiki grows; the index is where domain-specific structure
lives, not the folders. Update it on every ingest. On a query, read the index FIRST
to find relevant pages, then drill in. At a few hundred pages this works well and
avoids needing embedding-based retrieval.

The index is layered too: open it with a few lines on what this brain covers and
where to start — the three or four pages a newcomer (or I, after two months away)
should read first — before the full catalog. It is the top layer of the whole wiki,
so it has to be readable without scrolling.

log.md is CHRONOLOGICAL and append-only. Every entry starts with this header so
`grep "^## \[" wiki/log.md | tail -5` works:

  ## [YYYY-MM-DD] <op> | <title>

<op> is one of: ingest, query, lint, note. Body is 1-5 lines: what you did, what
changed, anything notable — contradictions, stubs created, follow-ups.


# Operations

The three operations are `/ingest`, `/query`, and `/lint`, plus `/move` for
relocating a page. Their full procedures are NOT written into this repo — they live
once, in the shared **`second-brain` plugin** (the folder this setup document lives
in), and every brain enables that plugin rather than carrying its own copy.

**Do NOT create `.claude/skills/` or `.claude/agents/` in this repo, and put nothing
in `.claude/commands/` except the pointer shims from "Your task" step 2.** Skills,
agents, and scripts used to be copied into every brain and the copies drifted apart;
consolidating them into the plugin was deliberate. The only other per-brain Claude
configuration is `.claude/settings.json`, which enables the plugin.

The specifications below are here so CLAUDE.md can say *what* each operation does,
and so you can tell when one has gone wrong. The procedures themselves come from the
plugin. Reference them in CLAUDE.md by their namespaced command names —
`/second-brain:ingest`, `/second-brain:query`, `/second-brain:lint`,
`/second-brain:move` — and name the `second-brain:wiki-researcher` subagent for
read-heavy queries.

## /ingest <path-or-url>
1. Read the source.
2. Discuss the key takeaways with me before writing anything.
3. Write the source page (full or thin, per the rule above).
4. Ripple the new information out to every affected page — a single source often
   touches 10-15 pages. Update existing pages; create stubs for new references.
5. Record contradictions rather than overwriting.
6. Update index.md.
7. Append an ingest entry to log.md.

## /query <question>
1. Read wiki/index.md first. Do not answer from memory.
2. Identify and read the relevant pages.
3. Answer with citations to the pages and sources you used.
4. Answer in layers, the same way pages are written: the direct answer in one or two
   sentences first, then the supporting detail, then caveats. Don't restage the
   derivation chain or list every page you consulted, and don't cite as decoration —
   cite claims that need backing.
5. The answer can take whatever form fits: prose, a comparison table, a diagram, a
   chart, a deck. If the answer is fundamentally about structure or sequence, draw
   it rather than describing it.
6. If the answer is worth keeping, offer to file it as a new page. Don't pre-write it
   into the reply. A comparison I asked for, an analysis, a connection I found —
   these should compound in the wiki like ingested sources do, not evaporate into
   chat history.

## /lint
A health check. Report findings grouped by severity, propose fixes, and only apply
them once I approve. Append a lint entry to log.md when done.

LINK INTEGRITY (mechanical — replicate the server's resolution order: exact path,
then walk-up from the linking directory, then basename fallback only when the target
has no slash):
  L1. Every wikilink resolves to an existing file.
  L2. Every UNPREFIXED link resolves to a file inside THIS brain. A bare link to a
      missing page can silently resolve into a sibling repo through the basename
      fallback — this check is what turns that back into a visible error.
  L3. No two files in the wiki share a basename.
  L4. Link form is correct: prefixed for people/, sources/, desk/, desk/archived/;
      bare for root subject pages.
  L5. No ![[transclusion]] syntax anywhere.
  L6. Every [[page#Section]] anchor points at a heading that exists.
  L7. Report broken links in log.md separately and informationally — it's
      append-only history and will legitimately reference renamed or never-created
      pages. Never rewrite log.md to fix them.

STRUCTURE:
  S1. Frontmatter is valid: required fields present, `kind` from the allowed set and
      present on subject pages only, dates well-formed, every slug in `sources:`
      exists, `derived_from:` present whenever `derived: true`. Flag any `type:`
      field — it means an agent reintroduced a folder-duplicating field.
  S2. No directories outside the specified structure. Flag any and stop — do not
      reorganize on your own.
  S3. Every page appears in index.md exactly once, and no index entry points at a
      page that no longer exists.
  S4. Pages over ~400 lines — propose a split.
  S5. assets/ contains no markdown; wiki/ page folders contain no binaries.

GRAPH:
  G1. Orphans — pages with no inbound link from any other page. index.md and log.md
      are exempt.
  G2. Missing pages — something named repeatedly across pages with no page of its
      own. Propose a stub.
  G3. Missing cross-references — page A mentions the title or a listed alias of
      page B in prose without linking it.

CONTENT:
  C1. Contradictions between pages that aren't recorded in a `## Contradictions`
      section.
  C2. Stale claims — a claim a newer source supersedes; compare a page's `updated:`
      against the newest source that touches it.
  C3. Non-trivial claims with no citation.
  C4. Derived drift — for every page with `derived: true`, re-derive it from
      `derived_from:` and report any divergence.
  C5. Desk hygiene — desk pages past their `expires:` date, or whose actions all read
      as complete. Propose moving them to desk/archived/ (with `/second-brain:move`,
      never by hand).

READABILITY (the layering rules in "# Page shape" — check these on every lint):
  R1. Every page opens with an H1 followed by one bold sentence saying what it is.
  R2. Every page over ~40 lines has a `## The short version` section, and that
      section actually summarizes the page rather than introducing it.
  R3. No paragraph over 4 lines. No section over ~40 lines without subheadings.
  R4. No bullet nested more than two deep.
  R5. Pages whose subject has a shape — a sequence, hierarchy, timeline, comparison,
      or relational structure — but no diagram. Propose one, and say which kind
      (Mermaid, draw.io, chart).
  R6. Diagrams that only restate the prose around them. Propose deleting.
  R7. Pages that have grown into walls of text since they were written. Propose a
      re-layer, NOT a trim — moving detail down a layer or out to a linked page,
      never cutting facts.

GAPS:
  X1. Questions the wiki raises but doesn't answer.
  X2. Sources worth acquiring, or facts worth a web search.
  X3. Good follow-up questions to investigate.


# Default behavior outside slash commands

- A substantive question is a /query. Read the index; don't answer from memory.
- A pasted link or a path under raw/ is a suggestion to /ingest, not a cue to
  answer off the top of your head.
- AMBIENT INGEST: any time I state a new fact in chat — a name, a date, a
  relationship, a correction, a preference — propagate it into the wiki
  immediately. Don't wait for an explicit /ingest. Apply it to the affected pages,
  cite the provenance inline as "(per conversation YYYY-MM-DD)", and append a `note`
  entry to log.md. If the fact is substantial — a story, a stance, a goal — suggest
  I save it as a note under raw/notes/<YYYY-MM-DD>-<topic>.md so the wiki has a
  stable artifact to cite, then ingest it normally. If it contradicts an existing
  claim, prefer the conversational fact (more recent, from me directly) but record
  both. Without this rule, everything learned in chat evaporates when the session
  ends.
- Never modify raw/.


# Page shape — layered, skimmable, concept first

I skim these pages. A wall of text is unusable to me even when every
sentence in it is correct. Present information in layers so I can stop at any depth
and still have something complete, and always give me the whole shape of a thing
before any of its detail.

CONCISE MEANS FEWER WORDS, NOT FEWER FACTS. Never drop a fact to shorten a page. Cut
preamble, throat-clearing, hedging, and restatement. When a section is genuinely too
long, push the detail DOWN a layer or OUT to a linked page — never delete it. The
wiki's whole value is that it accumulates; brevity that loses content defeats it.

THREE LAYERS, IN THIS ORDER, ON EVERY PAGE:

  Layer 1 — the H1, then ONE bold sentence saying what this is. If I read nothing
            else on the page, I know what the thing is and why it's in the wiki.

  Layer 2 — a `## The short version` section: 3-6 bullets carrying the whole page in
            summary, plus a diagram if the subject has a shape. Someone who stops
            here has the gist and can act on it. Required on any page over ~40 lines.
            On a shorter page, the page IS the short version.

  Layer 3 — the detail sections, each under a heading that states its point.

Use these exact section names. Predictability is the point — I should always know
where to look without reading.

WRITING RULES:
- Answer first, context second. Never build up to a conclusion.
- Headings state the finding, not the topic: "Deploy has no progress feedback", not
  "Deploy".
- No paragraph longer than 4 lines. If it's longer, it wants to be a bullet list.
- One idea per bullet. Bold the load-bearing term so the page scans.
- Bullets nest at most two deep.
- A table whenever two or more things are being compared.
- Specifics over generalities: numbers, dates, names, exact quotes with citations.
- No preamble, no "in this section we will", no restating my question back to me.
- One page, one subject. Over ~400 lines, split it.

DIAGRAMS — USE THEM. A diagram is the fastest layer-2 device there is. When a subject
has a shape, draw the shape instead of describing it in prose.

Reach for one whenever a page involves a sequence or pipeline, a hierarchy or org
structure, a timeline, a family tree, a state machine, two architectures being
compared, a route, or anything where what-connects-to-what is the actual content.

- Mermaid, in a fenced ```mermaid block, is the default. It renders natively and
  versions as plain text.
- draw.io — a .drawio file in assets/, referenced by relative markdown link — for
  what Mermaid can't express: dense architecture diagrams, layered stacks, anything
  needing real layout control.
- Charts (matplotlib, PNG into assets/) when the point is quantitative.
- One-line caption above every diagram saying what it shows.
- If a `mermaid-style` or `drawio-diagram` skill is available, use it so diagrams
  come out in my house style.
- Don't decorate. A diagram has to carry weight prose can't. If it only restates the
  bullets above it, delete it.


# Notes for later — do not act on these now

- Revisit the structure past roughly 200 pages. If it needs splitting then, split by
  DOMAIN (finance/, homelab/, travel/), never by page type. Queries are
  domain-scoped; page type has never been a useful retrieval axis.
- Keep this repo out of any file-sync client. Sync clients fight git and weaken the
  immutability guarantee on raw/.


# Your task

**Where the plugin comes from.** The `second-brain` plugin ships in the `ai-plugins`
marketplace (GitHub: `nvkris123/ai-plugins`). This setup document lives inside it,
at `plugins/second-brain/` — so the marketplace root is two folders up from this
file. Below, `<marketplace-path>` means that folder's absolute path.

1. If this repo already has content in a different layout, do NOT migrate it
   silently. Report what's there and what would have to move, and ask me first.

2. **Check that the shared plugin is wired up**, and fix it if not. Read
   `.claude/settings.json` and confirm it has both keys:

   ```json
   {
     "extraKnownMarketplaces": {
       "ai-plugins": {
         "source": { "source": "github", "repo": "nvkris123/ai-plugins" }
       }
     },
     "enabledPlugins": { "second-brain@ai-plugins": true }
   }
   ```

   The `ai-plugins` source may instead be `{"source": "directory", "path":
   "<marketplace-path>"}` when I edit the plugin from a local clone — either is
   correct. An old `second-brain@second-brain` entry, or a `second-brain`
   marketplace pointing at `open-code/second-brain`, is stale: report it.

   `enabledPlugins` alone works on this machine but leans on user-level
   registration; `extraKnownMarketplaces` is what makes a fresh clone resolve the
   plugin on its own. If either key is missing, don't hand-edit the JSON — tell me
   to run these two from this folder, which write both keys correctly:

   ```bash
   claude plugin marketplace add nvkris123/ai-plugins --scope project
   claude plugin install second-brain@ai-plugins --scope project
   ```

   Then verify no stale local copies exist: if `.claude/skills/` or
   `.claude/agents/` contain ingest/query/lint/move or wiki-researcher, or the brain
   root has its own `move-page.py`, report them — they shadow or duplicate the
   plugin and must be deleted, not maintained. Brain-specific skills that do
   something else are fine to keep.

   **Write the four command shims** into `.claude/commands/` — `ingest.md`,
   `query.md`, `lint.md`, `move.md` — so I can type `/ingest` instead of
   `/second-brain:ingest`. Plugin commands are always namespaced and there's no
   aliasing mechanism, so a local shim is the only way to get the short form. Each
   is three lines and contains **no procedure**, only a pointer, so it can't drift
   from the skill the way a copied SKILL.md would:

   ```markdown
   ---
   description: Process a new source into the wiki — read it, discuss takeaways, write a source page, ripple updates, log.
   argument-hint: <path-or-url>
   ---

   Invoke the `second-brain:ingest` skill and follow its procedure for this source: $ARGUMENTS

   If `$ARGUMENTS` is empty, ask the user for a path under `raw/` or a URL.
   ```

   Do the same for `query` (argument-hint `<question>`), `lint` (no argument
   hint), and `move` (argument-hint `<old-path> <new-path>`). If you ever find yourself pasting a *procedure* into one of these, stop —
   that belongs in the plugin.

3. Ask me about anything above that's genuinely underspecified for this domain —
   especially what this brain is FOR, since that shapes the index categories.

4. Then write CLAUDE.md implementing everything in this document: the three layers,
   the exact directory structure with the reasoning for why those folders and no
   others, the filing questions, frontmatter schema, source-page rules, link
   conventions, index and log formats, the operations **as provided by the
   `second-brain` plugin** (never as local skill files), ambient ingest, and the
   page-shape rules.

   Write CLAUDE.md in the same layered style it prescribes — it is the page I will
   reread most often, and a schema I can't skim is a schema that won't be followed.

5. **Create the skeleton yourself** — don't make me do it by hand. If they don't
   already exist, create:

   - `raw/` — plus an empty `raw/.gitkeep`, since git won't track an empty directory
     and this one starts empty.
   - `wiki/` with `index.md` and `log.md`.

   Give `index.md` its "start here" opening — a few lines on what this brain covers
   and which pages to read first — even if the catalog below it is empty for now.
   Give `log.md` an `## [YYYY-MM-DD] note | brain created` entry recording what we
   decided in step 3.

   Do not create any other directory. `people/`, `sources/`, and `desk/` appear the
   first time a page actually belongs in one.

Write CLAUDE.md for a reader who has never seen this document — it has to stand on
its own, because it's the only thing you'll read on future runs.
