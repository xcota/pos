---
type: rule
status: hard
escalated_from: a verify-before-ship anti-pattern cluster (C4, sensory sub-axis) —
  promoted after the agent shipped artifacts judged by a sense it lacks directly
  (sight, sound, interaction) "blind" — off text, structure, or "it built OK" —
  and hit total rejection across several modalities with the same root and the
  same fix.
---

# HARD RULE: Don't ship a sensory artifact without perceiving it through a real proxy

## Principle

An artifact whose quality is judged by a **sense the agent doesn't have directly**
— sight (layout, rendering), sound (a mix, a preset), interaction (a click, an
input, a state change) — must not be shipped off assumptions. "It compiled", "the
server returned 200", "the structure looks right" are **blind** signals for these
domains. Before shipping, run the artifact through an available perception proxy
and actually look at / listen to / operate the output.

## The gate before ship

- **Visual** (a page, HTML, an image, a poster, slides, a diagram): render it and
  screenshot at the **target** viewport (mobile if the operator said mobile-first),
  in both light and dark, and check any interactive pieces. Iterate on the
  screenshots **before** delivering.
- **Interactive** (a dashboard, form, or widget — anything with click, input, or
  state): a static screenshot and an API test **do not** catch client behavior —
  scroll jumps, focus, post-click state. "Verified" means a real interaction ran
  in the live DOM (drive it programmatically, use a headless browser with a click
  script, or hand it to the operator to click). If a scripted proxy won't come up
  in your environment, **don't silently degrade to a static check** — find an
  interaction-capable path, or say plainly "I couldn't run the click". Render-verify
  is not use-verify.
- **Audio** (a track, a mix, a preset): use a spectrum/analysis tool or export it
  for the operator to hear in a loop — don't guess a melody, a mix, or a softness
  from "it should sound like…".
- **Any other sensory domain**: find a measurement or render proxy. Don't
  verbalize the output blind.

**The check:** "Is this artifact judged by eye or ear? → have I seen/heard the
actual output through a proxy?" If it has click/input/state, add: "did I run the
actual use-loop in a live DOM, not just the render?" If no — don't ship. "It built
/ compiled / 200 / the screenshot draws" ≠ "it looks and feels fine to use".

## Why it's a hard rule

The failure fired across three modalities — audio, visual, interaction — with one
root and one generalizable fix. The proxy (a screenshot, a spectrum, one live
click) is cheap; a public rejection is not. And a blind ship has twice hidden a
real bug the proxy would have surfaced immediately — so perceiving the output is
also how you catch the defect, not only the ugliness.

## Related

Sibling to the "don't iterate blind on what you can't perceive" and "verify your
own fixes end-to-end" corrections. Cluster C4.
