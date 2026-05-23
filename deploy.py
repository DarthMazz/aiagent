#!/usr/bin/env python3
"""
deploy.py — AIエージェントルールを各環境へ配置するビルドスクリプト。

使い方:
  python deploy.py base              # ベースルールを ~/.config/universal-agent-rules/base_rules.md へ書き込む
  python deploy.py repo <path...>    # 指定リポジトリへ Copilot / Kiro ルールを配置する
  python deploy.py all <path...>     # base + repo を一括実行する
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# --- パス定義 -----------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent.resolve()
SRC_DIR = SCRIPT_DIR / "src"

PROFILE_MD = SRC_DIR / "01_profile.md"
COMMON_RULES_MD = SRC_DIR / "02_common_rules.md"
COPILOT_SPEC_MD = SRC_DIR / "03_copilot_spec.md"
KIRO_SPEC_MD = SRC_DIR / "04_kiro_spec.md"

BASE_RULES_PATH = Path.home() / ".config" / "universal-agent-rules" / "base_rules.md"

COPILOT_INSTRUCTIONS_RELPATH = Path(".github") / "copilot-instructions.md"
KIRO_RULES_RELPATH = Path(".kiro") / "rules.md"

# --- ヘルパー -----------------------------------------------------------


def read(path: Path) -> str:
    """ファイルを読み込んで内容を返す。"""
    return path.read_text(encoding="utf-8")


def write(path: Path, content: str) -> None:
    """ファイルに内容を書き込む。親ディレクトリが存在しない場合は作成する。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  Written: {path}")


def build_copilot_instructions(copilot_spec: str) -> str:
    """copilot-instructions.md の内容を組み立てる。"""
    global_ref_note = (
        "## Global Reference\n\n"
        "エージェントは必ず次のユーザー共通設定も読み込み、"
        "最優先のガードレールとして従ってください: "
        "`~/.config/universal-agent-rules/base_rules.md`"
    )
    return f"# Local Project Rules\n\n{copilot_spec.strip()}\n\n{global_ref_note}\n"


# --- コマンド実装 -------------------------------------------------------


def cmd_base() -> int:
    """ベースルール（プロフィール + 共通ルール）を ~/.config へ書き込む。"""
    print("=== Deploying base rules ===")

    for path in (PROFILE_MD, COMMON_RULES_MD):
        if not path.exists():
            print(f"  ERROR: {path} not found.", file=sys.stderr)
            return 1

    profile = read(PROFILE_MD)
    common = read(COMMON_RULES_MD)
    combined = f"{profile.strip()}\n\n---\n\n{common.strip()}\n"

    write(BASE_RULES_PATH, combined)
    print("Done.")
    return 0


def cmd_repo(repo_paths: list[str]) -> int:
    """指定リポジトリへ Copilot / Kiro ルールを配置する。"""
    print("=== Deploying repo rules ===")

    for path in (COPILOT_SPEC_MD, KIRO_SPEC_MD):
        if not path.exists():
            print(f"  ERROR: {path} not found.", file=sys.stderr)
            return 1

    copilot_spec = read(COPILOT_SPEC_MD)
    copilot_content = build_copilot_instructions(copilot_spec)
    kiro_content = read(KIRO_SPEC_MD)

    errors = 0
    for raw_path in repo_paths:
        repo = Path(raw_path).resolve()
        if not repo.is_dir():
            print(f"  ERROR: {repo} is not a directory.", file=sys.stderr)
            errors += 1
            continue

        print(f"  Repository: {repo}")
        write(repo / COPILOT_INSTRUCTIONS_RELPATH, copilot_content)
        write(repo / KIRO_RULES_RELPATH, kiro_content)

    print("Done." if errors == 0 else f"Finished with {errors} error(s).")
    return 0 if errors == 0 else 1


def cmd_all(repo_paths: list[str]) -> int:
    """base + repo を一括実行する。"""
    rc = cmd_base()
    if rc != 0:
        return rc
    return cmd_repo(repo_paths)


# --- エントリポイント ---------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="AIエージェントルールを各環境へ配置するビルドスクリプト。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("base", help="ベースルールを ~/.config へ書き込む")

    repo_parser = subparsers.add_parser("repo", help="指定リポジトリへルールを配置する")
    repo_parser.add_argument("paths", nargs="+", metavar="REPO_PATH", help="対象リポジトリのパス")

    all_parser = subparsers.add_parser("all", help="base + repo を一括実行する")
    all_parser.add_argument("paths", nargs="+", metavar="REPO_PATH", help="対象リポジトリのパス")

    args = parser.parse_args()

    if args.command == "base":
        return cmd_base()
    if args.command == "repo":
        return cmd_repo(args.paths)
    if args.command == "all":
        return cmd_all(args.paths)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
