# Contributing to second-brain-cli

Thanks for your interest in contributing!

## Setup

```bash
git clone https://github.com/abhijnyan-codes/second-brain-cli
cd second-brain-cli
pip install -e .
```

## How to contribute

1. Fork the repo
2. Create a branch: `git checkout -b feat/your-feature`
3. Make your changes
4. Test locally: `brain --help`
5. Commit: `git commit -m "feat: your feature"`
6. Push: `git push origin feat/your-feature`
7. Open a Pull Request

## Good first issues

- `brain show <id>` — view a single entry in full
- `brain tag list` — show all unique tags
- fzf interactive search
- Shell autocomplete
- `brain count` — show total entries count

## Guidelines

- Keep code simple and minimal
- Test your changes before submitting
- One feature per PR