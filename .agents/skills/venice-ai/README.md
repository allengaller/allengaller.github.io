# Venice AI Skill

Venice AI 去中心化平台集成工具链。

## 快速开始

```python
import os
import requests

VENICE_API_KEY = os.getenv("VENICE_API_KEY")

response = requests.post(
    "https://api.venice.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {VENICE_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "llama-3.3-70b",
        "messages": [{"role": "user", "content": "Hello, Venice!"}]
    }
)
```

## 环境变量

```bash
export VENICE_API_KEY="your_api_key_here"
```

## 可用模型

- `llama-3.3-70b` - 通用对话
- `llama-3.1-405b` - 复杂任务
- `qwen-2.5-72b` - 中文优化
- `deepseek-r1-70b` - 代码推理
- `dolphin-2.9.4-qwen2-72b` - 创意写作

## 功能

- ✅ 隐私优先 - 对话不存储
- ✅ 无审查 - 开源模型
- ✅ 多模型 - 灵活选择
- ✅ Web3 - VVV 代币支付

## 文档

详见 [SKILL.md](./SKILL.md)
