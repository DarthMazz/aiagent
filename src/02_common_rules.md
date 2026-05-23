# 共通ガードレール

Python開発・DDD・コマンド実行・セキュリティに関するエージェント共通の行動ルールを定義します。

## Python 開発基本ルール

- **Pythonバージョン**: Python 3.12 以上
- **仮想環境**: `uv venv` / `uv sync` を使用（pip 直接使用禁止）
- **依存関係**: `pyproject.toml` で管理、`requirements.txt` は使用しない
- **エンコーディング**: すべてのソースファイルは UTF-8

## コード品質ルール

- **型ヒント**: すべての関数・メソッドに型ヒントを付ける
- **Docstring**: すべての関数・クラス・モジュールに記述（引数・戻り値・例外を明記）
- **例外処理**: 具体的な例外をキャッチする（bare `except:` 禁止）
- **最小変更**: 目的を達成するために最小限の変更のみ行う
- **既存機能の保持**: 動作中のコードを壊さない

## Lint・フォーマットルール

```bash
uv run ruff check .          # Lintチェック
uv run ruff check --fix .    # 自動修正
uv run ruff format .         # フォーマット
```

コード変更後は必ず `uv run ruff check .` を実行し、コミット前にエラーをゼロにする。

`pyproject.toml` での設定:
```toml
[tool.ruff]
line-length = 88
target-version = "py312"
```

## 依存関係管理ルール

```bash
uv venv            # 仮想環境作成
uv sync            # 依存関係インストール（クローン後・変更後）
uv add <pkg>       # パッケージ追加
uv add --dev <pkg> # 開発用パッケージ追加
uv remove <pkg>    # パッケージ削除
uv run <cmd>       # プロジェクトのコンテキストでコマンド実行
```

`uv.lock` はコミットする。

## テストルール

- フレームワーク: pytest
- ファイル命名: `test_*.py` または `*_test.py`
- TDD実践: Red（失敗テスト）→ Green（最小実装）→ Refactor
- ユニットテスト: ドメインロジックをリポジトリ/外部サービスのモックで独立させる
- コミット前に全テストがパスすること

## ドメイン駆動設計（DDD）ルール

### ヘキサゴナルアーキテクチャ構造

```
project/
├── domain/              # コアビジネスロジック（外部依存なし）
│   ├── entities/        # エンティティ
│   ├── value_objects/   # 値オブジェクト
│   ├── repositories/    # リポジトリインターフェース
│   ├── services/        # ドメインサービス
│   └── events/          # ドメインイベント
├── application/         # ユースケース（ドメイン層のみに依存）
│   ├── use_cases/
│   └── dto/
├── infrastructure/      # 技術的実装（ポートを実装）
│   ├── persistence/
│   └── messaging/
└── adapters/            # 外部接続
    ├── api/
    ├── cli/
    └── ui/
```

**依存関係の方向**: 常に内側（ドメイン）に向かう。ドメイン層は他層に依存しない。

### 戦術的設計パターン

**エンティティ** — UUID を持つ識別可能なオブジェクト:
```python
from dataclasses import dataclass
from uuid import UUID

@dataclass
class Order:
    id: UUID
    customer_id: UUID
```

**値オブジェクト** — 不変・属性で識別:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Email:
    address: str

    def __post_init__(self):
        if '@' not in self.address:
            raise ValueError("Invalid email")
```

**リポジトリインターフェース** — Protocol を使用:
```python
from typing import Protocol
from uuid import UUID

class OrderRepository(Protocol):
    def find_by_id(self, order_id: UUID) -> Order | None: ...
    def save(self, order: Order) -> None: ...
```

**ドメインイベント** — 過去形・不変:
```python
@dataclass(frozen=True)
class OrderPlaced:
    order_id: UUID
    placed_at: datetime
```

### 命名規則

| 概念 | パターン | 例 |
|---|---|---|
| エンティティ | 名詞 | `User`, `Order` |
| 値オブジェクト | 概念名詞 | `Email`, `Money`, `OrderStatus` |
| リポジトリ | `{Entity}Repository` | `OrderRepository` |
| ドメインサービス | `{Action}Service` | `PricingService` |
| ユースケース | `{Verb}{Noun}UseCase` | `CreateOrderUseCase` |
| ドメインイベント | 過去形 | `OrderPlaced`, `PaymentProcessed` |

## コマンド実行ポリシー

### 承認不要（読み取り専用）

- ファイル参照: `ls`, `cat`, `head`, `tail`, `find`, `grep`, `diff`, `tree`
- Git 読み取り: `git status`, `git log`, `git diff`, `git branch`, `git show`
- Python/uv 読み取り: `uv pip list`, `uv pip show`, `uv run ruff check .`, `uv run pytest --collect-only`
- システム情報: `echo`, `ps`, `which`

### 実行前に確認が必要（書き込み操作）

- ファイル変更: `rm`, `mv`, `cp`（上書き時）
- パッケージ操作: `uv add`, `uv remove`
- Git 書き込み: `git commit`, `git push`, `git reset`, `git rebase`
- 自動修正: `ruff check --fix`, `ruff format`
- データベース変更操作

## セキュリティルール

- 認証情報・機密データをコミットしない
- コマンド実行前にユーザー入力を検証する
- 変更時には既存ファイルを保持する
- 確認なしに破壊的操作を行わない

## AI駆動開発ライフサイクル（AIDLC）

### フェーズ1: 要件定義
- ユーザーストーリー形式で記述: `〜として、〜したい、なぜなら〜`
- 受け入れ条件（Acceptance Criteria）を明確にする
- 曖昧な要件は実装前に確認する

### フェーズ2: 設計
- DDDコンテキストマップを先に定義する
- 重要な決定はADRに記録: `docs/adr/ADR-NNN-title.md`
  ```markdown
  # ADR-001: タイトル
  ## ステータス: 採用
  ## 背景: ...
  ## 決定: ...
  ## 理由: ...
  ## トレードオフ: ...
  ```

### フェーズ3: 実装
- Red → Green → Refactor サイクルで進める
- 小さい単位で実装・確認を繰り返す
- AI生成コードは必ず人間がレビューしてから採用する

### フェーズ4: テスト・検証
- 全テストパス + Lintエラーゼロ でコミット

### フェーズ5: リファクタリング
- ドメイン理解が深まったらコードに反映
- ユビキタス言語と集約境界を継続的に見直す

### フェーズ6: 振り返り
- 有効だったパターンを `src/` に反映
- プロンプトの改善点を記録する
