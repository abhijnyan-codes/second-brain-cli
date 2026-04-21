# 🧠 Second Brain CLI

A personal knowledge base for developers, entirely in the terminal.  
Save notes, links, and code snippets — retrieve them in seconds.

---

## Why

You constantly find useful things while coding, studying, or browsing.  
You forget them. This tool fixes that — without leaving your terminal.

---

## Install

```bash
git clone https://github.com/abhijnyan-codes/second-brain-cli
cd second-brain-cli
pip install -e .
```

## Usage

```bash
# Add a note
brain add "always use debounce on search inputs" --tag js,frontend

# Add a link
brain add "https://github.com/charmbracelet/bubbletea" --tag go,tui

# Add a snippet
brain add "git reset --hard HEAD~1" --type snippet --tag git

# List all entries
brain list-all

# Search by keyword
brain search "debounce"

# Search by tag
brain search --tag git

# Search today's entries
brain search --today

# Delete an entry
brain delete 1
```

---

## Features

- Save notes, links, snippets
- Tag everything
- Fuzzy keyword search
- Filter by tag, type, date
- Fully offline — stored in `~/.second-brain/brain.db`
- No cloud, no account, no tracking

---

## Roadmap

- [ ] `brain edit <id>` — edit entry in $EDITOR
- [ ] `brain export` — export to markdown/json
- [ ] `brain today` — show today's entries
- [ ] fzf interactive search
- [ ] Shell autocomplete

---

## Contributing

PRs welcome. Open an issue first for big changes.

---

## License

MIT