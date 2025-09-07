"""Tests for the MCP server tools using an HTTP client session."""

from __future__ import annotations

import asyncio
from contextlib import suppress

import pytest
import pytest_asyncio
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mcp_server.main import server


@pytest_asyncio.fixture(scope="module")
async def running_server() -> None:
    """Start the MCP server in the background for tests."""

    task = asyncio.create_task(server.run_streamable_http_async())
    await asyncio.sleep(0.5)
    yield
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task


@pytest.mark.asyncio
async def test_calculate_addition(running_server: None) -> None:
    async with streamablehttp_client("http://127.0.0.1:8000/mcp") as (read, write, _):
        session = ClientSession(read, write)
        await session.initialize()
        res = await session.call_tool(
            "calculate", {"a": 1, "b": 2, "operation": "add"}
        )
        assert res.content[0].text == "3"


@pytest.mark.asyncio
async def test_is_even_true(running_server: None) -> None:
    async with streamablehttp_client("http://127.0.0.1:8000/mcp") as (read, write, _):
        session = ClientSession(read, write)
        await session.initialize()
        res = await session.call_tool("is_even", {"number": 4})
        assert res.content[0].text == "True"


@pytest.mark.asyncio
async def test_search_langchain(running_server: None) -> None:
    async with streamablehttp_client("http://127.0.0.1:8000/mcp") as (read, write, _):
        session = ClientSession(read, write)
        await session.initialize()
        res = await session.call_tool("search", {"query": "langchain"})
        assert "LangChain" in res.content[0].text

