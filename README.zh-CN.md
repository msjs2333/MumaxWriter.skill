# MumaxWriter.skill

[English](README.md) | 中文 | [日本語](README.ja.md)

这是一个 Codex skill 项目，用于帮助 AI agent 编写、审查、参数化和维护 mumax3 `.mx3` 微磁学仿真脚本。

当前仓库包含一个已清理的通用 `mumax3` skill；项目专用研究材料已从公开快照中移除，安装版 skill 路径保持通用化。

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
        project_discovery.md
        project_workflows.md
        parameter_sweep.md
        output_and_reproducibility.md
        compatibility_notes.md
      scripts/
        check_mx3_static.py
        render_template.py
        collect_case_status.py
        sync_local_skill.py
  docs/
    release_notes_v0.1.0.md
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
- 在参数扫描、拟合、绘图和结果整理场景中建议使用 Python 包装 mumax3。

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

## 快速示例

```text
Use $mumax3 to write a minimal mumax3 thin-film relaxation script with SI units, table output, and a final OVF save.
```

参数扫描任务应让 Python 负责 case 生成、metadata、日志和后处理；每个仿真仍保持为原生 mumax3 `.mx3` 脚本。

## 本地验证

在仓库根目录运行本地验证：

```powershell
python tests\validate_release.py
```

该验证脚本只使用 Python 标准库。它会编译 helper 脚本、检查模板参数示例、对 expected-output `.mx3` 做保守静态检查，并在本地 `PATH` 中存在 mumax3 时运行 `mumax3 -vet`。

## 当前状态

最近的标签与元数据版本为 `v0.1.1`。此后的工作树增加了项目上下文发现、签名感知的任务工作流、安全本地同步和辅助工具回归测试，同时继续保持公开 skill 与具体研究项目解耦。

示例和静态检查只用于 skill 验证和脚本卫生检查，不证明物理正确性、数值收敛或论文级可用性。

如果项目提供 `docs/mumax3_reference/current_project_context.md`，skill 会把该项目内文件及其链接的活动源码视为高于通用示例的权威依据。

## 引用

如果你在科研、教学或公开工作流中使用这个 skill，请使用 [`CITATION.cff`](CITATION.cff) 中的元数据引用本仓库。GitHub 应会通过仓库页面的 “Cite this repository” 按钮显示这些引用信息。

本项目已为 Zenodo 软件归档做好准备。Zenodo 为 `v0.1.1` release 分配 DOI 后，再把 DOI badge 和 DOI 链接补充到本节。

## 未来规划

后续版本计划方向：

- 评估 Python 侧数据处理工作流，包括将 Ubermag 生态及相关分析工具作为可选方案。
- 增加 mumax+ 兼容能力；当前仍以 mumax3 为主，长期方向是逐步转向以 mumax+ 为主，同时保留 mumax3 支持。
- 提供从现有 mumax3 `.mx3` 脚本迁移到 mumax+ 的辅助工作流，包括 API 映射、行为差异和验证 checklist。
- 扩展 OVF/table 后处理示例，例如频谱、模式图、磁结构位置追踪和参数扫描汇总。

## 参考文档

- [v0.1.1 发布说明](docs/release_notes_v0.1.1.md)
- [v0.1.0 发布说明](docs/release_notes_v0.1.0.md)
- [示例 catalog](examples/catalog/README.md)
- [第三方来源说明](docs/third_party_sources.md)
- [故障排查](docs/troubleshooting.md)

## 许可证

本项目使用 [Apache License 2.0](LICENSE) 许可证。
