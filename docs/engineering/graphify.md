# graphify

**Summary:** builds a graph of the code (files, functions, imports, calls) in `graphify-out/`. In my setup it is used only to locate files.

## What it does

It statically analyzes the code and generates a graph: nodes are files and functions, edges are imports and calls. With the graph ready, I can ask "who calls this function?" or "which files depend on this module?" without opening files one by one.

The output lives in `graphify-out/` inside the project. The skill's references load only in the step that asks for them.

## How it is triggered in my setup

**Only with `/graphify`** (`user-invocable-only`). The rule in the global CLAUDE.md is explicit: "graphify only locates files". After finding the file, I read by range or with grep.

## When to use

- A large repository, where I do not know where a function is or who depends on it.
- Before a refactor that spans several files, to gauge the size of the impact.

## When not to use

- To understand the code: reading the whole graph costs more than a precise grep.
- A small repository, where a grep is enough.

## Token cost

- In the listing: zero (hidden).
- When called: ~5.3 KB (about 1,300 tokens). The graph itself can be large; that is why I query only the needed slice.

## Why it is in the setup and why limited

In a large repository, finding the right file on the first try saves several wrong reads. But the graph becomes a trap if the model tries to read all of it "to understand the architecture". Limiting use to locating keeps the gain and cuts the risk.

## How to tell it is working

- The answer uses the graph to point to a file and line, then reads only that excerpt.
