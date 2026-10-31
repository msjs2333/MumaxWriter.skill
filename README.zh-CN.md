# MumaxWriter.skill

[English](README.md) | 中文 | [日本語](README.ja.md)

这是一个 Codex skill 项目，用于帮助 AI agent 编写、审查、参数化和维护 mumax3 `.mx3` 微磁学仿真脚本。

本仓库包含 MuMax3 agent skill、可复用的完整教学案例，以及独立的评估题。

## 仓库结构

```text
MumaxWriter.skill/
  README.md
  README.zh-CN.md
  README.ja.md
  examples/
    prompts/
    expected_outputs/
    catalog/
    manual_evaluation_checklist.md
  skills/
    mumax3/
      SKILL.md
      agents/
        openai.yaml
      assets/
        templates/
          minimal_relax.mx3.template
          thin_film_with_region.mx3.template
          local_ac_field.mx3.template
      references/
        language_subset.md
        anti_patterns.md
        api_index.md
        api_patterns.md
        api_full.md
        examples.md
        structures.md
        parameter_sweep.md
        output_and_reproducibility.md
        compatibility_notes.md
        installation.md
        worked_workflows.md
        case_status.md
      examples/
        hysteresis/
        standard_problem4/
        fmr/
      scripts/
        check_mx3_static.py
        render_template.py
        collect_case_status.py
        analyze_tutorial.py
        sync_local_skill.py
  docs/
    release_notes_v0.1.0.md
    release_notes_v0.2.0.md
    release_notes_v0.3.0.md
    third_party_sources.md
    troubleshooting.md
  tests/
    validate_release.py
```

## Skill 能做什么

- 编写有效的 mumax3 `.mx3` 脚本。
- 审查常见 mumax3 语法和 API 错误。
- 为批量仿真参数化脚本。
- 按 mesh、geometry、material、initial state、field、output、run stage 组织脚本。
- 原生循环适合顺序扫描，Python 可用于独立 case 编排、拟合与绘图。
- 让纯 status/monitor 和产品级绘图按最小上下文执行，不默认加载无关 API、几何历史或大体积场数据。
- 简短保留单 writer、输入可追溯、证据充分及人工/自动结论分离；具体哈希与门禁按任务需要采用。
- 项目字段、后台调度、备份/释放协议和代理分工交由项目指导；通用参考按请求加载，不强制每个任务采用同一框架。

## 本地安装

将 skill 文件夹复制到 Codex skills 目录：

```powershell
Copy-Item -Recurse .\skills\mumax3 C:\Users\<you>\.codex\skills\mumax3
```

然后显式调用：

```text
Use $mumax3 to write or review this mumax3 script.
```

已有安装可先预览，再执行带备份的精确同步：

```powershell
python skills\mumax3\scripts\sync_local_skill.py --dry-run
python skills\mumax3\scripts\sync_local_skill.py --apply
```

应用同步前会备份当前 `.../skills/mumax3`，替换后再校验源码与安装目录的文件哈希。

## 从 Codex Marketplace 安装

通过 GitHub 安装 standalone skill：

```powershell
npx codex-marketplace add msjs2333/MumaxWriter.skill/skills/mumax3 --skill
```

然后显式调用：

```text
Use $mumax3 to write or review this mumax3 script.
```

MuMax3 模拟器需要单独安装。请按需阅读简短的[安装指南](skills/mumax3/references/installation.md)，其中说明环境检查、官方预编译包、WSL/源码编译路线和 Agent 辅助安装。

## 快速示例

```text
Use $mumax3 to write a minimal mumax3 thin-film relaxation script with SI units, table output, and a final OVF save.
```

顺序扫描可直接使用 MuMax3 循环；独立 case 可选 Python 编排。状态助手仅适用于其约定目录，不是任意 `.out` 扫描器，使用前查看 `--help`。

## 本地验证

在仓库根目录运行本地验证：

```powershell
python tests\validate_release.py
# 仅文档改动
python tests\validate_release.py --scope docs
# helper 改动（内部只跑一次 helper 测试）
python tests\validate_release.py --scope helpers
```

验证脚本只用 Python 标准库。默认 full 检查元数据/链接、维护文件敏感项、helper 行为、模板、静态告警及可用的引擎 vet；缺失检查明确记为 skip，不冒充通过。docs 范围不运行 helper 套件，不再锁定精确文案或项目禁词。

## 当前状态

当前版本为 `v0.3.0`，新增[完整工作案例](skills/mumax3/references/worked_workflows.md)：连续磁滞、标准问题 SP4 的场 1，以及脉冲激励的宏自旋 FMR，包含数据分析与明确的验收边界。复制 `skills/mumax3/` 即包含教学案例和分析工具；独立评估题保留在 `examples/prompts/`。

这些内容是通用指南和验证接口。具体研究仓库仍须在本地实现并测试适用的状态、锁、科学决策、输出和留存行为；
本次通用 skill 更新不表示任何项目任务代码或项目数据已经迁移。

示例和静态检查只用于 skill 验证和脚本卫生检查，不证明物理正确性、数值收敛或论文级可用性。

从相关项目指导和活动任务源码开始，不要求特定上下文文件名，也不默认全读无关历史。

## 未来规划

后续版本计划方向：

- 评估 Python 侧数据处理工作流，包括将 Ubermag 生态及相关分析工具作为可选方案。
- 增加 mumax+ 兼容能力；当前仍以 mumax3 为主，长期方向是逐步转向以 mumax+ 为主，同时保留 mumax3 支持。
- 提供从现有 mumax3 `.mx3` 脚本迁移到 mumax+ 的辅助工作流，包括 API 映射、行为差异和验证 checklist。
- 扩展 OVF/table 后处理示例，例如频谱、模式图、磁结构位置追踪和参数扫描汇总。

## 参考文档

- [v0.3.0 发行说明](docs/release_notes_v0.3.0.md)：参数一致性、随 skill 安装的建模与分析案例及验证范围。
- [v0.2.0 发布说明](docs/release_notes_v0.2.0.md)
- [v0.1.0 发布说明](docs/release_notes_v0.1.0.md)
- [示例 catalog](examples/catalog/README.md)
- [第三方来源说明](docs/third_party_sources.md)
- [故障排查](docs/troubleshooting.md)

## 许可证

本项目使用 [Apache License 2.0](LICENSE) 许可证。
