from langchain_community.utilities import SQLDatabase

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

from langchain_core.tools import tool
from langgraph.runtime import get_runtime
from dataclasses import dataclass

from dotenv import load_dotenv
load_dotenv()

db = SQLDatabase.from_uri("sqlite:///Chinook.db")

# define context structure to support dependency injection


@dataclass
class RuntimeContext:
    db: SQLDatabase


model = init_chat_model(
    "deepseek-chat",
    # Kwargs passed to the model:
    temperature=0,
    timeout=30,
    max_tokens=1000,
)

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
- Limit to 5 rows of output unless the user explicitly asks otherwise.
- If the tool returns 'Error:', revise the SQL and try again.
- Prefer explicit column lists; avoid SELECT *.
"""

agent = create_agent(
    model=model,
    tools=[execute_sql],
    system_prompt=SYSTEM_PROMPT,
    response_format=None
)

# Run the agent
# raw_response = agent.invoke(
#     {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
# )

question = "Which table has the largest number of entries?"
msg = {"messages": [{"role": "user", "content": question}]}

# Stream mode values 按每个步骤输出message

for step in agent.stream(
    msg,
    context=RuntimeContext(db=db),
    stream_mode="values",
):
    # print(step["messages"][-1])
    step["messages"][-1].pretty_print()



# Stream mode messages 按token逐个输出

# for token, metadata in agent.stream(
#     msg,
#     context=RuntimeContext(db=db),
#     stream_mode="messages",
# ):
#     print(f'{token.content}', end='')



# ================================ Human Message =================================

# Which table has the largest number of entries?
# ================================== Ai Message ==================================

# I'll help you find which table has the largest number of entries. Let me first check what tables are available in the database.
# Tool Calls:
#   execute_sql (call_00_P9LFuQIGETVwieO3YvO6ee3Z)
#  Call ID: call_00_P9LFuQIGETVwieO3YvO6ee3Z
#   Args:
#     query: SELECT name FROM sqlite_master WHERE type='table';
# ================================= Tool Message =================================
# Name: execute_sql

# [('Album',), ('Artist',), ('Customer',), ('Employee',), ('Genre',), ('Invoice',), ('InvoiceLine',), ('MediaType',), ('Playlist',), ('PlaylistTrack',), ('Track',)]
# ================================== Ai Message ==================================

# Now I'll check the row count for each table to determine which one has the most entries:
# Tool Calls:
#   execute_sql (call_00_Ja2GGak4vPhCrF82xpCPNwzV)
#  Call ID: call_00_Ja2GGak4vPhCrF82xpCPNwzV
#   Args:
#     query: SELECT 'Album' as table_name, COUNT(*) as row_count FROM Album
# UNION ALL
# SELECT 'Artist', COUNT(*) FROM Artist
# UNION ALL
# SELECT 'Customer', COUNT(*) FROM Customer
# UNION ALL
# SELECT 'Employee', COUNT(*) FROM Employee
# UNION ALL
# SELECT 'Genre', COUNT(*) FROM Genre
# UNION ALL
# SELECT 'Invoice', COUNT(*) FROM Invoice
# UNION ALL
# SELECT 'InvoiceLine', COUNT(*) FROM InvoiceLine
# UNION ALL
# SELECT 'MediaType', COUNT(*) FROM MediaType
# UNION ALL
# SELECT 'Playlist', COUNT(*) FROM Playlist
# UNION ALL
# SELECT 'PlaylistTrack', COUNT(*) FROM PlaylistTrack
# UNION ALL
# SELECT 'Track', COUNT(*) FROM Track
# ORDER BY row_count DESC
# LIMIT 5;
# ================================= Tool Message =================================
# Name: execute_sql

# [('PlaylistTrack', 8715), ('Track', 3503), ('InvoiceLine', 2240), ('Invoice', 412), ('Album', 347)]
# ================================== Ai Message ==================================

# Based on the query results, the **PlaylistTrack** table has the largest number of entries with **8,715 rows**.

# Here's the ranking of the top 5 tables by row count:
# 1. PlaylistTrack: 8,715 rows
# 2. Track: 3,503 rows
# 3. InvoiceLine: 2,240 rows
# 4. Invoice: 412 rows
# 5. Album: 347 rows

# The PlaylistTrack table appears to be a junction table that tracks which tracks belong to which playlists, which explains why it has the highest number of entries.