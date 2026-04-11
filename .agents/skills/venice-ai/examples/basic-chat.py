#!/usr/bin/env python3
"""
Venice AI 基础聊天示例
"""
import os
import requests

# 从环境变量获取 API Key
VENICE_API_KEY = os.getenv("VENICE_API_KEY")
if not VENICE_API_KEY:
    raise ValueError("请设置 VENICE_API_KEY 环境变量")

BASE_URL = "https://api.venice.ai/api/v1"


def chat(message, model="llama-3.3-70b", temperature=0.7):
    """发送聊天请求到 Venice AI"""
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {VENICE_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "temperature": temperature
        }
    )
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"


if __name__ == "__main__":
    # 测试不同模型
    models = [
        "llama-3.3-70b",
        "deepseek-r1-70b",
        "qwen-2.5-72b"
    ]
    
    question = "解释什么是去中心化 AI，用一句话概括"
    
    print(f"问题: {question}\n")
    
    for model in models:
        print(f"[{model}]")
        answer = chat(question, model=model)
        print(f"回答: {answer}\n")
