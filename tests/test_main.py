"""Tests for the project's main module."""

from __future__ import annotations

import asyncio

from src import main as app_main


def test_main_runs_agent_and_displays_thinking(monkeypatch, capsys) -> None:
    """Ensure the async entry point logs, spans, and renders agent output."""
    info_calls: list[tuple[str, dict[str, object]]] = []

    def fake_info(event: str, **kwargs: object) -> None:
        info_calls.append((event, kwargs))

    monkeypatch.setattr(app_main.logfire, "info", fake_info)

    span_events: list[dict[str, object]] = []

    class FakeSpan:
        def __init__(self, name: str, **kwargs: object) -> None:
            span_events.append({"event": "created", "name": name, "kwargs": kwargs})

        def __enter__(self) -> "FakeSpan":
            span_events.append({"event": "entered"})
            return self

        def __exit__(self, exc_type, exc, tb) -> None:
            span_events.append({"event": "exited", "exc_type": exc_type})

    monkeypatch.setattr(app_main.logfire, "span", lambda name, **kwargs: FakeSpan(name, **kwargs))

    run_calls: list[tuple[str, dict[str, object]]] = []

    class FakeResult:
        def __init__(self, output: str) -> None:
            self.output = output

    class FakeAgent:
        async def run(self, prompt: str, *, model_settings) -> FakeResult:
            extra = getattr(model_settings, "extra_body", model_settings)
            if isinstance(extra, dict) and "extra_body" in extra:
                payload = extra["extra_body"]
            else:
                payload = extra
            run_calls.append((prompt, payload))
            return FakeResult("<think>Estoy pensando...</think>¡Listo!")

    monkeypatch.setattr(app_main, "get_agent", lambda: FakeAgent())
    monkeypatch.setattr(app_main, "_agent", None)

    user_input = "Hola, ¿qué tal?"
    asyncio.run(app_main.main(user_input=user_input))

    captured = capsys.readouterr()
    lines = captured.out.strip().splitlines()

    assert len(lines) == 4
    assert lines[0] == "Thinking Process:"
    assert lines[1].strip() == "<think>Estoy pensando..."
    assert lines[2] == "Final Answer:"
    assert lines[3].strip() == "¡Listo!"
    assert span_events == [
        {"event": "created", "name": "Spanish tutor session", "kwargs": {}},
        {"event": "entered"},
        {"event": "exited", "exc_type": None},
    ]
    assert run_calls == [(user_input, {"max_tokens": app_main.MAX_TOKENS})]
    assert info_calls == [
        ("Starting agent run", {"user_input": user_input}),
        ("Agent response received", {"output": "<think>Estoy pensando...</think>¡Listo!"}),
    ]
