# test_mcp

Example MCP server and client using LangChain and LangGraph.

## Features
- MCP server built with the official `mcp` python SDK exposing tools:
  - `calculator` – basic arithmetic (add, sub, mul, div)
  - `search` – query a tiny in-memory dataset
  - `is_even` – check if a number is even
- LangChain client using `MCPToolkit` and LangGraph to call the server.
- Docker and docker-compose configurations for running server and client.
- Unit and end-to-end tests for all tools and client integration.

## Change History
- Initial implementation of MCP server and client with tests and Docker setup.
- Switch server to use `mcp` python SDK and update client to `MCPToolkit`.

## Running Locally
```bash
# build and start the server and client
docker-compose up --build
```
The client executes sample tool calls on startup. The MCP endpoint is available at `http://localhost:8000/mcp`.

To run tests locally:
```bash
pip install -r mcp_server/requirements.txt -r mcp_client/requirements.txt
pip install pytest flake8
pytest
flake8
```

## Future Improvements
- Extend search tool with real search engine integration.
- Add authentication and rate limiting.
- Expose additional tools and more complex LangGraph workflows.
