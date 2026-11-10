---
name: graphify
description: "Use for code/architecture questions if graphify-out/ exists, or /graphify."
---

# Graphify

Code knowledge graph. Maps relationships between files, functions, imports.

## Trigger

`/graphify` or a `graphify-out/` folder exists in the project.

## When to reach for it

- Understanding a large codebase
- Finding hidden dependencies
- Cross-file refactoring
- Documenting architecture

## What it does

Runs static analysis and generates a graph in `graphify-out/`. Nodes = files/functions, edges = imports/calls.

## Common questions

**Q: Does it work in any language?**
Main ones: TS/JS, Python, Go, Rust, Java. Others: best-effort.

**Q: Does it update by itself?**
Re-run `/graphify` after big changes.

## It's working if

`graphify-out/graph.json` exists and has > 50 nodes.