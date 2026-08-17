# mumax3 Skill 改造发布审计

审计日期：2026-08-17

## 1. 发布结论

阶段 4 已按批准范围完成。`main` 从 `ccca7d7756726bb1696bad375f023536dfa7ba66`
纯快进到内容提交 `0922ebd33b0a6154f6c293ab3cd5509291400f9d`，随后通过维护脚本将
`D:\Project\MumaxWriter.skill\skills\mumax3` 同步到
`C:\Users\msjs2\.codex\skills\mumax3`。同步后源码与安装版的 21 个维护文件在相对路径、
字节数和逐文件 SHA256 上完全一致，差异数为 `0`。

- 批准 diff：`ccca7d7..0922ebd`，5 个提交、10 个文件、`+494/-31`；
- 内容标签：`mumax3-skill-improvement-20260817`，解引用到 `0922ebd…`；
- 21 文件清单 SHA256：`623dd6b4054df4ffe3e117053fddd97dc28e7f9326377447a8cb1b3feb7a0c89`；
- 同步备份：`C:\Users\msjs2\.codex\skills\.mumax3-backups\mumax3-20260817-152203`。

标签固定实际发布内容；本文在标签之后单独提交，避免发布内容提交自引用审计哈希。

## 2. 审查与批准

Claude 对 `ccca7d7..0922ebd` 做了全程只读独立审查，结论为“通过”，未发现阻断问题；其三项
非阻断建议经本对话独立判断均不构成本次发布前置条件，因此未扩大已审查 diff。用户随后明确批准执行
快进与同步。

五个内容提交保持单一意图和计划顺序：

| 提交 | 内容 |
|---|---|
| `c3485dd` | 将任务意图路由到四大安全护栏 |
| `378128d` | 定义安全任务工作流合同 |
| `8e5a053` | 定义输出谱系与留存合同 |
| `0139125` | 增加工作流安全合同回归测试 |
| `0922ebd` | 更新发布说明与多语言 README |

## 3. 主分支发布门禁

| 检查 | 主分支复验结果 |
|---|---|
| `python -m unittest discover -s tests -p "test_*.py"` | 9/9 通过 |
| `python tests\validate_release.py` | 全部通过；含合同、链接、项目独立性、helper、模板及 7 个 expected-output 的 `mumax3 -vet` |
| `python skills\mumax3\scripts\sync_local_skill.py --dry-run` | 同步前仅 4 个维护文件变化，`add=0 change=4 remove=0` |
| `git diff --check` | 通过 |
| 三个 CDW 代表模板 | 渲染完成，静态检查无警告，MuMax3 3.12 `-vet` 全通过 |

代表模板为 `ellipse_ku_pinned_dw_lens_weakwave.mx3.template`、
`dmi2p4_f050_strongdrive_hy_compensation.mx3.template` 和
`bimeron_current_nucleation_stage.mx3.template`。验证仅在系统临时目录生成小型 `.mx3`，结束后按唯一目录
精确清理；未读取或修改正式 `runs\`、`results\` 及其中数据。

## 4. 同步与独立核对

同步严格使用：

```text
python skills\mumax3\scripts\sync_local_skill.py --apply
```

脚本报告仅以下 4 个维护文件变化，无新增或删除：

- `SKILL.md`
- `references/output_and_reproducibility.md`
- `references/project_discovery.md`
- `references/project_workflows.md`

同步后另行枚举两侧文件，排除 `__pycache__`、`.pyc`、`.pyo`，按大小写不敏感的相对路径排序，
以 `相对路径<TAB>字节数<TAB>文件SHA256` 拼接后计算清单 SHA256。结果如下：

| 项目 | 源码 | 安装版 |
|---|---:|---:|
| 文件数 | 21 | 21 |
| 清单 SHA256 | `623dd6b…a0c89` | `623dd6b…a0c89` |
| 路径/字节数/逐文件 SHA256 差异 | 0 | 0 |

同步后再次执行 dry-run，结果为 `add=0 change=0 remove=0`、`Already synchronized`。

## 5. 边界与后续

- 保留主工作树中既有未跟踪 staging/work 内容，未暂存、删除或纳入提交；
- 未修改 Skill 源码目录之外的运行逻辑；本审计文件是计划内项目维护记录；
- 未推送分支、提交或标签到远端；
- 阶段 4.5 尚未开始，须按已确认的执行计划另行进入。
