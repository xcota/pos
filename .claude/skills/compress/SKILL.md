---
name: compress
description: "Use when context is 50%+ full and needs compression, or when asked to compress text."
version: 1.0
user_invocable: true
---

# InfoCompressor — Context Compression

Compress text/context to ~30% of the original. Apply ALL 5 techniques simultaneously.

## Techniques

### 1. Structural
- Prose → tables (when data has patterns)
- Paragraphs → bullet points (3-7 words each)
- Nested → flat with `→` for hierarchy

### 2. Linguistic
- Kill filler: "it should be noted that" → cut
- Kill hedging: "perhaps", "it seems" → cut
- Active voice: "was done by X" → "X did"
- Imperative mood: "you should run" → "run"
- Present tense everywhere
- Drop articles where meaning is clear

### 3. Symbolic
- `→` causality ("X causes Y" → "X → Y")
- `|` alternatives ("either A or B" → "A | B")
- `+` additions
- `=` equivalence
- `✓/✗` yes/no
- `~` approximation

### 4. Abbreviation
Standard: cfg, env, srv, dir, repo, fn, arg, param, cmd, msg, req, res
**NEVER abbreviate:** file paths, entity names, error messages, URLs, numbers

### 5. Deduplication
- Each fact stated ONCE
- Merge related items into a single statement
- Remove repeated context from multiple messages

## Modes

### `/compress context`
Compress the current conversation. Output a compressed blob for a new session.
Steps: review the full conversation → extract goals/decisions/progress/pending/files → apply all techniques → output a <2KB blob → show the ratio.

### `/compress clipboard`
User pastes text. Return the compressed version.

### `/compress file <path>`
Read the file, compress, return.

## Quality Check
After compression verify:
- [ ] All file paths preserved exactly
- [ ] All numeric values preserved
- [ ] All entity/variable names preserved
- [ ] Meaning recoverable by someone who didn't read the original
- [ ] No ambiguity introduced by abbreviation

## Auto-Trigger (advisory)

Context-fill % isn't directly observable — gate on the token budget in `CLAUDE.md` instead. As the main thread approaches the **100K ceiling** (or `/session-save` is invoked) → compress first → handoff blob. When context is clearly heavy (near the ~150K session-save threshold) → compress + save immediately → REFUSE further execution → handoff blob.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Abbreviating file paths | NEVER — preserve exactly |
| Losing numeric values | Always keep numbers |
| Compressing without dedup first | Dedup THEN compress |
| Generic summary instead of compression | Compression preserves ALL facts, just shorter |
| Forgetting symbolic substitution | → \| ✓/✗ save 40%+ alone |
