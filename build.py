from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"

CHAPTERS = [
    ("00-start-here", "Start Here",
     "What system design is, how to approach an interview, and the numbers worth knowing."),
    ("01-fundamentals", "Chapter 1: Fundamentals",
     "Networking, load balancing, caching, availability, scalability and storage."),
    ("02-databases", "Chapter 2: Databases",
     "How data is stored, queried, copied and split across machines."),
    ("03-architecture", "Chapter 3: Architecture and Communication",
     "How services are structured and how they talk to each other."),
    ("04-design-toolkit", "Chapter 4: Design Toolkit",
     "Reusable techniques for reliability, scale and observability."),
    ("05-infrastructure-and-security", "Chapter 5: Infrastructure and Security",
     "Recovery, containers, identity and encrypted connections."),
]

NAV_RE = re.compile(r"\n*<!-- nav:start -->.*?<!-- nav:end -->\n*", re.S)
LINK_RE = re.compile(r"\]\(([^)#\s]+\.md)\)")
FENCE_RE = re.compile(r"^\s*```")


def write(path: Path, text: str) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def slugify(title: str) -> str:
    s = title.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


def title_of(text: str) -> str:
    first = text.lstrip().splitlines()[0]
    assert first.startswith("# "), f"page must start with '# Title', got: {first!r}"
    return first[2:].strip()


def shift_headings(text: str, by: int) -> str:
    out, in_fence = [], False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
        elif not in_fence and re.match(r"^#{1,6} ", line):
            line = "#" * by + line
        out.append(line)
    return "\n".join(out)


def load_pages():
    pages = []
    for ci, (folder, _, _) in enumerate(CHAPTERS):
        for path in sorted((DOCS / folder).glob("*.md")):
            text = NAV_RE.sub("", path.read_text(encoding="utf-8")).strip() + "\n"
            title = title_of(text)
            pages.append(dict(path=path, chapter=ci, title=title, slug=slugify(title), text=text))
    return pages


def check_unique(pages):
    seen = {}
    for p in pages:
        assert p["slug"] not in seen, f"duplicate title slug: {p['slug']}"
        seen[p["slug"]] = p["path"]
    for _, name, _ in CHAPTERS:
        assert slugify(name) not in seen, f"chapter slug clashes with a page: {name}"
    return seen


def resolve(src: Path, target: str) -> Path:
    return Path(os.path.normpath(src.parent / target))


def to_anchor_links(page, by_path):
    def repl(m):
        dest = resolve(page["path"], m.group(1))
        assert dest in by_path, f"{page['path'].name}: broken link {m.group(1)}"
        return f"](#{by_path[dest]['slug']})"
    return LINK_RE.sub(repl, page["text"])


def write_nav(pages, by_path):
    for i, p in enumerate(pages):
        for m in LINK_RE.finditer(p["text"]):
            assert resolve(p["path"], m.group(1)) in by_path, f"{p['path'].name}: broken link {m.group(1)}"
        parts = []
        if i > 0:
            q = pages[i - 1]
            rel = os.path.relpath(q["path"], p["path"].parent).replace(os.sep, "/")
            parts.append(f"Previous: [{q['title']}]({rel})")
        if i < len(pages) - 1:
            q = pages[i + 1]
            rel = os.path.relpath(q["path"], p["path"].parent).replace(os.sep, "/")
            parts.append(f"Next: [{q['title']}]({rel})")
        parts.append("[All topics](../README.md)")
        nav = "\n\n<!-- nav:start -->\n---\n\n" + " | ".join(parts) + "\n<!-- nav:end -->\n"
        write(p["path"], p["text"].rstrip() + nav)


def build_docs_index(pages):
    lines = [
        "# Topics",
        "",
        "One page per idea. Read in order, or jump to what you need. The same content is available as a single file in the [main README](../README.md).",
        "",
    ]
    for ci, (folder, name, desc) in enumerate(CHAPTERS):
        lines += [f"## {name}", "", desc, ""]
        for p in (x for x in pages if x["chapter"] == ci):
            lines.append(f"- [{p['title']}]({folder}/{p['path'].name})")
        lines.append("")
    write(DOCS / "README.md", "\n".join(lines))


def build_readme(pages, by_path):
    out = [
        "# System Design",
        "",
        "Notes on how to design systems that handle a lot of users and data, written for learning and for system design interviews. Each topic is short, starts from the problem it solves, and says what it costs.",
        "",
        "There are two ways to read this. Everything is in this one file, so you can scroll or search it with your browser. If you prefer small pages, the same content is split into one file per topic under [docs/](docs/README.md).",
        "",
        "Diagrams are written in [Mermaid](https://mermaid.js.org/), which GitHub renders directly.",
        "",
        "## Table of contents",
        "",
    ]
    for ci, (_, name, _) in enumerate(CHAPTERS):
        out.append(f"- [{name}](#{slugify(name)})")
        for p in (x for x in pages if x["chapter"] == ci):
            out.append(f"  - [{p['title']}](#{p['slug']})")
    out.append("")
    for ci, (_, name, desc) in enumerate(CHAPTERS):
        out += ["", "---", "", f"## {name}", "", desc, ""]
        for p in (x for x in pages if x["chapter"] == ci):
            body = shift_headings(to_anchor_links(p, by_path), 2).strip()
            out += [body, ""]
    out += [
        "---",
        "",
        "## About this file",
        "",
        "This README is generated from the files in `docs/`. To change something, edit the page there and run `python build.py`. See [CONTRIBUTING.md](CONTRIBUTING.md).",
        "",
    ]
    write(ROOT / "README.md", "\n".join(out))


def main():
    pages = load_pages()
    check_unique(pages)
    by_path = {p["path"]: p for p in pages}
    build_readme(pages, by_path)
    build_docs_index(pages)
    write_nav(pages, by_path)
    print(f"built README.md and docs/README.md from {len(pages)} pages")


if __name__ == "__main__":
    main()