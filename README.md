# AI Agent Rules

Copilot・Kiro などの AI エージェント向けルールを一元管理し、`deploy.py` で各プロジェクトへ配布するリポジトリです。

## リポジトリ構成

```
├── src/
│   ├── 01_profile.md        # AIエージェントのプロフィール・ペルソナ（共通）
│   ├── 02_common_rules.md   # Python/DDD/コマンドポリシー等の共通ガードレール
│   ├── 03_copilot_spec.md   # Copilot固有のプロンプト仕様
│   └── 04_kiro_spec.md      # Kiro固有のプロンプト仕様
├── templates/
│   ├── copilot-local.tmpl   # プロジェクト固有Copilotルールの雛形
│   └── kiro-local.tmpl      # プロジェクト固有Kiroルールの雛形
├── deploy.py                # ビルド・配置スクリプト
└── docs/
    └── SUBTREE_SYNC.md      # git subtree による同期手順
```

## deploy.py の使い方

```bash
# ベースルールをユーザー共通設定へ書き込む
#   01_profile.md + 02_common_rules.md → ~/.config/universal-agent-rules/base_rules.md
python3 deploy.py base

# 指定リポジトリへ Copilot / Kiro ルールを配置する
#   03_copilot_spec.md → {repo}/.github/copilot-instructions.md
#   04_kiro_spec.md    → {repo}/.kiro/rules.md
python3 deploy.py repo /path/to/your/project

# base + repo を一括実行
python3 deploy.py all /path/to/your/project

# 複数リポジトリへ一括配置
python3 deploy.py repo /path/to/project-a /path/to/project-b
```

## 新しいプロジェクトへ適用する手順

1. このリポジトリをクローンまたは git subtree で取り込む
2. `python3 deploy.py base` でユーザー共通設定を初期化（初回のみ）
3. `python3 deploy.py repo <対象リポジトリのパス>` でルールを配置する
4. 必要に応じて `templates/copilot-local.tmpl` / `kiro-local.tmpl` を参考に、プロジェクト固有ルールを追記する

## ルールの更新

`src/` 内のファイルを編集後、`deploy.py` を再実行して各環境へ反映します。

```bash
python3 deploy.py all /path/to/project
```

## git subtree による同期

このリポジトリをテンプレートとして他リポジトリへ `.github` / `docs` を同期する手順は [docs/SUBTREE_SYNC.md](docs/SUBTREE_SYNC.md) を参照してください。

## ライセンス

MIT License
