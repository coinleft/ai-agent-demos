import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),  
    base_url="https://api.deepseek.com"
)

def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    return response

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_closing_price",
            "description": "使用该工具获取指定股票的收盘价",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "股票名称",
                    }
                },
                "required": ["name"]
            },
        }
    },
]

def get_closing_price(stock_name):
    mock_data = {
        "青岛啤酒": {"股票名称": "青岛啤酒", "收盘价": 58.20, "日期": "2025-10-21"},
        "贵州茅台": {"股票名称": "贵州茅台", "收盘价": 1725.50, "日期": "2025-10-21"},
        "未知股票": "未查询到数据" 
    }
    return mock_data.get(stock_name, f"未查询到{stock_name}的信息")

if __name__ == "__main__":
    stock_name = input('输入要查询的股票名称: ')
    messages = [{"role": "user", "content": f"{stock_name}的收盘价是多少？"}]
    print(f'{messages[0]['role']}: {messages[0]['content']}')

    while True:
        response = send_messages(messages)
        print(f'{response.choices[0].message.role}: ')
        print(response.choices[0].message.content)

        messages.append(response.choices[0].message)

        if response.choices[0].message.tool_calls != None:
            tool_call = response.choices[0].message.tool_calls[0]
        
            if tool_call.function.name == "get_closing_price":
                arguments_dict = json.loads(tool_call.function.arguments)
                stock_search_result = get_closing_price(arguments_dict['name'])

                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "content": str(stock_search_result),
                })

                if isinstance(stock_search_result, dict):
                    print(f'tool: 获取到{stock_name}价格{stock_search_result['收盘价']}')
                    break
                else: 
                    print(f'tool: {stock_search_result}')


    response = send_messages(messages)
                
    print(f'{response.choices[0].message.role}: ')
    print(response.choices[0].message.content)