

# Langchain(v1.0.2)

## 1. Agents

主要是一个入口，它有一个`create_agent`函数, 创建一个循环loop，用于和`LLM`交互，定义如下：

```
Creates an agent graph that calls tools in a loop until a stopping condition is met.
```

### create_agent 参数:

model: The language model for the agent. Can be a string identifier (e.g., "openai:gpt-4") or a chat model instance (e.g., ChatOpenAI()).
tools: A list of tools, dicts, or Callable. If None or an empty list, the agent will consist of a model node without a tool calling loop.
system_prompt: An optional system prompt for the LLM. Prompts are converted to a SystemMessage and added to the beginning of the message list.
middleware: A sequence of middleware instances to apply to the agent. Middleware can intercept and modify agent behavior at various stages.

response_format: An optional configuration for structured responses. Can be a ToolStrategy, ProviderStrategy, or a Pydantic model class. If provided, the agent will handle structured output during the conversation flow. Raw schemas will be wrapped in an appropriate strategy based on model capabilities.

### Models
### Messages
### Tools
### Short-term memory
### Streaming
### Middleware
### Structured output




## 参考链接
https://docs.langchain.com/oss/python/langchain/overview
https://reference.langchain.com/python/langchain/langchain/