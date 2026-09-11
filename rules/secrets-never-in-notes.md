---
type: rule
status: hard
escalated_from: a promise made to the person in the package (README "Where your data lives",
  docs/en/presentation.md "What about passwords?") that had no rule behind it — and a neighbouring
  rule (local-only-repo.md) that tells the agent NOT to raise credential findings, which reads
  as permission to write them down. This rule closes that gap.
---

# HARD RULE: the person's passwords and codes never land in their files

## The rule

A password, PIN, key, token, card number, CVV, SMS code, wallet seed phrase, passport number —
**is never carried into any file in the folder**, even if the person dictated it in conversation
themselves and even if they asked you to "write it down".

Applies everywhere, no exceptions:

- the record of a conversation (`/session-save`, `daily/`, `state/`);
- verbatim stories (`memory/svoboda/{id}/stories/`) and domain cards;
- anything the person dropped into `inbox/` (a screenshot, an export, a chat log);
- `knowledge/`, `reports/`, commits.

## What to do instead

1. Don't write it down. Only the fact without the secret goes into the file: "has access to the
   bank", "keeps the wallet key offline" — without the value itself.
2. Say it in one plain line, no lecture and no repeats, in the person's language:
   > I don't write down passwords and codes — that line won't be in the files.
3. If you see a secret in a file that already exists (the person typed it in themselves) — don't
   silently rewrite the file: say in one line where it is and offer to remove it. They decide.

## Boundaries

- This rule is about **the person's data in their files**, not about auditing a repository.
  `rules/local-only-repo.md` and `rules/match-cost-to-scope.md` forbid inflating findings of the
  "there's a token in the repo → rotate it, rewrite history" kind — they still stand and do not
  contradict this rule: that is about infrastructure, this is about other people's passwords, which
  there is no reason to keep at all.
- No security lecture on top: one line, then back to the work.
