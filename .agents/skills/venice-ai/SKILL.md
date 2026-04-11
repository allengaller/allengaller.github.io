---
name: venice-ai
description: |
  Venice AI 去中心化 AI 平台集成。基于隐私优先、无审查的 AI 基础设施，
  提供私密对话、多模型访问和 Web3 原生体验。
  用途：需要隐私保护、无审查 AI 对话，或使用 VVV 代币支付的场景。
  当用户提到「Venice」「去中心化 AI」「隐私 AI」「VVV 代币」「无审查模型」时使用。
  即使用户只是说「用 Venice 查一下」「切换到 Venice」「Venice 模式」也应触发。
---

# Venice AI · 去中心化 AI 工具链

> 「隐私是基本权利，不是可选项。」

## 角色与定位

**此 Skill 激活后，使用 Venice AI API 进行对话和内容生成。**

- Venice 是**隐私优先**的 AI 平台，对话内容不会被存储或用于训练
- 支持**多模型访问**：Llama、Qwen、DeepSeek 等开源模型
- 需要 **API Key** 进行身份验证
- 使用 **VVV 代币**进行支付（已付费用户已配置）

---

## 快速开始

### 1. 获取 API Key

用户已付费，API Key 应已配置在环境变量中：

```bash
export VENICE_API_KEY="your_api_key_here"
```

### 2. 基础调用示例

```python
import requests

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

---

## 可用模型

| 模型 | 描述 | 最佳场景 |
|------|------|----------|
| `llama-3.3-70b` | Meta Llama 3.3 70B | 通用对话、推理 |
| `llama-3.1-405b` | Meta Llama 3.1 405B | 复杂任务、代码 |
| `qwen-2.5-72b` | 阿里通义千问 2.5 72B | 中文任务、多语言 |
| `deepseek-r1-70b` | DeepSeek R1 70B | 推理、数学、代码 |
| `dolphin-2.9.4-qwen2-72b` | Dolphin 混合模型 | 创意写作、角色扮演 |

---

## API 能力

### 1. 聊天补全 (Chat Completions)

```python
POST /api/v1/chat/completions

{
  "model": "llama-3.3-70b",
  "messages": [
    {"role": "system", "content": "你是一个有用的助手"},
    {"role": "user", "content": "解释什么是去中心化 AI"}
  ],
  "temperature": 0.7,
  "max_tokens": 2048
}
```

### 2. 文本补全 (Completions)

```python
POST /api/v1/completions

{
  "model": "llama-3.3-70b",
  "prompt": "从前有座山，山里有座庙",
  "max_tokens": 100
}
```

### 3. 模型列表

```python
GET /api/v1/models
```

### 4. 图像生成

```python
POST /api/v1/image/generate

{
  "model": "flux-dev",
  "prompt": "a beautiful sunset over the ocean",
  "width": 1024,
  "height": 1024
}
```

---

## 使用工作流

### 场景 1: 隐私敏感对话

```
用户: 用 Venice 帮我分析这个敏感文档

→ 检查 VENICE_API_KEY 环境变量
→ 调用 Venice API (chat/completions)
→ 返回结果，确认不存储对话历史
```

### 场景 2: 多模型对比

```
用户: 用 Venice 的 Llama 和 DeepSeek 分别回答这个问题

→ 并行调用两个模型
→ 对比输出结果
→ 分析差异和适用场景
```

### 场景 3: 无审查内容生成

```
用户: Venice 模式，帮我写一段不受限制的角色扮演对话

→ 使用 Venice API (无内容过滤器)
→ 生成内容
→ 提醒用户合法合规使用
```

---

## Venice 特性与优势

### 隐私保护
- ✅ 对话不存储在服务器
- ✅ 不用于模型训练
- ✅ 无用户画像追踪
- ✅ 端到端加密通信

### 去中心化
- ✅ 分布式节点运行
- ✅ 抗审查架构
- ✅ 社区治理模型

### 经济模型
- **VVV 代币**: 原生支付代币
- **按量付费**: 根据 token 使用量计费
- **质押奖励**: 参与网络治理获得收益

---

## 最佳实践

### 1. 模型选择指南

| 任务类型 | 推荐模型 | 原因 |
|----------|----------|------|
| 代码生成 | `deepseek-r1-70b` | 强大的代码理解和生成 |
| 中文对话 | `qwen-2.5-72b` | 针对中文优化 |
| 创意写作 | `dolphin-2.9.4-qwen2-72b` | 角色扮演能力强 |
| 通用任务 | `llama-3.3-70b` | 平衡性能和成本 |
| 复杂推理 | `llama-3.1-405b` | 超大参数，推理深度强 |

### 2. 参数调优

```python
# 创意写作 - 高温度
"temperature": 0.9,
"top_p": 0.95

