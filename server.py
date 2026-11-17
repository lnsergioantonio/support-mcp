from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Support AI")

@mcp.tool()
def get_order_status(order_id: str) -> dict:
    """Get the status of an order."""

    orders = {
        "123": "Shipped",
        "456": "Processing",
        "789": "Delivered"
    }

    status = orders.get(order_id)

    if status is None:
        return {"error": "Order not found"}

    return {
        "order_id": order_id,
        "status": status
    }


if __name__ == "__main__":
    mcp.run()
