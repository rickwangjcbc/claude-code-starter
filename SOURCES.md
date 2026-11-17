# 根拠と適用範囲

公式資料:
- https://code.claude.com/docs/en/best-practices
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/permissions
- https://code.claude.com/docs/en/security
- https://code.claude.com/docs/en/hooks

この配布物は上記の機構を利用する独自のチーム標準雛形であり、公式配布物・組織承認済み標準ではない。
team-で始まるSkillは本配布物の独自Skill。組込みコマンドの名称との衝突を避けている。
Hooksは初期状態では設定しない。技術スタックが不明な段階で整形や検査を全編集へ自動適用しないため。
Hooksを追加する場合は公式イベントスキーマ・標準入力JSON・失敗動作を対象版で確認し、fixtureと実CLIの両方で検証する。
バージョンや既定の権限モードは変化する。対象版で読込と許可/拒否の動作を確認する。
