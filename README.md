# Support MCP Server

`support-mcp` is a Python Model Context Protocol (MCP) server that exposes
sample customer-support capabilities to an MCP-compatible AI client. It
provides order and customer lookups, order searching, refund-policy content,
and reusable prompts for drafting and analyzing support responses.

The project is intended as a simple local MCP server example. Customer and
order data are currently stored in memory, and order/todo details are fetched
from the public [JSONPlaceholder](https://jsonplaceholder.typicode.com/) API.

## Requirements

- Python 3.10 or newer
- Internet access for `get_order_status`, `get_todo_details`, and
  `test_api.py`
- An MCP-compatible client if you want to use the server interactively
- The pinned Python dependencies listed in [requirements.txt](requirements.txt)

## Installation

From the project directory, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the MCP server

Start the server directly with:

```bash
python server.py
```

The server communicates over MCP stdio, so it is normally launched by an MCP
client rather than accessed through a web browser. Keep the terminal process
running while the client is connected.

For an MCP client configuration, use the Python executable from the project’s
virtual environment and pass the absolute path to `server.py`. For example:

```json
{
  "mcpServers": {
    "support-mcp": {
      "command": "/absolute/path/to/support-mcp/.venv/bin/python",
      "args": ["/absolute/path/to/support-mcp/server.py"]
    }
  }
}
```

On Windows, use the equivalent `.venv\\Scripts\\python.exe` path.

## Available MCP capabilities

### Tools

- `get_order_status(order_id)` — Fetches a todo-like order record from
  JSONPlaceholder. `order_id` must be between 1 and 200.
- `get_customer_info(customer_id)` — Returns the in-memory record for customer
  `1` or `2`.
- `search_orders(customer_id, status=None, limit=10)` — Searches the sample
  order list. Allowed statuses are `Shipped`, `Processing`, and `Delivered`;
  `limit` must be between 1 and 50.
- `get_todo_details(todo_id)` — Fetches a todo from JSONPlaceholder. `todo_id`
  must be between 1 and 200.

### Resources

- `support://policies/refunds` — Refund policy text.
- `support://customers/{customer_id}` — Customer information for customer `1`
  or `2`.
- `support://orders/{order_id}` — Sample order information for orders `123`,
  `456`, or `789`.

### Prompts

- `draft_support_reply(customer_name, issue)` — Produces instructions for
  drafting an empathetic, professional support reply.
- `analyze_customer_complaint(customer_name, complaint_text, order_id=None)` —
  Produces a concise complaint analysis and suggested next steps.

## Test the external API connection

`test_api.py` makes a direct request to JSONPlaceholder and prints the returned
record:

```bash
python test_api.py
```

This is an API connectivity smoke test, not a complete automated test suite.

## Project files

```text
server.py         MCP server implementation
test_api.py       External API connectivity smoke test
requirements.txt  Pinned Python dependencies
```

## Troubleshooting

- If imports fail, activate `.venv` and reinstall with
  `python -m pip install -r requirements.txt`.
- If external lookups fail, verify internet access and that
  `https://jsonplaceholder.typicode.com/todos/1` is reachable.
- MCP clients must launch the server using the same Python environment where
  the dependencies were installed.
