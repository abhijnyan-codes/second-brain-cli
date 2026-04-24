# 🧠 second-brain-cli

> Your memory, but searchable.  
> A fast, minimal, terminal-first knowledge base for developers.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)

---

## ✨ Why this exists

You discover useful things while coding —  
commands, fixes, links, ideas.

Then you forget them.

**second-brain-cli makes sure you don’t.**

No browser. No clutter. Just your terminal.

---

## ⚡ Features

- 📝 Notes, links, and code snippets
- 🔍 Fuzzy search with scoring
- 🏷️ Tag-based filtering
- 📌 Pin important entries
- 📋 Copy to clipboard instantly
- 📅 Filter by date (`--today`)
- 📤 Export to Markdown / JSON
- 🤝 Share via GitHub Gist (short codes)
- 🔒 100% offline-first (SQLite)
- ⚡ Fast, minimal CLI experience

---

## 📦 Installation

```bash
pip install second-brain-cli
```

---

## 🚀 Quick Start

```bash
# Add a note
brain add "use debounce for search inputs" --tag js,frontend

# Add a link
brain add "https://github.com/charmbracelet/bubbletea" --tag go,tui --type link

# Add a snippet
brain add "git reset --hard HEAD~1" --tag git --type snippet

# Quick add
brain say "revise binary search"

# Search
brain search "debounce"
brain search --tag git

# View
brain list-all
brain today
```

---

## 🧩 Commands

### Add
```bash
brain add "content" --tag tags --type note|link|snippet --lang python
brain say "content"
```

### Retrieve
```bash
brain list-all
brain search "keyword" --tag tag --type note --today
brain today
```

### Manage
```bash
brain edit <id>
brain delete <id>
brain pin <id>
brain copy <id>
```

### Export
```bash
brain export --format markdown
brain export --format json
```

### Share
```bash
brain send <id1> <id2>
brain recv <code>
```

---

## 🔐 Setup (for sharing)

```bash
# Create GitHub token (gist scope)
https://github.com/settings/tokens

brain config --set github_token --value YOUR_TOKEN
```

---

## 🗂️ Storage

All data is stored locally:

```
~/.second-brain/brain.db
~/.second-brain/config.json
~/.second-brain/export.md
~/.second-brain/export.json
```

- SQLite database
- No cloud
- No tracking
- Full privacy

---

## 🧠 Philosophy

- Terminal-first
- Zero friction
- Developer-focused
- Privacy by default

---

## 🛣️ Roadmap

- [ ] `brain tui` — full terminal UI (Textual)
- [ ] `brain show <id>`
- [ ] Shell autocomplete
- [ ] Browser extension
- [ ] fzf interactive search

---

## 🤝 Contributing

Contributions are welcome!

```bash
# 1. Fork
# 2. Create branch
git checkout -b feat/your-feature

# 3. Commit
git commit -m "feat: your feature"

# 4. Push
git push origin feat/your-feature
```

Then open a Pull Request 🚀

---

## ⭐ Support

If you find this useful:
- Star the repo ⭐
- Share it with friends
- Suggest features

---

## 📄 License

MIT — free to use, modify, and distribute.

---

## 🔗 Links

- PyPI: https://pypi.org/project/second-brain-cli/
- GitHub: https://github.com/abhijnyan-codes/second-brain-cli
