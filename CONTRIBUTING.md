# Contributing to Camomile

English · [中文](CONTRIBUTING.zh.md)

Found a bug, have an idea, or want to fix something? This page says how, in a few minutes of reading. Camomile is made for people who do not write code, so one clear sentence helps as much as a working patch.

**Maintainer:** Cota. **Where we talk:** the Issues of the repository, on [GitHub](https://github.com/xcota/pos/issues) or on [Gitee](https://gitee.com/cotya/pos-starter/issues) — whichever opens for you. There is no other channel (no e-mail, no chat). Write in English, 中文 or Русский.

## Report a bug

Open an Issue (on GitHub pick "Bug report") and tell us:

- **Your computer:** Mac or Linux, and which version (on a Mac: Apple menu → About This Mac).
- **Claude Code version:** type `claude --version` in the command window.
- **Steps:** what you typed or clicked, in order, starting from opening the folder.
- **What you expected**, and **what you got instead**. Copy any error message exactly as it appears.
- Only if it is about search by meaning or saving: the output of `python3 --version` and `git --version`.

**Please do not attach your notes.** The folders with your records (`daily/`, `knowledge/`, `memory/`, `state/`, `reports/`, `inbox/`) and the files `HOME.md`, `MEMORY.md` and `context/identity.md` are personal, and an Issue is public. Describe the problem in your own words; if one line of a note really matters, swap the names and details for placeholders first.

## Suggest an improvement

Open an Issue (on GitHub pick "Feature request"). Start with the problem, not the solution: what you were doing, what got in your way, who else would run into it. Then your idea, if you have one.

An idea fits best when it keeps what the README promises:

- everything stays as plain files on the person's own disk — no accounts, no server of ours;
- nothing happens behind the person's back — the assistant asks first;
- everything can be asked for in plain words: no jargon, no commands the person must learn;
- Claude Code stays the only thing the person pays for.

An idea that breaks one of these can still be worth discussing — say why in the Issue.

## Send a pull request

For a typo or a small fix, go straight to a pull request. For anything bigger, open an Issue first, so we can agree on the direction before you spend your time.

1. Fork the repository, make your change on a branch, open the pull request against `main`.
2. **Keep it small:** one pull request, one change. Unrelated fixes go in separate pull requests.
3. **Everything the assistant itself reads is written in English:** `CLAUDE.md`, `AGENTS.md`, `.claude/` (skills and hooks), `rules/`, `context/`, `scripts/`, `modules/`, `_templates/`. The assistant answers in the person's own language by itself. `AGENTS.md` is a parallel instruction sheet for other AI programs, kept in step with `CLAUDE.md` by hand: if your change touches the rules in one, check the other.
4. **Texts meant for people come in three languages** — English, Chinese, Russian: `README.md`, `README.zh.md`, `docs/ru/README.md` and the `.md` files in `docs/en/`, `docs/zh/`, `docs/ru/`. If you change one language you do not have to translate it yourself, but say in the pull request which files now need the same change. Edit the `.md` only: the web pages in `docs/` (`.html`) are rebuilt by the maintainer.
5. **File names** use only `a-z`, `0-9`, `_` and `-` (see `rules/naming-convention.md`).
6. **Nothing personal:** no real notes, names, e-mail addresses or paths from your own computer — not in files, not in commit messages, not in screenshots.

Before you open the pull request, run these two checks from the root of the folder:

```bash
python3 scripts/vault_sensors.py
for f in .claude/hooks/*.sh; do bash -n "$f" || echo "syntax error: $f"; done
```

The first one only reports (its exit code is always 0), so read what it prints: run it before you start and again at the end, and make sure your change added nothing new. The second prints nothing when every hook parses; if you changed any other `.sh` file, check it with `bash -n` too.

**Where to send it:** GitHub, branch `main`. The Gitee repository is a mirror: its `master` branch is rebuilt from `main` every time the maintainer publishes, so a change merged on Gitee itself would be overwritten. You can still open a pull request on Gitee — the maintainer will carry an accepted change into `main` by hand.

The maintainer reviews pull requests when time allows, may ask for changes, and decides what is merged.

## License of your contribution

Camomile is licensed under [AGPL-3.0](LICENSE). Whatever you send is released under the same license. Please send only what you wrote yourself, or what you have the right to release under it.

## Where to talk

Issues are the one place — on [GitHub](https://github.com/xcota/pos/issues) or [Gitee](https://gitee.com/cotya/pos-starter/issues): bug reports, ideas, questions about using Camomile ([the guide](docs/en/guide.md) answers most of them) and questions about a pull request. The maintainer, Cota, answers when time allows; there is no promised reply time.
