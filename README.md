# Pydantic_ai MLX model logged by logfire

Small code example to get started.

## Installation

### Clone the repo

Clone this new repository:

```sh
git clone https://github.com/cast42/pydantic_ai_mlx.git
```

### Install uv if not already installed

- Install `uv` following the upstream instructions: <https://docs.astral.sh/uv/getting-started/installation/>

## Initial setup of the project

Change directory into the new cloned directory (Replace new-repo-from-template with the name of your repository):

```sh
cd pydantic_ai_mlx
```

### Optional: Logging with logfire

Get your logfire token, copy the .env.example to .env and fill in value for  LOGFIRE_TOKEN.
The app calls `logfire.configure(send_to_logfire='if-token-present')`, so nothing
is sent to Logfire unless you provide credentials.

### Install Just for command invocation

If `just` is not yet installed. install with (on osx)

```sh
brew install just
```

## Test if everthing works

Check the code quality with ruff and ty from Astral by running the command `just check`:

```sh
> just check
uv run ruff check --fix 
All checks passed!
uv run ty check 
Checking ------------------------------------------------------------ 2/2
files
All checks passed!
```

Test the code by issuing command `just test`:

```sh
> just test
uv run -m pytest -q 
.
1 passed in 0.01s
```

Run the python code in `src/main.py`:

```sh
> just run
```

Since the justfile starts with `set dotenv-load`, the environment variables defined in the `.env` file are loaded before
the python program is run. The python program will also run if the LOGFIRE environment variable is not set but no logging on pydantic endpoint will be done.

You should see this output:

```sh
uv run python -m src.main
15:12:23.707 application.startup
Hello from python-minimal-boilerplate!
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

# Test the mlx model from the commandline

To get commandline options for mlx_lm:

```sh
 uv run mlx_lm.generate --help
 ```

For Qwen models add extra eos-token and trust-remote-code option for the tokenizer.

```sh
uv run mlx_lm.generate --model mlx-community/Qwen3-4B-Thinking-2507-4bit --prompt "hoh hey how are you?"   --system-prompt "You are a Spanish tutor. Help the user learn Spanish. ONLY respond in Spanish." --max-tokens 2048 --extra-eos-token "<|endoftext|>"  --trust-remote-code
 ```
