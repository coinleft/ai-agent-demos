from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

from dotenv import load_dotenv
load_dotenv()

# Connect to the mcp-time server for timezone-aware operations
# This Go-based server provides tools for current time, relative time parsing,
# timezone conversion, duration arithmetic, and time comparison
mcp_client = MultiServerMCPClient(
    {
        "time": {
            "transport": "stdio",
            "command": "npx",
            "args": ["-y", "@theo.foobar/mcp-time"],
        }
    },
)

# Load tools from the MCP server
async def get_mcp_tools():
    mcp_tools = await mcp_client.get_tools()
    print(f"Loaded {len(mcp_tools)} MCP tools: {[t.name for t in mcp_tools]}")
    return mcp_tools

# asyncio.run(get_mcp_tools())
# Loaded 5 MCP tools: ['add_time', 'compare_time', 'convert_timezone', 'current_time', 'relative_time']

async def main():
    mcp_tools = await mcp_client.get_tools()

    agent_with_mcp = create_agent(
        model="deepseek-chat",
        tools=mcp_tools,
        system_prompt="You are a helpful assistant",
    )

    result = await agent_with_mcp.ainvoke(
        {"messages": [
            {"role": "user", "content": "What's the time in Beijing right now?"}]}
    )
    for msg in result["messages"]:
        msg.pretty_print()

asyncio.run(main())
# ================================ Human Message =================================

# What's the time in Beijing right now?
# ================================== Ai Message ==================================

# I'll check the current time in Beijing for you.
# Tool Calls:
#   current_time (call_00_yHpyeoi5Mnc5Za8ADPo9i1fg)
#  Call ID: call_00_yHpyeoi5Mnc5Za8ADPo9i1fg
#   Args:
#     timezone: Asia/Shanghai
#     format: 2006-01-02 15:04:05
# ================================= Tool Message =================================
# Name: current_time

# 2025-11-07 18:11:59
# ================================== Ai Message ==================================

# The current time in Beijing is **2025-11-07 18:11:59** (6:11 PM). Note that Beijing uses the Asia/Shanghai timezone, which is UTC+8.