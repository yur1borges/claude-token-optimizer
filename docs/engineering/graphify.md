# Graphify

## What it does

Runs static analysis, generates graph in `graphify-out/`. Nodes = files/functions, edges = imports/calls.

## When to reach for it

- Understanding large codebase
- Finding hidden dependencies
- Cross-file refactoring
- Documenting architecture

## Common questions

**Does it work for any language?**
Main: TS/JS, Python, Go, Rust, Java. Others: best-effort.

**Does it update automatically?**
Re-run `/graphify` after major changes.

## It's working if

`graphify-out/graph.json` exists and has > 50 nodes.