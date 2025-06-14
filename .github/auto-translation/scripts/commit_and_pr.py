#!/usr/bin/env python3
"""
JHipster日本語ドキュメント自動翻訳システム
コミット&PR作成スクリプト
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from typing import Optional


class CommitAndPRManager:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.bot_user = os.getenv("BOT_GIT_USER", "jhipster-auto-translation-bot")
        self.bot_email = os.getenv("BOT_GIT_EMAIL", "bot@jhipster.tech")
        self.gh_token = os.getenv("GH_TOKEN")
    
    def setup_git_config(self) -> bool:
        """Git設定をセットアップ"""
        try:
            if not self.dry_run:
                subprocess.run(
                    ["git", "config", "user.name", self.bot_user],
                    check=True
                )
                subprocess.run(
                    ["git", "config", "user.email", self.bot_email],
                    check=True
                )
            
            print(f"✅ Git config set: {self.bot_user} <{self.bot_email}>")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error setting up git config: {e}")
            return False
    
    def get_current_branch(self) -> Optional[str]:
        """現在のブランチ名を取得"""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None
    
    def get_commit_hash_from_branch(self, branch_name: str) -> Optional[str]:
        """ブランチ名からコミットハッシュを抽出"""
        if branch_name and branch_name.startswith("sync-"):
            return branch_name[5:]  # "sync-"を除去
        return None
    
    def stage_changes(self) -> bool:
        """変更をステージング"""
        try:
            if not self.dry_run:
                subprocess.run(["git", "add", "."], check=True)
            
            # ステージされたファイルを確認
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True, text=True, check=True
            )
            
            staged_files = [f for f in result.stdout.strip().split('\n') if f]
            
            if staged_files:
                print(f"✅ Staged {len(staged_files)} files")
                for file in staged_files[:10]:  # 最初の10ファイルのみ表示
                    print(f"   - {file}")
                if len(staged_files) > 10:
                    print(f"   ... and {len(staged_files) - 10} more files")
                return True
            else:
                print("📋 No changes to stage")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error staging changes: {e}")
            return False
    
    def create_commit(self, commit_hash: str) -> bool:
        """コミットを作成"""
        commit_message = f"docs(sync): upstream {commit_hash} 翻訳\n\n🤖 Generated with [Claude Code](https://claude.ai/code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>"
        
        try:
            if not self.dry_run:
                subprocess.run(
                    ["git", "commit", "-m", commit_message],
                    check=True
                )
            else:
                print("DRY RUN: Would create commit with message:")
                print(f"   {commit_message}")
            
            print(f"✅ Created commit: docs(sync): upstream {commit_hash} 翻訳")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating commit: {e}")
            return False
    
    def generate_pr_body(self, classification_file: Optional[str] = None) -> str:
        """PR本文を生成"""
        body_parts = []
        
        body_parts.append("## 🔄 Upstream同期と翻訳")
        body_parts.append("")
        body_parts.append("このPRは、JHipster upstream リポジトリからの変更を自動的に翻訳したものです。")
        body_parts.append("")
        
        # 分類情報を含める
        if classification_file and os.path.exists(classification_file):
            try:
                with open(classification_file, 'r', encoding='utf-8') as f:
                    classification = json.load(f)
                
                body_parts.append("### 📋 変更ファイル概要")
                body_parts.append("")
                body_parts.append(f"- **総ファイル数**: {classification['total_files']}")
                body_parts.append(f"- **翻訳対象ファイル数**: {classification['translatable_files']}")
                body_parts.append("")
                
                summary = classification["summary"]
                if summary["a"]:
                    body_parts.append(f"#### 🆕 新規文書 ({len(summary['a'])} files)")
                    for file in summary["a"][:5]:
                        body_parts.append(f"- `{file}`")
                    if len(summary["a"]) > 5:
                        body_parts.append(f"- ... and {len(summary['a']) - 5} more files")
                    body_parts.append("")
                
                if summary["b-1"]:
                    body_parts.append(f"#### ✏️ 更新文書 - 衝突なし ({len(summary['b-1'])} files)")
                    for file in summary["b-1"][:5]:
                        body_parts.append(f"- `{file}`")
                    if len(summary["b-1"]) > 5:
                        body_parts.append(f"- ... and {len(summary['b-1']) - 5} more files")
                    body_parts.append("")
                
                if summary["b-2"]:
                    body_parts.append(f"#### ⚠️ 更新文書 - 衝突あり ({len(summary['b-2'])} files)")
                    body_parts.append("")
                    body_parts.append("⚠️ これらのファイルには翻訳衝突が含まれていました。手動確認が推奨されます。")
                    body_parts.append("")
                    for file in summary["b-2"][:5]:
                        body_parts.append(f"- `{file}`")
                    if len(summary["b-2"]) > 5:
                        body_parts.append(f"- ... and {len(summary['b-2']) - 5} more files")
                    body_parts.append("")
                
                if summary["c"]:
                    body_parts.append(f"#### 📄 非翻訳ファイル ({len(summary['c'])} files)")
                    body_parts.append("以下のファイルは翻訳対象外のため、そのままコピーされました。")
                    body_parts.append("")
                    for file in summary["c"][:5]:
                        body_parts.append(f"- `{file}`")
                    if len(summary["c"]) > 5:
                        body_parts.append(f"- ... and {len(summary['c']) - 5} more files")
                    body_parts.append("")
                        
            except Exception as e:
                print(f"⚠️ Error reading classification file: {e}")
        
        body_parts.append("### 🔍 レビューのお願い")
        body_parts.append("")
        body_parts.append("- 翻訳の品質と正確性を確認してください")
        body_parts.append("- 技術用語の翻訳が適切かチェックしてください")
        body_parts.append("- マークダウン形式が正しく保持されているか確認してください")
        body_parts.append("- 衝突ありファイルは特に注意深く確認してください")
        body_parts.append("")
        body_parts.append("---")
        body_parts.append("")
        body_parts.append("🤖 Generated with [Claude Code](https://claude.ai/code)")
        
        return '\n'.join(body_parts)
    
    def create_pull_request(self, branch_name: str, commit_hash: str, classification_file: Optional[str] = None) -> bool:
        """プルリクエストを作成"""
        if not self.gh_token or self.gh_token == "fake_github_token_for_development":
            print("⚠️ GH_TOKEN not available, skipping PR creation")
            return True
        
        pr_title = f"docs: upstream {commit_hash} Translation"
        pr_body = self.generate_pr_body(classification_file)
        
        try:
            if not self.dry_run:
                # まずブランチをプッシュ
                subprocess.run(
                    ["git", "push", "-u", "origin", branch_name],
                    check=True
                )
                
                # PRを作成
                subprocess.run([
                    "gh", "pr", "create",
                    "--title", pr_title,
                    "--body", pr_body,
                    "--head", branch_name,
                    "--base", "main"
                ], check=True)
                
                print(f"✅ Created pull request: {pr_title}")
            else:
                print("DRY RUN: Would create PR with:")
                print(f"   Title: {pr_title}")
                print(f"   Branch: {branch_name}")
                print("   Body:")
                for line in pr_body.split('\n')[:10]:
                    print(f"     {line}")
                print("     ...")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating pull request: {e}")
            return False
    
    def push_to_origin(self, branch_name: str) -> bool:
        """originにプッシュ"""
        try:
            if not self.dry_run:
                subprocess.run(
                    ["git", "push", "-u", "origin", branch_name],
                    check=True
                )
            else:
                print(f"DRY RUN: Would push branch {branch_name} to origin")
            
            print(f"✅ Pushed branch to origin: {branch_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error pushing to origin: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="Commit changes and create PR")
    parser.add_argument(
        "--classification",
        help="Classification JSON file for PR body generation"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run mode (don't actually commit/push/create PR)"
    )
    parser.add_argument(
        "--push-origin",
        type=str,
        choices=["true", "false"],
        default="true",
        help="Whether to push to origin"
    )
    parser.add_argument(
        "--create-pr",
        type=str,
        choices=["true", "false"],
        default="true",
        help="Whether to create pull request"
    )
    
    args = parser.parse_args()
    
    # DRY_RUN環境変数もチェック
    dry_run = args.dry_run or os.getenv("DRY_RUN", "false").lower() == "true"
    push_origin = args.push_origin.lower() == "true"
    create_pr = args.create_pr.lower() == "true"
    
    manager = CommitAndPRManager(dry_run)
    
    # Git設定をセットアップ
    if not manager.setup_git_config():
        sys.exit(1)
    
    # 現在のブランチを取得
    branch_name = manager.get_current_branch()
    if not branch_name:
        print("❌ Could not determine current branch")
        sys.exit(1)
    
    print(f"📋 Current branch: {branch_name}")
    
    # ブランチ名からコミットハッシュを抽出
    commit_hash = manager.get_commit_hash_from_branch(branch_name)
    if not commit_hash:
        print("⚠️ Could not extract commit hash from branch name, using timestamp")
        commit_hash = datetime.now().strftime("%Y%m%d")
    
    # 変更をステージング
    if not manager.stage_changes():
        print("📋 No changes to commit")
        sys.exit(0)
    
    # コミットを作成
    if not manager.create_commit(commit_hash):
        sys.exit(1)
    
    # originにプッシュ
    if push_origin:
        if not manager.push_to_origin(branch_name):
            sys.exit(1)
    
    # プルリクエストを作成
    if create_pr:
        if not manager.create_pull_request(branch_name, commit_hash, args.classification):
            sys.exit(1)
    
    print("✅ All operations completed successfully")


if __name__ == "__main__":
    main()