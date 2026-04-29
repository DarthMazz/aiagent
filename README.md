# AI Agent Template

Python開発用のAIエージェントテンプレート。ドメイン駆動設計（DDD）とヘキサゴナルアーキテクチャに基づいた開発ガイドラインを提供します。

## 特徴

- **Python 3.12+** 対応
- **PEP 8** コーディング規約準拠
- **ドメイン駆動設計（DDD）** のベストプラクティス
- **ヘキサゴナルアーキテクチャ** 採用
- **uv** による高速パッケージ管理
- **ruff** による Lint とフォーマット
- **pytest** によるテスト

## ドキュメント

- [RULES.md](docs/RULES.md) - 開発ルールとガイドライン
- [SKILLS.md](docs/SKILLS.md) - AIエージェントのスキル定義
- [Copilot Instructions](.github/copilot-instructions.md) - GitHub Copilot 設定

## 使い方

### 前提条件

- Python 3.12 以上
- [uv](https://github.com/astral-sh/uv) のインストール

### セットアップ

```bash
# リポジトリのクローン
git clone <repository-url>
cd aiagent

# 仮想環境の作成
uv venv

# 依存関係のインストール
uv sync
```

### 開発

```bash
# Lintチェック
uv run ruff check .

# 自動修正
uv run ruff check --fix .

# フォーマット
uv run ruff format .

# テスト実行
uv run pytest
```

## アーキテクチャ

このテンプレートは、ヘキサゴナルアーキテクチャ（ポート&アダプターパターン）を採用しています：

```
project/
├── domain/              # ドメイン層（コアビジネスロジック）
│   ├── entities/        # エンティティ
│   ├── value_objects/   # 値オブジェクト
│   ├── repositories/    # リポジトリインターフェース
│   ├── services/        # ドメインサービス
│   └── events/          # ドメインイベント
├── application/         # アプリケーション層（ユースケース）
│   ├── use_cases/       # ユースケース
│   └── dto/             # データ転送オブジェクト
├── infrastructure/      # インフラ層（技術的実装）
│   ├── persistence/     # データベース実装
│   └── messaging/       # メッセージング実装
└── adapters/            # アダプター層（外部接続）
    ├── api/             # REST API、GraphQL等
    ├── cli/             # コマンドラインインターフェース
    └── ui/              # ユーザーインターフェース
```

## ライセンス

MIT License

## 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずissueを開いて変更内容を議論してください。
