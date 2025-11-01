# DeepSeek 聊天模型集成

本文介绍如何使用Langchain集成 DeepSeek 聊天模型。


## 环境设置

1. 安装 `langchain-deepseek` 库
2. 设置环境变量 `DEEPSEEK_API_KEY`

```bash
pip install -U langchain-deepseek
export DEEPSEEK_API_KEY="your-api-key"
```


## 关键初始化参数

### 完成参数
- `model`: 要使用的 DeepSeek 模型名称，例如 `"deepseek-chat"`
- `temperature`: 采样温度
- `max_tokens`: 生成的最大令牌数

### 客户端参数
- `timeout`: 请求超时时间
- `max_retries`: 最大重试次数
- `api_key`: DeepSeek API 密钥。如果未传入，将从环境变量 `DEEPSEEK_API_KEY` 中读取


## 实例化模型

```python
from langchain_deepseek import ChatDeepSeek

model = ChatDeepSeek(
    model="...",          # 模型名称
    temperature=0,        # 采样温度
    max_tokens=None,      # 最大生成令牌数
    timeout=None,         # 超时时间
    max_retries=2,        # 最大重试次数
    # api_key="...",      # API密钥（可选）
    # 其他参数...
)
```


## 调用模型

### 基本调用

```python
messages = [
    ("system", "You are a helpful translator. Translate the user sentence to French."),
    ("human", "I love programming."),
]
model.invoke(messages)
```

### 流式输出

```python
for chunk in model.stream(messages):
    print(chunk.text, end="")
```

```python
stream = model.stream(messages)
full = next(stream)
for chunk in stream:
    full += chunk
full
```

### 异步调用

```python
await model.ainvoke(messages)

# 异步流式输出:
# async for chunk in (await model.astream(messages))

# 批量调用:
# await model.abatch([messages])
```


## 工具调用

```python
from pydantic import BaseModel, Field

class GetWeather(BaseModel):
    '''Get the current weather in a given location'''
    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")

class GetPopulation(BaseModel):
    '''Get the current population in a given location'''
    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")

model_with_tools = model.bind_tools([GetWeather, GetPopulation])
ai_msg = model_with_tools.invoke("Which city is hotter today and which is bigger: LA or NY?")
ai_msg.tool_calls
```

更多详情参见 `ChatDeepSeek.bind_tools()` 方法。


## 结构化输出

```python
from typing import Optional
from pydantic import BaseModel, Field

class Joke(BaseModel):
    '''Joke to tell user.'''
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: int | None = Field(description="How funny the joke is, from 1 to 10")

structured_model = model.with_structured_output(Joke)
structured_model.invoke("Tell me a joke about cats")
```

更多详情参见 `ChatDeepSeek.with_structured_output()` 方法。


## 令牌使用情况

```python
ai_msg = model.invoke(messages)
ai_msg.usage_metadata
```

输出示例：
```python
{"input_tokens": 28, "output_tokens": 5, "total_tokens": 33}
```


## 响应元数据

```python
ai_msg = model.invoke(messages)
ai_msg.response_metadata
```