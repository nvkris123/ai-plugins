#!/usr/bin/env python3
"""
Move or rename a wiki page and rewrite every inbound [[wikilink]] in the same pass.

    python3 move-page.py wiki/desk/outreach-plan.md wiki/desk/archived/outreach-plan.md
    python3 move-page.py ... --apply

Run it from the brain root (or anywhere inside the brain): the brain is the nearest
directory at or above the current one that contains wiki/.

Dry run by default. Resolves links the way the Markdown server does: exact path
(relative to wiki/), then walk-up from the linking file's directory, then — only
when the target has no slash — basename across the wiki. Any link that resolves to
the old file is rewritten to the new canonical form: bare slug for root pages,
prefixed path for foldered pages. Aliases (|...) and anchors (#...) are kept.
Relative ../assets links inside the moved page are re-pointed for its new depth.
wiki/log.md is append-only and is never rewritten. Uses `git mv` inside a repo.
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

def find_brain():
    for d in [Path.cwd().resolve(), *Path.cwd().resolve().parents]:
        if (d / "wiki").is_dir():
            return d
    sys.exit("error: no wiki/ directory at or above the current directory — run this from inside a brain")


BRAIN = WIKI = LOG = None  # set in main(), so --help works outside a brain
LINK = re.compile(r"(!?)\[\[([^\]|#]+)(#[^\]|]*)?(\|[^\]]*)?\]\]")
REL_LINK = re.compile(r"(\]\()(\.\.?/[^)\s]+)(\))")


def die(msg):
    sys.exit(f"error: {msg}")


def wiki_path(arg):
    p = (Path.cwd() / arg).resolve()
    try:
        p.relative_to(WIKI)
    except ValueError:
        die(f"{arg} is not under {WIKI}")
    if p.suffix != ".md":
        die(f"{arg} is not a .md page")
    return p


def all_pages():
    return [p for p in WIKI.rglob("*.md") if "assets" not in p.relative_to(WIKI).parts]


def resolve(target, linking_file, pages_by_rel, pages_by_base):
    t = target.strip()
    if t.endswith(".md"):
        t = t[:-3]
    if t in pages_by_rel:
        return pages_by_rel[t]
    d = linking_file.parent
    while True:
        cand = d / f"{t}.md"
        if cand.exists():
            return cand.resolve()
        if d == WIKI:
            break
        d = d.parent
    if "/" not in t:
        hits = pages_by_base.get(t, [])
        if hits:
            return hits[0]
    return None


def canonical(path):
    rel = path.relative_to(WIKI).with_suffix("").as_posix()
    return rel  # root pages have no slash, so this is already the bare slug


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("--apply", action="store_true", help="perform the move (default: dry run)")
    a = ap.parse_args()

    global BRAIN, WIKI, LOG
    BRAIN = find_brain()
    WIKI = BRAIN / "wiki"
    LOG = WIKI / "log.md"

    old, new = wiki_path(a.old), wiki_path(a.new)
    if not old.exists():
        die(f"{a.old} does not exist")
    if new.exists():
        die(f"{a.new} already exists")
    if old.resolve() in (LOG, WIKI / "index.md"):
        die("index.md and log.md never move")
    pages = all_pages()
    for p in pages:
        if p.resolve() != old.resolve() and p.stem == new.stem:
            die(f"basename '{new.stem}' already used by {p.relative_to(WIKI)} — filenames must be unique")

    pages_by_rel = {canonical(p.resolve()): p.resolve() for p in pages}
    pages_by_base = {}
    for p in pages:
        pages_by_base.setdefault(p.stem, []).append(p.resolve())

    new_target = canonical(new)
    edits = {}
    for page in pages:
        page = page.resolve()
        if page == LOG:
            continue
        text = page.read_text(encoding="utf-8")

        def sub(m):
            bang, target, anchor, alias = m.group(1), m.group(2), m.group(3) or "", m.group(4) or ""
            if resolve(target, page, pages_by_rel, pages_by_base) != old.resolve():
                return m.group(0)
            return f"{bang}[[{new_target}{anchor}{alias}]]"

        out = LINK.sub(sub, text)
        if page == old.resolve() and old.parent != new.parent:
            def rel(m):
                abs_target = (old.parent / m.group(2)).resolve()
                return f"{m.group(1)}{os.path.relpath(abs_target, new.parent)}{m.group(3)}"
            out = REL_LINK.sub(rel, out)
        if out != text:
            edits[page] = (text, out)

    print(f"move  {old.relative_to(BRAIN)} -> {new.relative_to(BRAIN)}")
    for page, (before, after) in edits.items():
        n = sum(1 for x, y in zip(before.splitlines(), after.splitlines()) if x != y)
        print(f"edit  {page.relative_to(BRAIN)}  ({n} line(s))")
    if not a.apply:
        print("dry run — rerun with --apply")
        return

    for page, (_, after) in edits.items():
        page.write_text(after, encoding="utf-8")
    new.parent.mkdir(parents=True, exist_ok=True)
    in_git = subprocess.run(["git", "-C", str(BRAIN), "rev-parse"], capture_output=True).returncode == 0
    tracked = in_git and subprocess.run(
        ["git", "-C", str(BRAIN), "ls-files", "--error-unmatch", str(old)], capture_output=True
    ).returncode == 0
    if tracked:
        subprocess.run(["git", "-C", str(BRAIN), "mv", str(old), str(new)], check=True)
    else:
        old.rename(new)
    for d in [old.parent, *old.parent.parents]:
        if d == WIKI or not d.is_relative_to(WIKI) or any(d.iterdir()):
            break
        d.rmdir()
    print("done")


if __name__ == "__main__":
    main()