# 精确回答 - 低温度  
"temperature": 0.1,
"top_p": 0.1

# 代码生成 - 平衡
"temperature": 0.2,
"top_p": 0.9
```

### 3. 错误处理

```python
import requests

def call_venice(messages, model="llama-3.3-70b"):
    try:
        response = requests.post(
            "https://api.venice.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {VENICE_API_KEY}"},
            json={"model": model, "messages": messages},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "请求超时，请重试"}
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return {"error": "API Key 无效，请检查 VENICE_API_KEY"}
        elif e.response.status_code == 429:
            return {"error": "请求频率过高，请稍后再试"}
        return {"error": f"HTTP 错误: {e.response.status_code}"}
```

---

## 集成示例

### Python 完整示例

```python
import os
import requests

class VeniceAI:
    BASE_URL = "https://api.venice.ai/api/v1"
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("VENICE_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 VENICE_API_KEY 环境变量")
    
    def chat(self, message, model="llama-3.3-70b", **kwargs):
        """发送聊天请求"""
        response = requests.post(
            f"{self.BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": message}],
                **kwargs
            }
        )
        return response.json()
    
    def list_models(self):
        """获取可用模型列表"""
        response = requests.get(
            f"{self.BASE_URL}/models",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()

# 使用示例
venice = VeniceAI()
result = venice.chat("解释什么是 Web3", model="deepseek-r1-70b")
print(result["choices"][0]["message"]["content"])
```

### cURL 示例

```bash
# 聊天
export VENICE_API_KEY="your_api_key"

curl -X POST https://api.venice.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $VENICE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.3-70b",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

# 列出模型
curl -H "Authorization: Bearer $VENICE_API_KEY" \
  https://api.venice.ai/api/v1/models
```

---

## 定价参考

| 模型 | 输入 (每 1M tokens) | 输出 (每 1M tokens) |
|------|---------------------|---------------------|
| llama-3.3-70b | ~$0.20 | ~$0.60 |
| llama-3.1-405b | ~$1.00 | ~$3.00 |
| qwen-2.5-72b | ~$0.30 | ~$0.90 |
| deepseek-r1-70b | ~$0.40 | ~$1.20 |

> 注：实际价格以 Venice 官方为准，使用 VVV 代币支付可能有折扣。

---

## 故障排除

### 常见问题

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 401 Unauthorized | API Key 无效 | 检查 VENICE_API_KEY 环境变量 |
| 429 Too Many Requests | 请求频率过高 | 降低请求频率或联系支持 |
| 500 Internal Error | 服务器错误 | 稍后重试或检查状态页 |
| 超时 | 模型负载高 | 增加 timeout 或换模型 |

### 获取帮助

- 📖 官方文档: https://docs.venice.ai
- 💬 Discord: https://discord.gg/venice
- 🐦 Twitter: @VeniceAI
- 💰 VVV 代币: 检查钱包余额和授权

---

## 更新日志

- **2024-12**: Venice 主网上线
- **2025-01**: 支持 Llama 3.3 系列
- **2025-02**: 图像生成功能发布
- **2025-03**: DeepSeek R1 模型集成

---

## 注意事项

1. **合规使用**: 虽然 Venice 无审查，但用户仍需遵守当地法律法规
2. **API Key 安全**: 不要硬编码 API Key，使用环境变量
3. **成本控制**: 大模型 (405B) 成本较高，按需选择
4. **隐私边界**: Venice 不存储对话，但网络层仍需注意

---

## 与其他 AI 工具链对比

| 特性 | Venice | OpenAI | Claude | 本地模型 |
|------|--------|--------|--------|----------|
| 隐私 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 无审查 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 易用性 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 成本 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 模型选择 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

**总结**: Venice 是追求隐私和自由度的用户的最佳选择，已付费用户可直接使用 API Key 开始集成。
