# caveman

**Summary:** terse replies, no ceremony, keeping every technical fact. It is the skill that saves the most in the setup, because it attacks the model's output.

## What it does

Cuts everything that carries no information:

- **goes away:** greetings, "sure, I'll help", caveats, a closing summary repeating what was said, offers of extra help;
- **stays:** code, commands, paths, numbers with units, exact error messages, negations (not, never, only, except).

It has levels:

| Level | Command | Style |
|---|---|---|
| normal | `/caveman` | short sentences, full grammar |
| ultra | `/ultracave` | fragments, content only |
| mega | `/megacave` | maximum compression |

Some things always come out as normal text, even at the highest level: security warnings, confirmation before an irreversible action, any sentence with two possible meanings, and everything saved outside the chat (code, commits, documents).

## How it is triggered in my setup

**Always on, at the `ultracave` level.** The `caveman@caveman` plugin injects the mode through a hook at the start of each session and reinforces it on every message. That is why the skill is `user-invocable-only`: it is already active and does not need to take up space in the listing. `caveman-commit` is turned off (my commits follow my once-a-month rule).

The plugin's subagents (`caveman:cavecrew-*`) are **denied** in `permissions.deny`: they were called without my asking and returned weak results for my kind of work.

## When to use

- Always, in the terminal.

## When not to use

- Text for other people (the mode already turns itself off in those cases).
- When I am confused by an answer: then I ask for a normal explanation.

## Token cost

- Fixed cost: the mode text injected by the hook each session (a few hundred tokens), which stays in the cache.
- Savings: the project itself says output drops by 40 to 60%. I have not measured it in my use. Output is the most expensive token, so the trade pays off.

## Why it is in the setup

**Discarded alternatives:**
- `Kulaxyz/token-diet`: does the same and adds other rules (read little, test little) that I already cover with ponytail and the hooks. It would overlap.
- Just a "be brief" rule in CLAUDE.md: the model forgets after a few replies. The hook reinforces it on every message.

## How to tell it is working

- Replies get straight to the point, with no opening or closing.
- Commands, paths and errors appear exactly.
