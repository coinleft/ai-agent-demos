from langchain_community.utilities import SQLDatabase
from langgraph.checkpoint.memory import InMemorySaver

from dotenv import load_dotenv
load_dotenv()

from dataclasses import dataclass
db = SQLDatabase.from_uri("sqlite:///../assets/Chinook.db")

@dataclass
class RuntimeContext:
    db: SQLDatabase

from langchain_core.tools import tool
from langgraph.runtime import get_runtime

@tool
def execute_sql(query: str) -> str:
    """Execute a SQLite command and return results."""
    runtime = get_runtime(RuntimeContext)
    db = runtime.context.db

    try:
        return db.run(query)
    except Exception as e:
        return f"Error: {e}"
    
SYSTEM_PROMPT = """You are a careful SQLite analyst.

Rules:
- Think step-by-step.
- When you need data, call the tool `execute_sql` with ONE SELECT query.
- Read-only only; no INSERT/UPDATE/DELETE/ALTER/DROP/CREATE/REPLACE/TRUNCATE.
- Limit to 5 rows unless the user explicitly asks otherwise.
- If the tool returns 'Error:', revise the SQL and try again.
- Prefer explicit column lists; avoid SELECT *.
"""

from langchain.agents import create_agent

agent = create_agent(
    model="deepseek-chat",
    tools=[execute_sql],
    system_prompt=SYSTEM_PROMPT,
    context_schema=RuntimeContext,
    checkpointer=InMemorySaver(),
)

question = "This is Frank Harris, What was the total on my last invoice?"
steps = []

for step in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    {"configurable": {"thread_id": "1"}}, 
    stream_mode="values",
    context=RuntimeContext(db=db),
):
    step["messages"][-1].pretty_print()
    steps.append(step)


question2 = "What were the titles?"
steps2 = []

for step2 in agent.stream(
    {"messages": [{"role": "user", "content": question2}]},
    {"configurable": {"thread_id": "1"}},
    context=RuntimeContext(db=db),
    stream_mode="values",
):
    step2["messages"][-1].pretty_print()
    steps2.append(step2)

# ================================ Human Message =================================

# What were the titles?
# ================================== Ai Message ==================================

# I'll find the titles of the items on Frank Harris's last invoice. Let me look at the invoice lines for invoice #374:
# Tool Calls:
#   execute_sql (call_00_yDC0HCWRfdg6lxskkJ5qzKnB)
#  Call ID: call_00_yDC0HCWRfdg6lxskkJ5qzKnB
#   Args:
#     query: SELECT il.*, t.Name as TrackName FROM InvoiceLine il JOIN Track t ON il.TrackId = t.TrackId WHERE il.InvoiceId = 374;
# ================================= Tool Message =================================
# Name: execute_sql

# [(2021, 374, 1803, 0.99, 1, 'Holier Than Thou'), (2022, 374, 1807, 0.99, 1, 'Through The Never'), (2023, 374, 1811, 0.99, 1, 'My Friend Of Misery'), (2024, 374, 1815, 0.99, 1, 'The Wait'), (2025, 374, 1819, 0.99, 1, 'Blitzkrieg'), (2026, 374, 1823, 0.99, 1, 'So What')]
# ================================== Ai Message ==================================

# Frank Harris, the titles on your last invoice (Invoice #374) were:

# 1. "Holier Than Thou"
# 2. "Through The Never"
# 3. "My Friend Of Misery"
# 4. "The Wait"
# 5. "Blitzkrieg"
# 6. "So What"

# These were all individual tracks purchased at $0.99 each, totaling $5.94.