from langchain.messages import HumanMessage, AIMessage, ToolMessage
from langchain.agents import create_agent

from dotenv import load_dotenv
load_dotenv()

def get_weather_tool(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="deepseek-chat",
    tools=[get_weather_tool],
    system_prompt="You are a helpful assistant",
    response_format=None
)

# Run the agent
raw_response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

def format_agent_response(raw_response):

    """
    格式化 LangChain Agent 的原始响应
    
    参数：
        raw_response: 原始响应（包含 'messages' 列表的字典）
    返回：
        格式化后的字典，包含核心信息
    """
    messages = raw_response.get('messages', [])
    formatted = {
        "user_question": None,          # 用户问题
        "final_answer": None,           # AI 最终回答
        "tool_calls": [],               # 工具调用记录
        "token_usage": None             # token 用量（最后一条 AI 消息的统计）
    }
    
    # 1. 提取用户问题（第一条 HumanMessage）
    for msg in messages:
        if isinstance(msg, HumanMessage):
            formatted["user_question"] = msg.content
            break
    
    # 2. 提取工具调用记录（ToolMessage 及其对应的 AIMessage 工具调用）
    tool_call_map = {}  # 临时存储：tool_call_id -> 工具调用信息
    for msg in messages:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            # 记录 AI 调用的工具（名称、参数、id）
            for tool_call in msg.tool_calls:
                tool_call_info = {
                    "name": tool_call.get("name"),
                    "args": tool_call.get("args"),
                    "id": tool_call.get("id"),
                    "result": None  # 后续关联 ToolMessage 的结果
                }
                tool_call_map[tool_call["id"]] = tool_call_info
                formatted["tool_calls"].append(tool_call_info)
        elif isinstance(msg, ToolMessage):
            # 关联工具调用结果到对应的工具调用记录
            tool_id = msg.tool_call_id
            if tool_id in tool_call_map:
                tool_call_map[tool_id]["result"] = msg.content
    
    # 3. 提取最终回答（最后一条 AIMessage 的内容）
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and not msg.tool_calls:  # 无工具调用的 AIMessage 通常是最终回答
            formatted["final_answer"] = msg.content
            # 提取 token 用量（从 response_metadata 中）
            formatted["token_usage"] = msg.response_metadata.get("token_usage")
            break
    
    return formatted

formatted_result = format_agent_response(raw_response)

print(formatted_result)
# {'user_question': 'what is the weather in sf', 'final_answer': "According to the weather information, it's always sunny in San Francisco!", 'tool_calls': [{'name': 'get_weathe_tool', 'args': {'city': 'San Francisco'}, 'id': 'call_00_VZVq95cEuhU8b5ZeWQOMNwjv', 'result': "It's always sunny in San Francisco!"}], 'token_usage': {'completion_tokens': 14, 'prompt_tokens': 201, 'total_tokens': 215, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 128}, 'prompt_cache_hit_tokens': 128, 'prompt_cache_miss_tokens': 73}}