from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name = "Calculator")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def sub(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b


@mcp.tool()
def multiplication(a: float, b: float) -> float:
    """
    Multiplies Numbers

    args: a (float): first number
          b (float): second number

    Returns:
        float: Result of the multiplication.
    """
    return a * b

@mcp.tool(
    name = "division",
    description = "Divides two numbers"
)
def divide(a: float, b: float) -> float:
    """
    Divides Numbers

    args: a (float): first number
          b (float): second number

    Returns:
        float: Result of the multiplication.
    """
    if b== 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


if __name__ == "__main__":
    mcp.run()

