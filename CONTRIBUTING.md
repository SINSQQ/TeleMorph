# Contributing to TeleMorph

First off — thanks for taking the time to contribute! 🦋

The following is a set of guidelines for contributing to **TeleMorph**. These are mostly suggestions, not rules. Use your best judgement and feel free to propose changes by opening an issue.

## 🧭 Code of Conduct

By participating, you agree to keep the conversation respectful and constructive. We follow the [Contributor Covenant](https://www.contributor-covenant.org/).

## 🐞 Reporting bugs

- Open a [GitHub issue](https://github.com/telemorph/telemorph/issues/new).
- Include a **minimal** reproducer.
- Tell us your Python version, OS, and which optional extras you have installed.

## 💡 Suggesting features

Open an issue tagged `enhancement`. Describe:
1. The problem you're trying to solve.
2. The proposed API (code samples are very welcome).
3. Any alternatives you considered.

## 🔧 Development setup

```bash
git clone https://github.com/telemorph/telemorph.git
cd telemorph
python -m venv .venv
source .venv/bin/activate
pip install -e ".[all,dev]"
pre-commit install
```

## 🧪 Running tests

```bash
pytest
pytest --cov=telemorph
```

## ✨ Style guide

- **Python 3.9+** syntax — no walrus operators below 3.8.
- **Formatter**: `black` (line length 100).
- **Linter**: `ruff`.
- **Types**: `mypy --strict`.
- **Docstrings**: Google-style.
- **Commits**: follow [Conventional Commits](https://www.conventionalcommits.org/).

## 🔀 Pull request flow

1. Fork the repo and create your branch from `main`.
2. If you've added code, add tests.
3. Make sure `pytest`, `ruff`, `black --check`, and `mypy` all pass.
4. Update the **CHANGELOG.md** under `[Unreleased]`.
5. Open the PR — fill in the template.

## 📦 Releasing (maintainers only)

```bash
bump2version patch   # or minor / major
git push --tags
python -m build
twine upload dist/*
```

That's it — happy hacking! 🚀