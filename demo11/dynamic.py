from langchain_community.utilities import SQLDatabase

from dotenv import load_dotenv
load_dotenv()

db = SQLDatabase.from_uri("sqlite:///../assets/Chinook.db")

from dataclasses import dataclass


@dataclass
class RuntimeContext:
    is_employee: bool
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
    

SYSTEM_PROMPT_TEMPLATE = """You are a careful SQLite analyst.

Rules:
- Think step-by-step.
- When you need data, call the tool `execute_sql` with ONE SELECT query.
- Read-only only; no INSERT/UPDATE/DELETE/ALTER/DROP/CREATE/REPLACE/TRUNCATE.
- Limit to 5 rows unless the user explicitly asks otherwise.
{table_limits}
- If the tool returns 'Error:', revise the SQL and try again.
- Prefer explicit column lists; avoid SELECT *.
"""

from langchain.agents.middleware.types import ModelRequest, dynamic_prompt


@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest) -> str:
    if not request.runtime.context.is_employee:
        table_limits = "limit access to these tables: Album, Artist, Genre, Playlist, PlaylistTrack, Track."
    else:
        table_limits = ""

    return SYSTEM_PROMPT_TEMPLATE.format(table_limits=table_limits)

from langchain.agents import create_agent

agent = create_agent(
    model="deepseek-chat",
    tools=[execute_sql],
    middleware=[dynamic_system_prompt],
    context_schema=RuntimeContext,
)

question = "What is the most costly purchase by Frank Harris?"

for step in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    context=RuntimeContext(is_employee=False, db=db),
    stream_mode="values",
):
    step["messages"][-1].pretty_print()


