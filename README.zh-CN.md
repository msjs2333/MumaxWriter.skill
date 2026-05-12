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
        parameter_sweep.md
        output_and_reproducibility.md
        compatibility_notes.md
      scripts/
        check_mx3_static.py
        render_template.py
        collect_case_status.py
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

这是 `v0.1.0` 公开快照。安装版 skill 现在已经在 `skills/mumax3/assets/templates/` 下包含通用 mumax3 模板，`skills/mumax3/references/api_patterns.md` 也已经扩展了常见 mumax3 API 组合、solver/output 选择、时间依赖场和高级功能的 pattern 覆盖；`skills/mumax3/scripts/` 现在包含确定性辅助脚本；仓库级 `examples/` 提供评估 prompt、预期输出、覆盖 catalog 和人工评估 checklist。

示例和静态检查只用于 skill 验证和脚本卫生检查，不证明物理正确性、数值收敛或论文级可用性。

## 参考文档

- [发布说明](docs/release_notes_v0.1.0.md)
- [示例 catalog](examples/catalog/README.md)
- [第三方来源说明](docs/third_party_sources.md)
- [故障排查](docs/troubleshooting.md)

## 许可证

本项目使用 [Apache License 2.0](LICENSE) 许可证。
