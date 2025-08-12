#!/usr/bin/env python3
"""
JHipster日本語ドキュメント自動翻訳システム
upstream取得とマージスクリプト
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


def find_project_root() -> Path:
    """プロジェクトルートディレクトリを見つける"""
    current = Path(__file__).parent
    while current != current.parent:
        if (current / '.git').exists() or (current / 'package.json').exists():
            return current
        current = current.parent
    return Path.cwd()


class UpstreamFetcher:
    def __init__(self, upstream_url: str = "https://github.com/jhipster/jhipster.github.io.git"):
        self.upstream_url = upstream_url
        self.upstream_remote = "upstream"
        self.project_root = find_project_root()
        # プロジェクトルートに移動
        os.chdir(self.project_root)
    
    def setup_upstream_remote(self) -> bool:
        """upstreamリモートをセットアップ"""
        try:
            # 既存のupstreamリモートを確認
            result = subprocess.run(
                ["git", "remote", "get-url", self.upstream_remote],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                print(f"upstream remote already exists: {result.stdout.strip()}")
                return True
            
            # upstreamリモートを追加
            subprocess.run(
                ["git", "remote", "add", self.upstream_remote, self.upstream_url],
                check=True
            )
            print(f"Added upstream remote: {self.upstream_url}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Error setting up upstream remote: {e}")
            return False
    
    def fetch_upstream(self) -> bool:
        """upstreamからフェッチ"""
        try:
            subprocess.run(["git", "fetch", self.upstream_remote], check=True)
            print("Successfully fetched from upstream")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error fetching upstream: {e}")
            return False
    
    def get_upstream_commit_hash(self, short: bool = True) -> Optional[str]:
        """upstreamのmainブランチの最新コミットハッシュを取得"""
        try:
            cmd = ["git", "rev-parse"]
            if short:
                cmd.append("--short=7")
            cmd.append(f"{self.upstream_remote}/main")
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error getting upstream commit hash: {e}")
            return None
    
    def get_current_branch(self) -> Optional[str]:
        """現在のブランチ名を取得"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error getting current branch: {e}")
            return None
    
    def create_sync_branch(self, commit_hash: str) -> bool:
        """sync-{hash}ブランチを作成"""
        branch_name = f"sync-{commit_hash}"
        
        try:
            # CI環境ではorigin/mainから分岐、ローカルでは現在のブランチから分岐
            if os.getenv('CI') or os.getenv('GITHUB_ACTIONS'):
                # GitHub Actions環境ではorigin/mainから分岐
                print("CI environment detected: branching from origin/main")
                subprocess.run(["git", "checkout", "origin/main"], check=True)
            else:
                # ローカル環境では現在のブランチから分岐
                current_branch = self.get_current_branch()
                if current_branch:
                    print(f"Local environment detected: branching from current branch '{current_branch}'")
                    # 現在のブランチに留まる（何もしない）
                else:
                    print("Warning: Could not determine current branch, falling back to main")
                    subprocess.run(["git", "checkout", "main"], check=True)
            
            subprocess.run(["git", "switch", "-c", branch_name], check=True)
            print(f"Created branch: {branch_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating sync branch: {e}")
            return False
    
    def merge_upstream(self, commit_hash: str) -> bool:
        """upstreamの変更をマージ（ワークフロー方式）"""
        target_commit = commit_hash
        try:
            print(f"Merging upstream changes from {target_commit}...")
            
            # マージ実行（失敗を許容）
            subprocess.run(
                ["git", "merge", target_commit, "--allow-unrelated-histories", "--no-edit"],
                check=False
            )
            
            # コンフリクト込みでコミット（失敗を許容）
            subprocess.run(["git", "commit", "-a", "--no-edit"], check=False)
            
            print(f"✓ Merged upstream {target_commit} (conflicts preserved if any)")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Error merging upstream: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="Fetch upstream and create sync branch")
    parser.add_argument(
        "--hash",
        help="Specific commit hash to checkout (optional)"
    )
    parser.add_argument(
        "--upstream-url",
        default="https://github.com/jhipster/jhipster.github.io.git",
        help="Upstream repository URL"
    )
    
    args = parser.parse_args()
    
    fetcher = UpstreamFetcher(args.upstream_url)
    
    # upstreamリモートをセットアップ
    if not fetcher.setup_upstream_remote():
        sys.exit(1)
    
    # upstreamからフェッチ
    if not fetcher.fetch_upstream():
        sys.exit(1)
    
    # コミットハッシュを決定
    if args.hash:
        commit_hash = args.hash[:8]  # 最初の8文字を使用
    else:
        commit_hash = fetcher.get_upstream_commit_hash()
        if not commit_hash:
            sys.exit(1)
    
    print(f"Target commit hash: {commit_hash}")
    
    # syncブランチを作成
    if not fetcher.create_sync_branch(commit_hash):
        sys.exit(1)
    
    # upstreamの変更をマージ
    if not fetcher.merge_upstream(commit_hash):
        sys.exit(1)
    
    print(f"✅ Successfully created sync branch with upstream changes: sync-{commit_hash}")


if __name__ == "__main__":
    main()