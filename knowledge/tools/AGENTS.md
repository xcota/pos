# tools/

Tools, APIs, platforms, libraries, and infrastructure components you use. A tool node captures *a thing you operate* — how it works, how you call it, its quirks and gotchas — not the idea behind it (that's a concept) and not what you're building with it (that's a project).

## What goes here

- CLIs, libraries, services, APIs
- Platforms and infrastructure
- Recurring command recipes worth remembering

## Node anatomy

```yaml
---
type: tool
tags: [domain/<domain>, type/tool]
updated: YYYY-MM-DD
---
```

Body shape:

```markdown
# <Tool Name>

One-line: what it does and why you use it.

## How to use
Key commands, invocation, config that you keep forgetting.

## Gotchas
Known failure modes, quirks, version traps.

## Related
- [[concept]] — what this implements
- [[project]] — where it's used
```

## How entities link

- Tool nodes implement [[concept]] nodes.
- They are referenced *from* [[project]] nodes that depend on them.
- Tools connect to each other when one wraps or feeds another.

## When to read

- When debugging an infrastructure or integration issue.
- When evaluating alternatives before adopting something new.
- When you need the invocation recipe you wrote down last time.
