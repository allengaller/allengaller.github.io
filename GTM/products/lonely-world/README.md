# GTM — lonely-world 孤独世界

本目录是 lonely-world 的 Go-to-Market 资产。`index.html` 是对外发布落地页，本文件记录页面背后的 GTM 框架，供后续迭代与渠道投放对齐。

## 打开页面

```bash
# 直接用浏览器打开
open GTM/index.html

# 或起一个本地静态服务
python3 -m http.server 8080 --directory GTM
# 访问 http://localhost:8080
```

## 1. 定位声明（Positioning）

> 对于**渴望自己写故事**的中文玩家与创作者，孤独世界是一款**由 LLM 驱动、没有既定剧情**的文字冒险游戏。它把无限剧情的 AI 装进一个**会记事的本地引擎**：世界由你共创，角色长期记忆，存档 100% 在本地——不同于通关即弃的传统文字冒险，也不同于转身就忘的聊天 AI 扮演。

一句话版本（对外传播用）：

- **没有既定剧情的中文 AI 文字冒险。**
- 故事由你执笔，记忆归你保管。

## 2. 目标人群（ICP）

| 人群 | 核心诉求 | 关键信息 |
|------|----------|----------|
| 互动小说 / 文字冒险玩家 | 玩到没有攻略、剧透不了的故事 | 每次开局独一无二 |
| Solo 跑团 & GM | 一个不累、不穿帮、记得住伏笔的 GM | 长期记忆 + 世界观共创 |
| AI / 开源爱好者 | 接自己的模型、改自己的玩法 | provider 抽象 + MIT 开源 |
| 写作者 / 故事人 | 灵感引擎 + 可带走成稿 | 5 轮共创 + story.md 导出 |

## 3. 信息屋（Messaging House）

- **屋顶**（唯一主张）：会记事的本地引擎 × 无限剧情的 AI。
- **三根柱子**：
  1. 无限剧情 —— 无预设故事线、世界观 5 轮问答共创；
  2. 长期记忆 —— 角色/物品/恩怨持久化，Token-aware 上下文 + 记忆压缩；
  3. 归你所有 —— 本地存档、密钥进钥匙串、MIT 开源、随时导出。
- **地基**（信任背书）：MIT、Python 3.10+、多模型（OpenAI / Claude / Ollama）、CLI + Web 双形态。

## 4. 差异化锚点

对三类替代品各立一个"反方"：传统文字冒险（剧本写死）、通用 AI 聊天扮演（转身就忘）、云端 AI 游戏（数据不在你手里）。落地页 `#compare` 对照表是对外统一话术，投放素材请与该表保持一致。

## 5. 转化路径与指标

页面按「认知 → 兴趣 → 激活」设计三级 CTA：

1. **主 CTA**：`pip install lonely-world`（一键复制）→ 激活
2. **次 CTA**：GitHub 查看源码 / Star → 建立信任、社区资产
3. **兜底 CTA**：Web UI 路径（`lonely-world-web`）→ 降低命令行门槛

建议北极星指标：**周活跃故事数（完成首局的存档）**。

漏斗参考：页面 UV → 复制安装命令 → `pip install` → 完成首局（激活）→ 7 日回访 → GitHub Star / Issue 反馈。

## 6. 渠道建议

- **GitHub / PyPI**：README 顶部挂本页链接与一句话定位；PyPI description 同步。
- **中文社区**：少数派、V2EX、即刻、小红书、B 站（终端录屏演示效果最好，可用页面终端动画的脚本做分镜）。
- **英文社区**（配合 i18n 后）：r/interactivefiction、Hacker News（Show HN，主打 open-source + local-first）。

## 7. 发布 Checklist

- [ ] 页面中的版本号与最新 Release 保持同步（当前 v0.2.0）
- [ ] GitHub 仓库简介、README、PyPI 三处话术对齐第 1 节
- [ ] 替换/补充真实社交证明（Star 数、玩家评价）后上线 `#trust` 区强化
- [ ] 接入基础统计（如 Cloudflare Analytics / umami），跟踪第 5 节漏斗
