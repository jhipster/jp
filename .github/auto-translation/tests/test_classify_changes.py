#!/usr/bin/env python3
"""
JHipster日本語ドキュメント自動翻訳システム
変更ファイル分類テスト
"""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from classify_changes import ChangeClassifier


class TestChangeClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = ChangeClassifier()
    
    def test_is_translatable_file(self):
        """翻訳対象ファイル判定のテスト"""
        # 翻訳対象
        self.assertTrue(self.classifier.is_translatable_file("README.md"))
        self.assertTrue(self.classifier.is_translatable_file("docs/getting-started.mdx"))
        self.assertTrue(self.classifier.is_translatable_file("guide.html"))
        self.assertTrue(self.classifier.is_translatable_file("manual.adoc"))
        
        # 翻訳対象外
        self.assertFalse(self.classifier.is_translatable_file("image.png"))
        self.assertFalse(self.classifier.is_translatable_file("config.json"))
        self.assertFalse(self.classifier.is_translatable_file("style.css"))
        self.assertFalse(self.classifier.is_translatable_file("script.js"))
        self.assertFalse(self.classifier.is_translatable_file("package.lock"))
        
        # 特殊ケース
        self.assertFalse(self.classifier.is_translatable_file("LICENSE"))
        self.assertFalse(self.classifier.is_translatable_file("CNAME"))
    
    def test_has_conflict_markers(self):
        """コンフリクトマーカー検出のテスト"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            # コンフリクトマーカーありのファイル
            f.write("""# Test Document

Some content here.

<<<<<<< HEAD
This is the current version.
=======
This is the incoming version.
>>>>>>> upstream/main

More content.
""")
            conflict_file = f.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            # コンフリクトマーカーなしのファイル
            f.write("""# Test Document

Some content here.
No conflicts in this file.
""")
            clean_file = f.name
        
        try:
            self.assertTrue(self.classifier.has_conflict_markers(conflict_file))
            self.assertFalse(self.classifier.has_conflict_markers(clean_file))
        finally:
            os.unlink(conflict_file)
            os.unlink(clean_file)
    
    def test_classify_file_change(self):
        """ファイル変更分類のテスト"""
        # 新規文書ファイル
        self.assertEqual(
            self.classifier.classify_file_change("A", "docs/new-guide.md"),
            "a"
        )
        
        # 変更された翻訳対象外ファイル
        self.assertEqual(
            self.classifier.classify_file_change("M", "package.json"),
            "c"
        )
        
        # 削除されたファイル
        self.assertEqual(
            self.classifier.classify_file_change("D", "old-doc.md"),
            "c"
        )
    
    @patch('subprocess.run')
    def test_get_changed_files(self, mock_run):
        """変更ファイル取得のテスト"""
        # gitコマンドの出力をモック
        mock_run.return_value = MagicMock(
            stdout="A\tdocs/new-guide.md\nM\tREADME.md\nD\told-file.txt\nM\tpackage.json\n",
            returncode=0
        )
        
        files = self.classifier.get_changed_files()
        
        expected = [
            ("A", "docs/new-guide.md"),
            ("M", "README.md"),
            ("D", "old-file.txt"),
            ("M", "package.json")
        ]
        
        self.assertEqual(files, expected)
        mock_run.assert_called_once_with(
            ["git", "diff", "--name-status", "origin/main..HEAD"],
            capture_output=True, text=True, check=True
        )
    
    @patch.object(ChangeClassifier, 'get_changed_files')
    @patch.object(ChangeClassifier, 'has_conflict_markers')
    def test_classify_all_changes(self, mock_has_conflicts, mock_get_files):
        """全変更分類のテスト"""
        # テストデータ
        mock_get_files.return_value = [
            ("A", "docs/new-guide.md"),      # a: 新規文書
            ("M", "README.md"),              # b-1: 追記 (No conflict)
            ("M", "docs/conflict.md"),       # b-2: 衝突 (Conflict)
            ("M", "package.json"),           # c: 非文書
            ("A", "image.png")               # c: 非文書
        ]
        
        # コンフリクトマーカーの有無を設定
        def conflict_side_effect(filepath):
            return filepath == "docs/conflict.md"
        
        mock_has_conflicts.side_effect = conflict_side_effect
        
        result = self.classifier.classify_all_changes()
        
        # 分類結果の確認
        expected_summary = {
            "a": ["docs/new-guide.md"],
            "b-1": ["README.md"],
            "b-2": ["docs/conflict.md"],
            "c": ["package.json", "image.png"]
        }
        
        self.assertEqual(result["summary"], expected_summary)
        self.assertEqual(result["total_files"], 5)
        self.assertEqual(result["translatable_files"], 3)


if __name__ == '__main__':
    unittest.main()