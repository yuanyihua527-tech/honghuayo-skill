# honghuayo-skill

可供 AI 助手调用的实用技能集合。

## FDE 碰头会实用助手

把 FDE 碰头会的观点用到自己的行业和工作中。一个入口，包含需求澄清、试点选择、专家经验蒸馏、系统集成、客户沟通、价值核算、交付采用、工作台设计、行业复用和信息跟进十项能力。

- [查看技能](skills/fde-enterprise-ai/SKILL.md)
- [阅读中文精华说明](docs/fde-enterprise-ai-guide.md)

### 可以这样问

1. “我是做___行业的，这场活动有哪些观点对我有用？”
2. “用通俗的话讲讲，活动里最值得记住的5个观点。”
3. “我负责___，哪些工作可以先尝试用 AI 改进？”
4. “我遇到了___，结合活动里的方法，可以从哪一步开始？”
5. “帮我把___这个想法，拆成一周内能尝试的小计划。”

只调用技能而未附具体问题时，助手先给出上述使用提示；已有具体问题时直接处理。

### 安装与调用

在支持 skill-installer 的 Codex 中，可以直接对助手说：

> 使用 skill-installer，从 GitHub 仓库 yuanyihua527-tech/honghuayo-skill 安装 skills/fde-enterprise-ai。

也可以下载本仓库，将整个 `skills/fde-enterprise-ai` 文件夹放入所用 AI 助手的技能目录。保留子目录及配套文件，不要只复制 SKILL.md。具体技能目录以所用客户端为准。

安装后调用：

```text
使用 $fde-enterprise-ai，我是做装修建材的，负责客户沟通。
这场活动有哪些对我有用的观点？请给出几个可以尝试的做法。
```

### 文件结构

```text
skills/fde-enterprise-ai/
  SKILL.md                 使用入口、开场消息与任务路由
  agents/openai.yaml       中文显示信息及默认提示
  references/              十张能力卡、概览、词典与速查
  resources/               需求、试点、交接、案例模板及价值计算工具
docs/
  fde-enterprise-ai-guide.md
```

本技能以《FDE碰头会_姓名与识别校订版》为基础，结合分析补充成可执行方法。来源位置保留在能力卡中。配套表单、验收设计和计算口径已注明为实现补充；具体项目仍需结合自己的业务材料使用。

制作方法参考 [cangjie-skill](https://github.com/kangarooking/cangjie-skill)，相关许可见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。仓库不包含原始会议转写、私人资料或本地工作记录。
