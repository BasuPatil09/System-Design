# Contributing

Fixes are welcome, especially factual corrections.

The pages live in `docs/`, one file per topic. The top-level `README.md` is generated from them, so don't edit it by hand. Change the page, then run:

```bash
python build.py
```

That rebuilds `README.md`, the topic index in `docs/README.md`, and the previous/next links at the bottom of each page.

A few guidelines for new or edited pages:

- Start the file with `# Title`. Titles must be unique, since they become the links in the big README.
- Explain the problem first, then the idea, then what it costs. Plain sentences beat jargon.
- Use diagrams only where they help, written in Mermaid.
- Link to other pages with relative paths like `../02-databases/10-sharding.md`. The build turns them into anchors in the big README.
- Add new pages with a numeric prefix so they sort where you want them.
