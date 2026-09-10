# business/

Commercial entities and the rules around them: companies, markets, pricing, offers, operational policies. Distinct from `projects/` — a project is *work you do*; a business node is a *commercial context* (a market, a company, a set of pricing rules).

## What goes here

- Company / market / segment nodes
- Operational rule sets (pricing, fulfillment, service policies)
- Offer and strategy frameworks you apply

## Node anatomy

```yaml
---
type: business
tags: [domain/<domain>, type/business]
updated: YYYY-MM-DD
---
```

Body shape:

```markdown
# <Entity Name>

One-line: what this is (company / market / rule set) and why it's tracked.

## Compiled Truth
_Current synthesis._
Key facts: stage, market, positioning, the rules in effect.

## Rules / Policies
The operational rules, if this is a rule node (pricing, discounts, service SLAs).

## Related
- [[person]] — who's involved
- [[project]] — the work behind it

## Evidence Timeline
_Append-only._
- YYYY-MM-DD: entity created — source
```

## How entities link

- Business nodes link to the [[person]] nodes attached to them (founders, contacts).
- They link to the [[project]] node that builds or runs them.
- Market nodes link to the company nodes operating in them.
- Rule nodes link to the business node they govern.

## When to read

- When making a pricing, offer, or operational decision.
- When preparing commercial materials.
- When applying a strategy framework to a new context.
