#!/usr/bin/env python3
"""
JHipster日本語ドキュメント自動翻訳システム
upstream取得とマージスクリプト
"""

import argparse
import os
import subprocess
import sys
from typing import Optional


class UpstreamFetcher:
    def __init__(self, upstream_url: str = "https://github.com/jhipster/jhipster.github.io.git"):
        self.upstream_url = upstream_url
        self.upstream_remote = "upstream"
    
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
    
    def create_sync_branch(self, commit_hash: str) -> bool:
        """sync-{hash}ブランチを作成"""
        branch_name = f"sync-{commit_hash}"
        
        try:
            # origin/mainから新しいブランチを作成
            subprocess.run(["git", "checkout", "origin/main"], check=True)
            subprocess.run(["git", "switch", "-c", branch_name], check=True)
            print(f"Created branch: {branch_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating sync branch: {e}")
            return False
    
    def merge_upstream(self, commit_hash: str) -> bool:
        """upstreamの変更をマージ（強制マージ戦略使用）"""
        try:
            # 通常のマージを試行
            try:
                subprocess.run(
                    ["git", "merge", f"{self.upstream_remote}/main", "--no-edit"],
                    check=True
                )
                print("Successfully merged upstream changes (no conflicts)")
                return True
            except subprocess.CalledProcessError:
                print("Merge conflicts detected, using ours strategy for some files...")
                
                # コンフリクトが発生した場合、日本語特有のファイルは'ours'戦略を使用
                # まずマージを中止
                subprocess.run(["git", "merge", "--abort"], check=False)
                
                # 強制マージ（コンフリクトマーカー付きでマージ）
                subprocess.run(
                    ["git", "merge", f"{self.upstream_remote}/main", "--no-edit", "--no-commit"],
                    check=False
                )
                
                # 日本語特有のファイルは'ours'を選択
                japanese_specific_files = [
                    "docusaurus.config.ts",
                    "sidebars.ts",
                    "src/theme/",
                    "CLAUDE.md"
                ]
                
                for file_pattern in japanese_specific_files:
                    subprocess.run(
                        ["git", "checkout", "--ours", file_pattern],
                        check=False
                    )
                
                # ステージング
                subprocess.run(["git", "add", "."], check=True)
                
                # コミット
                subprocess.run(
                    ["git", "commit", "-m", f"merge: upstream {commit_hash} with conflict resolution"],
                    check=True
                )
                
                print("Successfully merged upstream changes (with conflict resolution)")
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
        commit_hash = args.hash[:7]  # 最初の7文字を使用
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