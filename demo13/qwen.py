from langchain_openai import ChatOpenAI
import os

from dotenv import load_dotenv
load_dotenv()

chatLLM = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-max",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    # other params...
)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你是什么模型？"}]

response = chatLLM.invoke(messages)

print(response.model_dump_json())

