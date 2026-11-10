# ui-ux-pro-max

**Summary:** the setup's default interface skill. A database of styles, palettes, fonts and usability rules, queried by search, for web, mobile and desktop.

## What it does

Instead of putting all the design knowledge in the skill text, it ships a **CSV database** (colors, fonts, icons, charts, page types, app interface, per-technology guides) and a search script. The model queries only what it needs for the screen at hand.

The flow:

1. **Analyze the request:** product type, audience, style, technology (React, Flutter, PyQt etc.).
2. **Generate a design system** for new pages or projects: palette, typography, spacing, components. It can save this as a master file with per-page exceptions, to keep consistency across sessions.
3. **Complementary searches** when it needs something specific: a chart type, a palette for an industry, a form pattern.
4. **Technology guide:** rules specific to the library in use.

The rules are ordered by priority: accessibility and contrast first, then touch targets, performance, layout, typography, animation, charts.

## How it is triggered in my setup

**Automatic.** The global CLAUDE.md says to call it on any interface work. The `design` agent also uses it.

## When to use

- Creating or reviewing a screen, page, component, dashboard.
- Fixing a contrast, alignment or visual hierarchy problem.
- Choosing colors, fonts and chart type for data.
- The interfaces of my PyQt desktop apps.

## When not to use

- Code without an interface (backend, calculation, script).
- A showcase web page where I want a more distinctive visual result: then I call `/taste-skill` or `/impeccable`.

## Token cost

- In the listing: one line.
- When called: ~15.6 KB of instructions (about 3,900 tokens). The database does **not** enter the context; only the results of each search, which are small.

## Why this one and not the others

I had three design skills (ui-ux-pro-max, impeccable and taste-skill), each with its own opinion on the same screen. With all three visible, the model sometimes loaded two and tried to satisfy both, spending double and producing a less coherent result.

I kept this one as the default because:

- **It covers desktop.** My programs are PyQt; the other two are web-focused.
- **It queries instead of dumping.** The knowledge stays in the database and only the searched excerpt enters. The others put everything in the skill text.
- **It starts with accessibility**, which is what breaks most in hastily built interfaces.

The other two stay installed, but only via `/name`.

## How to tell it is working

- The answer cites the palette, fonts and rules applied, coming from the search.
- The result passes the contrast criteria and has no elements too small to click.
- Different screens of the same app keep the same design system.
