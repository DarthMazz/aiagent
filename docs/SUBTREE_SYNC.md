# git subtree による `.github` / `docs` 同期手順

このリポジトリをテンプレートとして使い、他のリポジトリへ `.github` と `docs` だけを同期するための手順です。

## 前提

- 配布元: このテンプレートリポジトリ（例: `DarthMazz/aiagent`）
- 配布先: テンプレートの設定を取り込みたい各リポジトリ
- 同期対象:
  - `.github`
  - `docs`

`git subtree` はリポジトリ全体ではなく、**ディレクトリ単位で split したブランチ**を経由して同期します。そのため、まずテンプレート側で配布用ブランチを作成・更新します。

## 全体像

1. テンプレート側で `.github` と `docs` の split ブランチを作る
2. 配布先リポジトリでそのブランチを `git subtree add` する
3. テンプレート更新時に split ブランチを更新する
4. 配布先リポジトリで `git subtree pull` する

## 1. テンプレート側: 配布用ブランチを作る

このリポジトリで実行します。

```bash
git subtree split --prefix=.github -b subtree/github
git subtree split --prefix=docs -b subtree/docs
git push origin subtree/github --force-with-lease
git push origin subtree/docs --force-with-lease
```

### ブランチの役割

| ブランチ | 内容 |
| --- | --- |
| `subtree/github` | `.github` ディレクトリだけを切り出した履歴 |
| `subtree/docs` | `docs` ディレクトリだけを切り出した履歴 |

## 2. 配布先リポジトリ: 初回取り込み

配布先リポジトリで実行します。

```bash
git remote add aiagent-template git@github.com:DarthMazz/aiagent.git
git fetch aiagent-template
git subtree add --prefix=.github aiagent-template subtree/github --squash
git subtree add --prefix=docs aiagent-template subtree/docs --squash
```

### 補足

- `--squash` を付けると、配布先リポジトリの履歴を見やすく保てます
- `.github` または `docs` がすでに存在する場合、`git subtree add` は失敗しやすいため、初回は既存内容を退避・整理してから実行してください

既存ディレクトリを置き換える場合の一例です。

```bash
mv .github .github.backup
mv docs docs.backup
git add .github.backup docs.backup
git commit -m "chore: backup local .github and docs before subtree adoption"
```

その後に `git subtree add` を実行し、必要な差分だけを手で戻します。

## 3. テンプレート更新時: 配布用ブランチを更新する

テンプレート側で `.github` または `docs` を更新したら、再度 split して push します。

```bash
git subtree split --prefix=.github -b subtree/github
git subtree split --prefix=docs -b subtree/docs
git push origin subtree/github --force-with-lease
git push origin subtree/docs --force-with-lease
```

運用上は、テンプレートの main ブランチに変更を取り込んだあとにこの更新を行います。

## 4. 配布先リポジトリ: 更新を取り込む

配布先リポジトリで実行します。

```bash
git fetch aiagent-template
git subtree pull --prefix=.github aiagent-template subtree/github --squash
git subtree pull --prefix=docs aiagent-template subtree/docs --squash
```

## コンフリクト対応

- 配布先で同期対象ファイルを直接編集していると、`git subtree pull` 時に競合することがあります
- 競合が発生したら通常の Git コンフリクトと同様に解消し、コミットします
- 長期運用では、テンプレートから配る内容と配布先固有の内容をできるだけ分離するのが安全です

## 推奨運用

1. テンプレート側で `.github` と `docs` をメンテナンスする
2. 変更後に split ブランチを更新する
3. 配布先では `git subtree pull` だけで追従する
4. 配布先固有の設定は、テンプレート管理対象とファイルを分ける

## よく使うコマンド一覧

### テンプレート側

```bash
git subtree split --prefix=.github -b subtree/github
git subtree split --prefix=docs -b subtree/docs
git push origin subtree/github --force-with-lease
git push origin subtree/docs --force-with-lease
```

### 配布先側

```bash
git remote add aiagent-template git@github.com:DarthMazz/aiagent.git
git fetch aiagent-template
git subtree add --prefix=.github aiagent-template subtree/github --squash
git subtree add --prefix=docs aiagent-template subtree/docs --squash
git subtree pull --prefix=.github aiagent-template subtree/github --squash
git subtree pull --prefix=docs aiagent-template subtree/docs --squash
```
