from langchain_community.utilities import SQLDatabase

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
)

question = "This is Frank Harris, What was the total on my last invoice?"
steps = []

for step in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    stream_mode="values",
    context=RuntimeContext(db=db),
):
    step["messages"][-1].pretty_print()
    steps.append(step)

# ================================ Human Message =================================

# This is Frank Harris, What was the total on my last invoice?
# ================================== Ai Message ==================================

# I'll help you find the total on Frank Harris's last invoice. Let me start by looking for Frank Harris in the database and then find his most recent invoice.
# Tool Calls:
#   execute_sql (call_00_ohhgrPb7edK73LjVjZLJakoE)
#  Call ID: call_00_ohhgrPb7edK73LjVjZLJakoE
#   Args:
#     query: SELECT * FROM customers WHERE first_name = 'Frank' AND last_name = 'Harris'
# ================================= Tool Message =================================
# Name: execute_sql

# Error: (sqlite3.OperationalError) no such table: customers
# [SQL: SELECT * FROM customers WHERE first_name = 'Frank' AND last_name = 'Harris']
# (Background on this error at: https://sqlalche.me/e/20/e3q8)
# ================================== Ai Message ==================================

# Let me first check what tables are available in the database to understand its structure.
# Tool Calls:
#   execute_sql (call_00_AhstVeFdiqPpyo0x6P8iNI6Y)
#  Call ID: call_00_AhstVeFdiqPpyo0x6P8iNI6Y
#   Args:
#     query: SELECT name FROM sqlite_master WHERE type='table'
# ================================= Tool Message =================================
# Name: execute_sql

# [('Album',), ('Artist',), ('Customer',), ('Employee',), ('Genre',), ('Invoice',), ('InvoiceLine',), ('MediaType',), ('Playlist',), ('PlaylistTrack',), ('Track',)]
# ================================== Ai Message ==================================

# Great! I can see there's a `Customer` table and an `Invoice` table. Let me find Frank Harris in the Customer table:
# Tool Calls:
#   execute_sql (call_00_nQiLLHJbRGZsggQ2HcK3ZCjV)
#  Call ID: call_00_nQiLLHJbRGZsggQ2HcK3ZCjV
#   Args:
#     query: SELECT CustomerId, FirstName, LastName FROM Customer WHERE FirstName = 'Frank' AND LastName = 'Harris'
# ================================= Tool Message =================================
# Name: execute_sql

# [(16, 'Frank', 'Harris')]
# ================================== Ai Message ==================================

# Perfect! Now let me find Frank Harris's most recent invoice by looking at the Invoice table:
# Tool Calls:
#   execute_sql (call_00_tXyXwY0BvLDrpn0aB7r08Lee)
#  Call ID: call_00_tXyXwY0BvLDrpn0aB7r08Lee
#   Args:
#     query: SELECT InvoiceId, InvoiceDate, Total FROM Invoice WHERE CustomerId = 16 ORDER BY InvoiceDate DESC LIMIT 1
# ================================= Tool Message =================================
# Name: execute_sql

# [(374, '2013-07-04 00:00:00', 5.94)]
# ================================== Ai Message ==================================

# Frank Harris's last invoice was invoice #374 dated July 4, 2013, and the total amount was **$5.94**.


# 测试没有记忆能力，输出如下：
# question = "What were the titles?"

# for step in agent.stream(
#     {"messages": [{"role": "user", "content": question}]},
#     context=RuntimeContext(db=db),
#     stream_mode="values",
# ):
#     step["messages"][-1].pretty_print()

# ================================ Human Message =================================

# What were the titles?
# ================================== Ai Message ==================================

# I notice you're asking about titles, but I need more context to help you effectively. Could you please specify:

# 1. Which database table or dataset you're referring to?
# 2. What kind of titles are you looking for (movie titles, book titles, article titles, etc.)?
# 3. Any additional criteria like date ranges, categories, or specific authors/directors?

# Once you provide more details, I'll be able to query the appropriate database table and retrieve the title information you're looking for.