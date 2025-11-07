from typing import Literal
from langchain.tools import tool
from langchain.agents import create_agent

from dotenv import load_dotenv
load_dotenv()

# @tool
# def real_number_calculator(
#     a: float, b: float, operation: Literal["add", "subtract", "multiply", "divide"]
# ) -> float:
#     """Perform basic arithmetic operations on two real numbers."""
#     print("🧮 Invoking calculator tool")
#     # Perform the specified operation
#     if operation == "add":
#         return a + b
#     elif operation == "subtract":
#         return a - b
#     elif operation == "multiply":
#         return a * b
#     elif operation == "divide":
#         if b == 0:
#             raise ValueError("Division by zero is not allowed.")
#         return a / b
#     else:
#         raise ValueError(f"Invalid operation: {operation}")

@tool(
    "calculator",
    parse_docstring=True,
    description=(
        "Perform basic arithmetic operations on two real numbers."
        "Use this whenever you have operations on any numbers, even if they are integers."
    ),
)
def real_number_calculator(
    a: float, b: float, operation: Literal["add", "subtract", "multiply", "divide"]
) -> float:
    """Perform basic arithmetic operations on two real numbers.

    Args:
        a (float): The first number.
        b (float): The second number.
        operation (Literal["add", "subtract", "multiply", "divide"]):
            The arithmetic operation to perform.

            - `"add"`: Returns the sum of `a` and `b`.
            - `"subtract"`: Returns the result of `a - b`.
            - `"multiply"`: Returns the product of `a` and `b`.
            - `"divide"`: Returns the result of `a / b`. Raises an error if `b` is zero.

    Returns:
        float: The numerical result of the specified operation.

    Raises:
        ValueError: If an invalid operation is provided or division by zero is attempted.
    """
    print("🧮  Invoking calculator tool")
    # Perform the specified operation
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b
    else:
        raise ValueError(f"Invalid operation: {operation}")


agent = create_agent(
    model="deepseek-chat",
    tools=[real_number_calculator],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "what is 3.1125 * 4.1234"}]}
)

print(result["messages"][-1].content)