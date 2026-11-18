import httpx
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("Support AI")


# Tool 1: String parameter
@mcp.tool()
def get_order_status(order_id: int) -> dict:
    """Get an order status from an external API."""

    if order_id <= 0 or order_id > 200:
        raise ToolError("Order ID must be between 1 and 200.")

    try:
        response = httpx.get(
            f"https://jsonplaceholder.typicode.com/todos/{order_id}",
            timeout=5.0
        )

        response.raise_for_status()

        data = response.json()

        if not data:
            raise ToolError("Order not found.")

        status = "Completed" if data["completed"] else "Pending"

        return {
            "order_id": data["id"],
            "title": data["title"],
            "status": status
        }

    except httpx.TimeoutException:
        raise ToolError("External API request timed out.")

    except httpx.HTTPStatusError as error:
        raise ToolError(
            f"External API returned HTTP {error.response.status_code}."
        )

    except httpx.RequestError:
        raise ToolError("Could not connect to the external API.")

# Tool 2: Integer parameter
@mcp.tool()
def get_customer_info(customer_id: int) -> dict:
    """Get customer information by customer ID."""

    customers = {
        1: {"name": "John", "email": "john@example.com"},
        2: {"name": "Mary", "email": "mary@example.com"}
    }

    customer = customers.get(customer_id)

    if customer is None:
        raise ToolError("Customer not found")

    return {
        "customer_id": customer_id,
        **customer
    }


# Tool 3: Multiple parameters
@mcp.tool()
def search_orders(
    customer_id: int,
    status: str | None = None,
    limit: int = 10
) -> dict:
    """Search orders by customer ID, optionally filtering by status."""

    if customer_id <= 0:
        raise ToolError("Customer ID must be a positive integer.")

    if limit <= 0 or limit > 50:
        raise ToolError("Limit must be a positive integer between 1 and 50.")

    if status is not None and status not in ["Shipped", "Processing", "Delivered"]:
        raise ToolError("Invalid status. Allowed values: Shipped, Processing, Delivered.")

    orders = [
        {"id": "123", "customer_id": 1, "status": "Shipped"},
        {"id": "456", "customer_id": 1, "status": "Processing"},
        {"id": "789", "customer_id": 2, "status": "Delivered"}
    ]

    results = [
        order for order in orders
        if order["customer_id"] == customer_id
        and (status is None or order["status"] == status)
    ]

    return {
        "orders": results[:limit],
        "total": len(results)
    }

@mcp.tool()
def get_todo_details(todo_id: int) -> dict:
    """Get details of a todo item from an external API."""

    if todo_id <= 0 or todo_id > 200:
        raise ToolError("Todo ID must be between 1 and 200.")

    try:
        response = httpx.get(
            f"https://jsonplaceholder.typicode.com/todos/{todo_id}",
            timeout=5.0
        )

        response.raise_for_status()

        data = response.json()

        return {
            "todo_id": data["id"],
            "title": data["title"],
            "completed": data["completed"],
            "user_id": data["userId"]
        }

    except httpx.TimeoutException:
        raise ToolError("External API request timed out.")

    except httpx.HTTPStatusError as error:
        raise ToolError(
            f"External API returned HTTP {error.response.status_code}."
        )

    except httpx.RequestError:
        raise ToolError("Could not connect to the external API.")

@mcp.resource("support://policies/refunds")
def get_refund_policy() -> str:
    """Company refund policy."""

    return """
    Refund Policy

    1. Customers can request a refund within 30 days.
    2. Products must be unused.
    3. Refund processing takes 5-7 business days.
    4. Shipping costs are non-refundable.
    """


customers = {
    "1": {
        "name": "John",
        "email": "john@example.com"
    },
    "2": {
        "name": "Mary",
        "email": "mary@example.com"
    }
}

@mcp.resource("support://customers/{customer_id}")
def get_customer_resource(customer_id: str) -> dict:
    """Get customer information."""

    customer = customers.get(customer_id)

    if customer is None:
        raise ToolError("Customer not found.")

    return customer

@mcp.resource("support://orders/{order_id}")
def get_order_status(order_id: str) -> dict:
    """Get order information."""

    orders = {
        "123": {"customer_id": 1, "status": "Shipped"},
        "456": {"customer_id": 1, "status": "Processing"},
        "789": {"customer_id": 2, "status": "Delivered"}
    }

    order = orders.get(order_id)

    if order is None:
        raise ToolError("Order not found.")

    return {
       "order_id": order_id,
        **order
    }

if __name__ == "__main__":
    mcp.run()
