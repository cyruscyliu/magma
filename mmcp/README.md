# Magma MCP Server

This directory contains the Magma MCP server. It exposes tools and resources
that let MCP clients inspect targets, fuzzers, bugs, build images, run
campaigns, and fetch results.

**Requirements**
1. Python 3.10+
2. Install dependencies:

```bash
pip install -r mmcp/requirements.txt
```

## Usage

Run the server over HTTP and test it with the FastMCP CLI.

1. **Start the HTTP server** (change the port if `8000` is in use):

```bash
PYTHONPATH=. fastmcp run mmcp/server.py --transport http --host 0.0.0.0 --port 8000 --path /mcp/
```

2. **Test as a client (HTTP)**:

```bash
python3 mmcp/examples/http_client.py --url http://localhost:8000/mcp/ \
  --tool magma_list_targets --args '{}'
```
