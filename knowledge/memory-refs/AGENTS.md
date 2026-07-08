# memory-refs/

Pointers into your long-term / cross-session memory. A memory-ref node is a *thin index card*: a short, stable summary of a durable fact or preference, plus a link to wherever the full detail lives. The point is fast recall — these are what you scan to remember "what do I already know about X?"

## What goes here

- One-line summaries of durable facts, preferences, and learnings
- Pointers to the fuller note, file, or external memory store
- Stable identity / context facts you want surfaced early in a session

## Node anatomy

```yaml
---
type: memory-ref
tags: [type/memory-ref]
updated: YYYY-MM-DD
---
```

Body shape — keep it tiny:

```markdown
# <Short Label>

One or two lines: the durable fact or preference.

→ Full detail: [[full-note]] or `path/to/source`
```

## How entities link

- Each memory-ref points *out* to the canonical node that holds the detail.
- Avoid duplicating content here — if it grows past a couple of lines, it belongs in a real node and this becomes just the pointer.

## Discipline

- Thin by design. A memory-ref that turns into an essay has outgrown the directory.
- Update the one-liner when the underlying fact changes; don't accumulate stale cards.

## When to read

- At session start, to reload durable context cheaply.
- Before asking the user something you may have already recorded.
