#!/usr/bin/env python3
"""
Venice AI Python 客户端封装
"""
import os
import requests
from typing import List, Dict, Optional, Generator


class VeniceAI:
    """Venice AI API 客户端"""
    
    BASE_URL = "https://api.venice.ai/api/v1"
    
    # 推荐模型
    MODELS = {
        "general": "llama-3.3-70b",
        "code": "deepseek-r1-70b",
        "chinese": "qwen-2.5-72b",
        "creative": "dolphin-2.9.4-qwen2-72b",
        "large": "llama-3.1-405b"
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 Venice AI 客户端
        
        Args:
            api_key: Venice API Key，默认从环境变量 VENICE_API_KEY 读取
        """
        self.api_key = api_key or os.getenv("VENICE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "请提供 api_key 或设置 VENICE_API_KEY 环境变量"
            )
    
    def _headers(self) -> Dict[str, str]:
        """生成请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(
        self,
        message: str,
        model: str = None,
        system: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False
    ) -> Dict:
        """
        发送聊天请求
        
        Args:
            message: 用户消息
            model: 模型名称，默认 llama-3.3-70b
            system: 系统提示词
            temperature: 温度参数 (0-2)
            max_tokens: 最大生成 token 数
            stream: 是否流式返回
        
        Returns:
            API 响应 JSON
        """
        model = model or self.MODELS["general"]
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": message})
        
        response = requests.post(
            f"{self.BASE_URL}/chat/completions",
            headers=self._headers(),
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": stream
            },
            stream=stream,
            timeout=60
        )
        
        response.raise_for_status()
        return response.json()
    
    def chat_simple(
        self,
        message: str,
        model: str = None,
        **kwargs
    ) -> str:
        """
        简化版聊天，直接返回文本内容
        
        Args:
            message: 用户消息
            model: 模型名称
            **kwargs: 其他参数传递给 chat()
        
        Returns:
            生成的文本内容
        """
        result = self.chat(message, model=model, **kwargs)
        return result["choices"][0]["message"]["content"]
    
    def list_models(self) -> List[Dict]:
        """
        获取可用模型列表
        
        Returns:
            模型列表
        """
        response = requests.get(
            f"{self.BASE_URL}/models",
            headers=self._headers(),
            timeout=30
        )
        response.raise_for_status()
        return response.json().get("data", [])
    
    def generate_image(
        self,
        prompt: str,
        model: str = "flux-dev",
        width: int = 1024,
        height: int = 1024
    ) -> Dict:
        """
        生成图像
        
        Args:
            prompt: 图像描述
            model: 图像生成模型
            width: 图像宽度
            height: 图像高度
        
        Returns:
            API 响应
        """
        response = requests.post(
            f"{self.BASE_URL}/image/generate",
            headers=self._headers(),
            json={
                "model": model,
                "prompt": prompt,
                "width": width,
                "height": height
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()


# 便捷函数
def quick_chat(message: str, model: str = None) -> str:
    """
    快速聊天，无需实例化客户端
    
    Args:
        message: 用户消息
        model: 模型名称
    
    Returns:
        生成的文本内容
    """
    client = VeniceAI()
    return client.chat_simple(message, model=model)


if __name__ == "__main__":
    # 测试客户端
    client = VeniceAI()
    
    print("1. 测试简单对话")
    print(client.chat_simple("Hello! 用中文回答"))
    
    print("\n2. 测试代码模型")
    code = client.chat_simple(
        "写个 Python 函数计算斐波那契数列",
        model="deepseek-r1-70b"
    )
    print(code)
    
    print("\n3. 测试模型列表")
    models = client.list_models()
    print(f"可用模型数量: {len(models)}")
