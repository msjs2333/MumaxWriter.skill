# MumaxWriter.skill

[English](README.md) | [中文](README.zh-CN.md) | 日本語

MumaxWriter.skill は、AI agent が mumax3 の `.mx3` シミュレーションスクリプトを作成、レビュー、パラメータ化、保守するための Codex skill プロジェクトです。

このリポジトリには、汎用化された `mumax3` skill が含まれています。プロジェクト固有の研究資料は公開用スナップショットから除外し、インストール対象の skill パスを汎用的な形に保っています。

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

## What The Skill Does

- mumax3 `.mx3` スクリプトを作成する。
- mumax3 の構文や API のよくあるミスをレビューする。
- バッチシミュレーション用にスクリプトをパラメータ化する。
- mesh、geometry、material、initial state、field、output、run stage を整理する。
- パラメータスイープ、フィッティング、可視化、出力整理には Python orchestration を使う方針を示す。

## Local Installation

Skill フォルダを Codex skills ディレクトリへコピーします。

```powershell
Copy-Item -Recurse .\skills\mumax3 C:\Users\<you>\.codex\skills\mumax3
```

その後、明示的に呼び出します。

```text
Use $mumax3 to write or review this mumax3 script.
```

## Quick Example

```text
Use $mumax3 to write a minimal mumax3 thin-film relaxation script with SI units, table output, and a final OVF save.
```

## Local Validation

Repository root で local validation を実行します。

```powershell
python tests\validate_release.py
```

この validator は Python standard library のみを使います。helper script の compile、template parameter example、expected-output `.mx3` の static check、利用可能な場合の `mumax3 -vet` を実行します。

## Current Status

これは `v0.1.0` public snapshot です。インストール対象 skill パスには、`skills/mumax3/assets/templates/` の下に汎用的な mumax3 テンプレートが追加され、`skills/mumax3/references/api_patterns.md` には一般的な mumax3 API pattern が拡充されています。`skills/mumax3/scripts/` には deterministic helper scripts があり、リポジトリレベルの `examples/` には evaluation prompt、expected output、coverage catalog、manual evaluation checklist が追加されています。

Examples and static checks are for skill validation and script hygiene. They do not prove physical correctness, numerical convergence, or publication readiness.

## Future Roadmap

Planned directions for later releases:

- Evaluate optional Python-side data handling workflows, including possible use of the Ubermag ecosystem and related analysis tools.
- Add mumax+ compatibility, with the long-term direction of making mumax+ the primary target while keeping mumax3 support.
- Provide assisted migration workflows from existing mumax3 `.mx3` scripts to mumax+, including API mapping notes, behavior differences, and validation checklists.
- Expand postprocessing examples for OVF/table output, spectra, mode maps, texture tracking, and sweep summaries.

## References

- [Release notes](docs/release_notes_v0.1.0.md)
- [Example catalog](examples/catalog/README.md)
- [Third-party sources](docs/third_party_sources.md)
- [Troubleshooting](docs/troubleshooting.md)

## License

Licensed under the [Apache License 2.0](LICENSE).
