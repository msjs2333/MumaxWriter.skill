# mumax3 Skill 安装基线审计

审计日期：2026-08-17

## 1. 结论

当前通用 Skill 源码 `D:\Project\MumaxWriter.skill\skills\mumax3` 与安装版
`C:\Users\msjs2\.codex\skills\mumax3` 在排除 `__pycache__`、`.pyc`、`.pyo` 后均为 21 个维护文件，
相对路径、字节数和逐文件 SHA256 完全一致。该安装内容已固化为：

- 内容基线 commit：`883a144afdb2502d732865a27638d2de01eb8fbf`；
- annotated tag：`mumax3-installed-baseline-20260817`，解引用到上述 commit；
- 21 文件清单 SHA256：`6b72247bcd7858ede96125548a6ec2ff9014ced500e8df86af8dd224be7df67d`。

标签只指向安装内容提交；本文随后单独提交，以便记录真实基线 commit，避免在同一提交内写自引用哈希。

## 2. 仓库起点

| 项目 | 审计值 |
|---|---|
| 初始分支 | `main` |
| 初始 HEAD | `40711725a80f5071144b07c87c1ad9bac832fa23` |
| 初始 `origin/main` | `40711725a80f5071144b07c87c1ad9bac832fa23` |
| 初始 worktree | 仅 `D:/Project/MumaxWriter.skill` |
| 仓库指令 | allowlist 范围内未发现 `AGENTS.md` |
| 同步动作 | 仅 `--dry-run`；未执行 `--apply`，安装版保持只读 |

## 3. 基线提交范围

显式暂存并提交以下 14 个文件，没有使用 `git add -A` 或宽泛目录 glob：

| 文件 | 状态 | 纳入理由 |
|---|---|---|
| `CHANGELOG.md` | 修改 | 只记录本次通用 Skill 能力 |
| `README.md`、`README.zh-CN.md`、`README.ja.md` | 修改 | 同步列出新增 reference、同步工具和当前版本说明 |
| `skills/mumax3/SKILL.md` | 修改 | 项目发现、工作流路由、谱系和人工分类边界 |
| `skills/mumax3/references/api_index.md` | 修改 | 补全已验证的 spin-torque 标识符 |
| `skills/mumax3/references/api_patterns.md` | 修改 | region 覆盖和空间电流 mask 的通用复现约束 |
| `skills/mumax3/references/project_discovery.md` | 新增 | 仓库上下文发现和权威来源顺序 |
| `skills/mumax3/references/project_workflows.md` | 新增 | CLI、签名、续做、人工复核和测试分层 |
| `skills/mumax3/scripts/check_mx3_static.py` | 修改 | 模板占位符、大小写和 protected built-in 检查修正 |
| `skills/mumax3/scripts/collect_case_status.py` | 修改 | provenance、analysis freshness 和 manual review 摘要 |
| `skills/mumax3/scripts/sync_local_skill.py` | 新增 | 带备份、精确替换和 SHA 核验的本地同步 |
| `tests/test_helpers.py` | 新增 | static/status/sync helper 临时目录回归 |
| `tests/validate_release.py` | 修改 | 新 helper、临时目录排除和 unittest 纳入发布验证 |

以下既有未跟踪内容未读取大文件、未暂存、未删除：`.*_stage/`、`.*_staging/`、`.tmp_*`、`.claude/`、
`work/`、论文 PDF、全文 TXT 和其他项目暂存件。它们不属于 Skill 安装基线，继续由原作者管理。

## 4. 验证记录

| 验证 | 结果 |
|---|---|
| `python -m unittest discover -s tests -p "test_*.py"` | 通过；5 tests，`0.892 s` |
| `python tests\validate_release.py` | 通过；helper/template/static/sensitive-term 全绿 |
| `mumax3 -vet` | 发布验证内 7 个 expected-output `.mx3` 全通过 |
| `python skills\mumax3\scripts\sync_local_skill.py --dry-run` | `add=0 change=0 remove=0`，`Already synchronized` |
| 独立源码/安装版清单 | 各 21 文件；mismatch `0`；清单 SHA256 相同 |
| staged diff 范围 | 14 个 allowlist 文件，无 staging/work/论文材料 |

严格 `git diff --cached --check` 对新增的 `project_discovery.md:41` 报告 `new blank line at EOF`。该尾部空行是
审计前安装版的既有字节；源码文件 SHA256
`bc507777a54dd3438611fdeab43f1940c1965dbb537c326f89d4464203b392e7` 与安装版完全相同。去除此空行会破坏
“基线与安装版逐字节一致”，因此阶段 3.5 保留它并把例外显式记录；其余 staged 文件的严格 diff check 通过。
阶段 4 若要清理该格式，必须作为可见源码 diff，经验证和用户确认后再同步安装版。

## 5. 后续边界

- 从本文提交后的 `main` 创建 `codex/mumax3-skill-improvement-20260817` 和独立 worktree；
- 阶段 4 只在独立 worktree 改造，基线 tag 不移动、不重写；
- 用户确认阶段 4 diff 前不 fast-forward `main`、不执行同步 `--apply`；
- 未推送 commit、branch 或 tag；远端发布需要用户另行授权。
