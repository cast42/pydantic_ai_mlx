# Pydantic AI MLX

A minimal reference project that runs a [Pydantic AI](https://pydantic.dev/ai/)
agent on an Apple Silicon machine using [MLX](https://github.com/ml-explore/mlx)
and [Outlines](https://github.com/outlines-dev/outlines), with observability
provided by [Pydantic Logfire](https://pydantic.dev/logfire). The repository is
configured with `uv` for dependency management, `just` for repeatable commands,
and Ruff, Ty, and pytest for quality gates.

## Installation

### Clone the repo

Clone this repository:

```sh
git clone https://github.com/cast42/pydantic_ai_mlx.git
```

### Install uv

- Install `uv` following the upstream instructions: <https://docs.astral.sh/uv/getting-started/installation/>

## Initial setup of the project

Change directory into the project (replace the path if you cloned elsewhere):

```sh
cd pydantic_ai_mlx
```

### Optional: Logging with Logfire

Get your Logfire token, copy `.env.example` to `.env`, and provide a value for
`LOGFIRE_TOKEN`. The app calls `logfire.configure(send_to_logfire='if-token-present')`,
so nothing is sent to Logfire unless credentials are available.

### Install Just for command invocation

If `just` is not yet installed, install it (macOS example):

```sh
brew install just
```

## Test if everthing works

Check the code quality with Ruff and Ty by running `just check`:

```sh
> just check
uv run ruff check --fix 
All checks passed!
uv run ty check 
Checking ------------------------------------------------------------ 2/2
files
All checks passed!
```

Run the tests with `just test`:

```sh
> just test
uv run -m pytest -q 
.
1 passed in 0.01s
```

Run the Python entry point in `src/main.py`:

```sh
> just run
```

Since the justfile starts with `set dotenv-load`, the environment variables
defined in the `.env` file are loaded before the Python program is executed.
The program still runs without `LOGFIRE_TOKEN`, but it will only log locally.

You should see this output:

```sh
uv run python -m src.main
Thinking Process:
 <think>Estoy pensando...</think>
Final Answer:
 ¡Listo!
```

### Build documentation

Generate the static site with MkDocs:

```sh
just docs
```

The rendered site is written to the `site/` directory.

### View documentation for `src/main.py`

After running `just docs` (or `uv run mkdocs serve` for live reload), open `site/index.html` in a browser. The landing page includes an *Application Entry Point (`src/main.py`)* section that explains how the module configures Logfire and what `main()` does. This keeps the narrative documentation aligned with the implementation in `src/main.py`.

## Available recipies in the just file

```sh
> just
Available recipes:
    run

    [docs]
    docs *args

    [lifecycle]
    clean        # Remove temporary files
    install      # Ensure project virtualenv is up to date
    update       # Update dependencies

    [qa]
    check *args
    lint *args
    test *args
    typing *args
```

# Test the MLX model from the command line

To explore the `mlx_lm` CLI:

```sh
 uv run mlx_lm.generate --help
 ```

For Qwen models add an extra EOS token and enable `trust-remote-code` on the tokenizer:

```sh
uv run mlx_lm.generate --model mlx-community/Qwen3-4B-Thinking-2507-4bit --prompt "oh hey how are you?" --system-prompt "You are a Spanish tutor. Help the user learn Spanish. ONLY respond in Spanish." --max-tokens 2048 --extra-eos-token "<|endoftext|>" --trust-remote-code
```
