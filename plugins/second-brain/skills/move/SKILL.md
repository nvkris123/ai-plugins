---
name: move
description: Move or rename a wiki page and rewrite every inbound [[wikilink]] in the same pass, using the bundled move-page.py. Invoke whenever a page has to change folder or filename — archiving a desk page, refiling a page into people/ or sources/, fixing a basename collision, renaming a slug — and whenever the user types `/move <old> <new>`. Never move a wiki page by hand.
---

# /move

**Relocate a page with `move-page.py` so no inbound link breaks. Never `mv` a wiki page by hand.**

## The short version

1. Work out the old and new paths, both under `wiki/` and ending in `.md`.
2. Dry run: `python3 <this skill's directory>/move-page.py <old> <new>` from the brain root.
3. Show the user the planned move and the pages it will edit.
4. On approval, rerun with `--apply`.
5. Update `wiki/index.md` if the page's entry changes, and append a `note` entry to `wiki/log.md`.

## Why a script

Prefixed links (`[[people/x]]`, `[[desk/y]]`) encode the folder, so moving a page by hand silently breaks every one of them. A bare link to a renamed page breaks too. The script resolves every link the same way the Markdown server does — exact path, then walk-up from the linking file, then basename only when the target has no slash — and rewrites each one that pointed at the old file.

## What the script does

- **Rewrites inbound links** to the new canonical form: bare slug for root pages, prefixed path for foldered pages. Aliases (`|...`) and anchors (`#...`) are kept.
- **Re-points relative links** (`../assets/...`) inside the moved page for its new depth.
- **Uses `git mv`** when the page is tracked, so history follows the file.
- **Removes folders** the move leaves empty.
- **Refuses** to move `index.md` or `log.md`, to overwrite an existing page, or to create a basename that another page already uses.
- **Never rewrites `wiki/log.md`.** It's append-only history; old links there are expected.

## Common moves

| Situation | Old → new |
|---|---|
| Desk page done or expired | `wiki/desk/x.md` → `wiki/desk/archived/x.md` |
| A root page turns out to be a human | `wiki/x.md` → `wiki/people/x.md` |
| Basename collision found by `/lint` (L3) | `wiki/x.md` → `wiki/x-<qualifier>.md` |

## After the move

- **index.md** — the script rewrites the link in it; check the entry's grouping and one-line summary still fit.
- **log.md** — append:

```markdown
## [YYYY-MM-DD] note | moved <old slug> -> <new slug>

- Why: <one line>
- Pages relinked: <N>
```
