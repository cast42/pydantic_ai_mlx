# Pydantic AI MLX

Welcome to the documentation for the **Pydantic AI MLX** sample project.
It demonstrates how to execute a local MLX model through Outlines, wire it into
a Pydantic AI agent, and observe the run with Pydantic Logfire.

## Overview

This project ships with:

- Dependency management via [uv](https://docs.astral.sh/uv/)
- Automation using [`just`](https://github.com/casey/just)
- Quality gates powered by Ruff, Ty, and pytest
- Structured logging delivered through [Pydantic Logfire](https://pydantic.dev/logfire)
- A `src/main.py` entry point that orchestrates the MLX-backed agent

## Getting Started

Use the `just` recipes to lint, type-check, test, and build project documentation:

```sh
just check   # lint + type-check
just test    # run the pytest suite
just docs    # build MkDocs documentation into the site/ directory
```

## Application Entry Point (`src/main.py`)

The application’s main module lives at `src/main.py`. It configures Logfire with
`send_to_logfire='if-token-present'`, creates an MLX-backed Outlines model,
wraps it with a Pydantic AI `Agent`, and runs the agent once with a sample prompt.
The console output mirrors the agent response, showing a “Thinking Process” block
followed by the final answer. Run `just run` (or `uv run python -m src.main`)
to exercise the entry point locally.
