#!/usr/bin/env python3
"""
fetch_upstream.py のテスト
"""

import os
import subprocess
import unittest
from unittest.mock import Mock, patch, call
import sys
from pathlib import Path

# scriptsディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from fetch_upstream import UpstreamFetcher


class TestUpstreamFetcher(unittest.TestCase):
    def setUp(self):
        """テストセットアップ"""
        self.fetcher = UpstreamFetcher()
    
    @patch('subprocess.run')
    def test_get_current_branch_success(self, mock_run):
        """現在のブランチ取得の成功テスト"""
        # subprocess.runの戻り値をモック
        mock_result = Mock()
        mock_result.stdout = "feature-branch\n"
        mock_run.return_value = mock_result
        
        result = self.fetcher.get_current_branch()
        
        # 正しいコマンドが呼ばれたことを確認
        mock_run.assert_called_once_with(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, check=True
        )
        
        # 結果が正しいことを確認（改行文字が除去されている）
        self.assertEqual(result, "feature-branch")
    
    @patch('subprocess.run')
    def test_get_current_branch_failure(self, mock_run):
        """現在のブランチ取得の失敗テスト"""
        # subprocess.CalledProcessErrorを発生させる
        mock_run.side_effect = subprocess.CalledProcessError(1, "git")
        
        result = self.fetcher.get_current_branch()
        
        # エラー時はNoneが返されることを確認
        self.assertIsNone(result)
    
    @patch.dict(os.environ, {}, clear=True)  # CI環境変数をクリア
    @patch('subprocess.run')
    def test_create_sync_branch_local_environment(self, mock_run):
        """ローカル環境でのsyncブランチ作成テスト"""
        # get_current_branchの戻り値をモック
        with patch.object(self.fetcher, 'get_current_branch', return_value="my-feature-branch"):
            result = self.fetcher.create_sync_branch("abc1234")
        
        # 成功することを確認
        self.assertTrue(result)
        
        # git switch -c が呼ばれることを確認
        mock_run.assert_called_once_with(["git", "switch", "-c", "sync-abc1234"], check=True)
    
    @patch.dict(os.environ, {'CI': 'true'})  # CI環境をシミュレート
    @patch('subprocess.run')
    def test_create_sync_branch_ci_environment(self, mock_run):
        """CI環境でのsyncブランチ作成テスト"""
        result = self.fetcher.create_sync_branch("abc1234")
        
        # 成功することを確認
        self.assertTrue(result)
        
        # 正しいコマンドが順序通り呼ばれることを確認
        expected_calls = [
            call(["git", "checkout", "origin/main"], check=True),
            call(["git", "switch", "-c", "sync-abc1234"], check=True)
        ]
        mock_run.assert_has_calls(expected_calls)
    
    @patch.dict(os.environ, {'GITHUB_ACTIONS': 'true'})  # GitHub Actions環境をシミュレート
    @patch('subprocess.run')
    def test_create_sync_branch_github_actions_environment(self, mock_run):
        """GitHub Actions環境でのsyncブランチ作成テスト"""
        result = self.fetcher.create_sync_branch("def5678")
        
        # 成功することを確認
        self.assertTrue(result)
        
        # 正しいコマンドが順序通り呼ばれることを確認
        expected_calls = [
            call(["git", "checkout", "origin/main"], check=True),
            call(["git", "switch", "-c", "sync-def5678"], check=True)
        ]
        mock_run.assert_has_calls(expected_calls)
    
    @patch.dict(os.environ, {}, clear=True)  # CI環境変数をクリア
    @patch('subprocess.run')
    def test_create_sync_branch_local_fallback_to_main(self, mock_run):
        """ローカル環境で現在ブランチ取得失敗時のフォールバックテスト"""
        # get_current_branchがNoneを返すようにモック
        with patch.object(self.fetcher, 'get_current_branch', return_value=None):
            result = self.fetcher.create_sync_branch("xyz9876")
        
        # 成功することを確認
        self.assertTrue(result)
        
        # mainブランチにチェックアウトしてからsyncブランチを作成することを確認
        expected_calls = [
            call(["git", "checkout", "main"], check=True),
            call(["git", "switch", "-c", "sync-xyz9876"], check=True)
        ]
        mock_run.assert_has_calls(expected_calls)
    
    @patch('subprocess.run')
    def test_create_sync_branch_failure(self, mock_run):
        """syncブランチ作成の失敗テスト"""
        # subprocess.CalledProcessErrorを発生させる
        mock_run.side_effect = subprocess.CalledProcessError(1, "git")
        
        result = self.fetcher.create_sync_branch("fail123")
        
        # 失敗することを確認
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()