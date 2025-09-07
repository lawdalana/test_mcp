"""LangChain client that connects to the MCP server via MCPToolkit."""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any, Dict

from langgraph.graph import END, StateGraph
from langchain_mcp import MCPToolkit
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client


SERVER_URL = os.getenv("SERVER_URL", "http://mcp_server:8000/mcp")


async def build_graph() -> StateGraph:
    """Connect to the MCP server and build a LangGraph state graph."""

    async with streamablehttp_client(SERVER_URL) as (read, write, _):
        session = ClientSession(read, write)
        toolkit = MCPToolkit(session=session)
        await toolkit.initialize()
        tools = {tool.name: tool for tool in toolkit.get_tools()}

        graph = StateGraph(dict)

        async def calculator_node(state: Dict[str, Any]) -> Dict[str, Any]:
            content, _ = await tools["calculator"].ainvoke(
                a=state["a"], b=state["b"], operation=state["operation"]
            )
            result = json.loads(content)[0]["text"]
            return {"result": float(result)}

        async def search_node(state: Dict[str, Any]) -> Dict[str, Any]:
            content, _ = await tools["search"].ainvoke(query=state["query"])
            result = json.loads(content)[0]["text"]
            return {"result": result}

        async def is_even_node(state: Dict[str, Any]) -> Dict[str, Any]:
            content, _ = await tools["is_even"].ainvoke(number=state["number"])
            result = json.loads(content)[0]["text"] == "True"
            return {"result": result}

        graph.add_node("calculator", calculator_node)
        graph.add_node("search", search_node)
        graph.add_node("is_even", is_even_node)

        graph.add_node("router", lambda state: state)
        graph.set_entry_point("router")

        def route(state: Dict[str, Any]) -> str:
            return state["tool"]

        graph.add_conditional_edges(
            "router",
            route,
            {"calculator": "calculator", "search": "search", "is_even": "is_even"},
        )
        graph.add_edge("calculator", END)
        graph.add_edge("search", END)
        graph.add_edge("is_even", END)

        return graph


async def run_examples() -> tuple[float, str, bool]:
    """Run sample invocations of all tools and return their results."""

    graph = await build_graph()
    compiled = graph.compile()

    calc = (
        await compiled.ainvoke(
            {"tool": "calculator", "a": 1, "b": 2, "operation": "add"}
        )
    )["result"]
    search = (
        await compiled.ainvoke({"tool": "search", "query": "python"})
    )["result"]
    even = (
        await compiled.ainvoke({"tool": "is_even", "number": 2})
    )["result"]
    return float(calc), search, bool(even)


def main() -> None:
    calc, search, even = asyncio.run(run_examples())
    print("Calculator result:", calc)
    print("Search result:", search)
    print("Is even result:", even)


if __name__ == "__main__":
    main()

