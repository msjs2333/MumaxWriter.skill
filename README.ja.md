# MumaxWriter.skill

[English](README.md) | [中文](README.zh-CN.md) | 日本語

MumaxWriter.skill は、AI agent が mumax3 の `.mx3` シミュレーションスクリプトを作成、レビュー、パラメータ化、保守するための Codex skill プロジェクトです。

このリポジトリには MuMax3 agent skill、再利用可能な実例、独立した評価用プロンプトが含まれます。

## Repository Layout

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
    third_party_sources.md
    troubleshooting.md
  tests/
    validate_release.py
```

## What The Skill Does

- mumax3 `.mx3` スクリプトを作成する。
- mumax3 の構文や API のよくあるミスをレビューする。
- バッチシミュレーション用にスクリプトをパラメータ化する。
- mesh、geometry、material、initial state、field、output、run stage を整理する。
- 逐次スイープには MuMax3 のループ、独立ケースには必要に応じて Python orchestration を利用する。
- status/monitor や product-only plotting では、無関係な API、geometry history、大容量 field data を読まずに最小 context を選ぶ。
- single writer、入力の追跡可能性、目的に十分な証拠、人間と自動判定の分離を維持し、ハッシュやゲートは必要な場合に使う。
- task schema、background scheduling、storage/release、agent 分担は project guidance に委ね、reference は必要時に読む。

## Local Installation

Skill フォルダを Codex skills ディレクトリへコピーします。

```powershell
Copy-Item -Recurse .\skills\mumax3 C:\Users\<you>\.codex\skills\mumax3
```

その後、明示的に呼び出します。

```text
Use $mumax3 to write or review this mumax3 script.
```

MuMax3 本体は skill とは別にインストールします。環境確認、公式バイナリ、WSL・ソースビルド、Agent によるセットアップは短い[インストールガイド](skills/mumax3/references/installation.md)を参照してください。

## Quick Example

```text
Use $mumax3 to write a minimal mumax3 thin-film relaxation script with SI units, table output, and a final OVF save.
```

## Local Validation

Repository root で local validation を実行します。

```powershell
python tests\validate_release.py
python tests\validate_release.py --scope docs
python tests\validate_release.py --scope helpers
```

validator は Python standard library のみを使用します。既定の full は metadata/link、維持対象ファイルの機密項目、helper、template、static check、利用可能な vet を確認します。未実行の vet は skip と表示し、文書の固定文言や project 名 blacklist は検証対象にしません。docs は helper suite を実行しません。

## Current Status

最新の公開リリースは `v0.2.0` です。現在のソースには、連続ヒステリシス、標準問題 SP4 の磁場 1、パルス励起 macrospin FMR の[実例](skills/mumax3/references/worked_workflows.md)と解析・判定基準を追加しています。`skills/mumax3/` のコピーには教材と解析ツールが含まれ、独立した評価課題は `examples/prompts/` に残ります。

これらは汎用 guidance と validation surface です。各 research repository は state、lock、scientific decision、
output、retention の必要な実装と test をローカルに持つ必要があり、この skill 更新だけで project task code や
project data が移行済みになったとはみなしません。

Examples and static checks are for skill validation and script hygiene. They do not prove physical correctness, numerical convergence, or publication readiness.

## Future Roadmap

Planned directions for later releases:

- Evaluate optional Python-side data handling workflows, including possible use of the Ubermag ecosystem and related analysis tools.
- Add mumax+ compatibility, with the long-term direction of making mumax+ the primary target while keeping mumax3 support.
- Provide assisted migration workflows from existing mumax3 `.mx3` scripts to mumax+, including API mapping notes, behavior differences, and validation checklists.
- Expand postprocessing examples for OVF/table output, spectra, mode maps, texture tracking, and sweep summaries.

## References

- [Release notes v0.2.0](docs/release_notes_v0.2.0.md)
- [Release notes v0.1.0](docs/release_notes_v0.1.0.md)
- [Example catalog](examples/catalog/README.md)
- [Third-party sources](docs/third_party_sources.md)
- [Troubleshooting](docs/troubleshooting.md)

## License

Licensed under the [Apache License 2.0](LICENSE).
