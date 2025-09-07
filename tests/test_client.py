"""End-to-end tests for the LangChain MCP client."""

from __future__ import annotations

import asyncio
import importlib
import os
from contextlib import suppress
import sys

import pytest
import pytest_asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mcp_server.main import server


@pytest_asyncio.fixture(scope="module")
async def running_server() -> None:
    task = asyncio.create_task(server.run_streamable_http_async())
    await asyncio.sleep(0.5)
    yield
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task


@pytest.mark.asyncio
async def test_client_run_examples(running_server: None) -> None:
    os.environ["SERVER_URL"] = "http://127.0.0.1:8000/mcp"
    import mcp_client.main as client_main

    importlib.reload(client_main)

    calc, search, even = await client_main.run_examples()
    assert calc == 3.0
    assert "Python" in search
    assert even is True

