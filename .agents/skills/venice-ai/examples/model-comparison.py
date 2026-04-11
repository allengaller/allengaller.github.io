#!/usr/bin/env python3
"""
Venice AI 多模型对比示例
"""
import os
import requests
from concurrent.futures import ThreadPoolExecutor

VENICE_API_KEY = os.getenv("VENICE_API_KEY")
BASE_URL = "https://api.venice.ai/api/v1"


def ask_model(model, message):
    """向指定模型发送请求"""
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {VENICE_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "temperature": 0.7,
            "max_tokens": 500
        },
        timeout=60
    )
    
    if response.status_code == 200:
        content = response.json()["choices"][0]["message"]["content"]
        return model, content
    else:
        return model, f"Error: {response.status_code}"


def compare_models(message, models=None):
    """并行对比多个模型的回答"""
    if models is None:
        models = [
            "llama-3.3-70b",
            "qwen-2.5-72b",
            "deepseek-r1-70b"
        ]
    
    results = {}
    
    with ThreadPoolExecutor(max_workers=len(models)) as executor:
        futures = {
            executor.submit(ask_model, model, message): model 
            for model in models
        }
        
        for future in futures:
            model, content = future.result()
            results[model] = content
    
    return results


if __name__ == "__main__":
    # 测试问题
    questions = [
        "用一句话解释区块链",
        "Python 中装饰器是什么",
        "写一首关于 AI 的四行诗"
    ]
    
    for question in questions:
        print(f"\n{'='*60}")
        print(f"问题: {question}")
        print('='*60)
        
        results = compare_models(question)
        
        for model, answer in results.items():
            print(f"\n[{model}]")
            print(f"{answer}")
