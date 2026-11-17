# Claude Code 開発標準スターター v1.0

そのまま再利用できる共通ルール・Skills・依頼文・品質検査のセットです。特定言語のアプリは含みません。
**既存案件を安全に調査して適用するための雛形であり、未設定の案件テストを成功扱いしません。**

## 最短の使い方
1. 新規案件は本フォルダーを案件の出発点にします。既存案件では、担当者または開発エージェントが同名ファイル・差分を確認し、手動でマージします。丸ごと上書きしないでください。
2. `prompts/00-bootstrap.md` の依頼文をClaude Codeへ渡します。手動で多数の設定ファイルを埋める代わりに、既存コードから調査できる部分を設定させます。
3. 重要な未決事項を確認し、`docs/SETUP.md` の導入判定を満たします。人の承認者や権限は推測しません。
4. 機能追加・修正・レビューには `prompts/` の依頼文を使います。

Slackを窓口にする運用では、この一式と導入依頼をPMへ渡せます。人の承認はSlackで行う設計にできますが、認証・信頼確認・承認中継の実装は本配布物に含みません。対象環境の実現可否は別途確認が必要です。

## 構成（主要ファイル）
```text
CLAUDE.md                       案件共通の短いルール
.claude/settings.json            共有権限設定・初期は広い自動許可なし
.claude/rules/security.md        共通セキュリティ規則
.claude/skills/team-*/SKILL.md    計画・実装・不具合・レビュー・引継ぎ
prompts/                        そのまま渡せる依頼文
project-checks.json             案件の実検証コマンド（初期は空）
scripts/checks.py               雛形検査・案件コマンド実行
 tests/test_starter.py           検査ツールの回帰試験
 templates/TASK.md               タスクと受入条件の雛形
 docs/PROJECT.md                 案件情報と導入状態
 docs/SETUP.md                   導入・検証・運用手順
.github/                        PR票とCI（GitHub利用時）
SOURCES.md                      公式資料と制約
```

## 使える独自Skills
全て明示起動専用です。自動起動を制限してもセキュリティ権限を保証するものではありません。
- `/team-plan 要件の概要` : 調査と計画。コード変更なし。
- `/team-implement タスク文書` : 受入条件に沿う実装と検証。
- `/team-fix-bug 症状` : 再現、原因調査、最小修正、回帰確認。
- `/team-review 比較元と対象` : 差分レビュー。編集なし。
- `/team-handoff 現在の作業` : commit・証跡・未決事項の引継ぎ。

## 検証コマンド（担当者・エージェント向け）
プロジェクトルートで実行します。Python 3.10以上、外部Pythonパッケージ不要。
```bash
python3 scripts/checks.py template
python3 -m unittest discover -s tests -v
python3 scripts/checks.py app
```
`python3`を使わないWindows環境では、利用可能なPython 3ランチャーへ読み替えます。アプリ側ランタイムは案件に合わせて追加します。

- template: ファイル存在・JSON・Skillヘッダーの軽量検査。意味的品質や実CLI読込の保証ではありません。
- unittest: 同梱の検査ツールの回帰試験。業務アプリの受入ではありません。
- app: 設定した実コマンドを順番に実行。空設定・不正設定・起動不能はBLOCKED（終了2）、実検査失敗は終了1。

初期状態で application-checks CI が失敗するのは意図した動作です。案件の実検証を設定していないのに緑へ見せないためです。

## 検証済みと未検証
作成時の実行結果は `VERIFICATION.md` を参照してください。Claude Code本体の読込、GitHub上でのCI・保護ルール、対象アプリの受入は各環境で確認が必要です。
