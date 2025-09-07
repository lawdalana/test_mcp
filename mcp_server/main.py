"""MCP server exposing calculator, search, and parity tools."""

from __future__ import annotations

import operator
from typing import List

from mcp import types
from mcp.server.fastmcp import FastMCP, tools


# In-memory data used by the search tool
DATASET = {
    "langchain": "LangChain is a framework for building applications with LLMs.",
    "langgraph": "LangGraph helps orchestrate chains and graphs of LLM calls.",
    "python": "Python is a versatile programming language.",
}

OPERATIONS = {
    "add": operator.add,
    "sub": operator.sub,
    "mul": operator.mul,
    "div": operator.truediv,
}


def calculate(a: float, b: float, operation: str) -> List[types.TextContent]:
    """Perform a basic arithmetic operation and return the result."""

    op_func = OPERATIONS.get(operation)
    if op_func is None:
        raise ValueError("Unsupported operation")
    result = op_func(a, b)
    return [types.TextContent(type="text", text=str(result))]


def search(query: str) -> List[types.TextContent]:
    """Return matching descriptions from the dataset."""

    q = query.lower()
    results = [text for key, text in DATASET.items() if q in key]
    return [types.TextContent(type="text", text=" | ".join(results))]


def is_even(number: int) -> List[types.TextContent]:
    """Determine whether the provided number is even."""

    return [types.TextContent(type="text", text=str(number % 2 == 0))]


server = FastMCP(
    name="Example MCP Server",
    tools=[
        tools.Tool.from_function(calculate),
        tools.Tool.from_function(search),
        tools.Tool.from_function(is_even),
    ],
)


if __name__ == "__main__":
    server.run("streamable-http")

