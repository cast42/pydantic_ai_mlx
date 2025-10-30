"""Application entry point for running the MLX-backed Spanish tutor agent."""

from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING, Final, cast

import logfire
from mlx_lm import load
from pydantic_ai import Agent
from pydantic_ai.models.outlines import OutlinesModel
from pydantic_ai.settings import ModelSettings

if TYPE_CHECKING:
    from mlx.nn.layers.base import Module as MlxModule
    from transformers import PreTrainedTokenizerBase

MLX_MODEL_ENV: Final = "MLX_MODEL"
DEFAULT_MODEL_ID: Final = "mlx-community/Qwen3-4B-Thinking-2507-4bit"
DEFAULT_USER_INPUT: Final = "oh hey how are you?"
MAX_TOKENS: Final = 2048

logfire.configure(send_to_logfire="if-token-present")
logfire.instrument_pydantic_ai()

_agent: Agent[None, str] | None = None


def build_agent(model_id: str) -> Agent[None, str]:
    """Construct a Pydantic AI agent backed by an Outlines MLX model."""

    load_result = load(
        model_id,
        tokenizer_config={"eos_token": "<|endoftext|>", "trust_remote_code": True},
        return_config=True,
    )
    model, tokenizer, _config = cast(
        "tuple[MlxModule, PreTrainedTokenizerBase, dict[str, object]]",
        load_result,
    )
    mlx_model = OutlinesModel.from_mlxlm(model, tokenizer)
    return Agent(
        mlx_model,
        system_prompt="You are a Spanish tutor. Help the user learn Spanish. ONLY respond in Spanish.",
        output_type=str,
    )


def get_agent() -> Agent[None, str]:
    """Return a cached agent instance, creating it on first use."""
    global _agent
    if _agent is None:
        model_id = os.environ.get(MLX_MODEL_ENV, DEFAULT_MODEL_ID)
        _agent = build_agent(model_id)
    return _agent


async def main(user_input: str = DEFAULT_USER_INPUT) -> None:
    """Run the Spanish tutor agent once and print the response."""
    agent = get_agent()
    with logfire.span("Spanish tutor session"):
        logfire.info("Starting agent run", user_input=user_input)
        result = await agent.run(
            user_input,
            model_settings=ModelSettings(extra_body={"max_tokens": MAX_TOKENS}),
        )
        logfire.info("Agent response received", output=result.output)
        thinking, answer = result.output.split("</think>", 1)
        print("Thinking Process:\n", thinking.strip())
        print("Final Answer:\n", answer.strip())


if __name__ == "__main__":
    asyncio.run(main())
