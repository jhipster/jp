#!/usr/bin/env python3
"""
JHipster日本語ドキュメント自動翻訳システム
ポストプロセッシングテスト
"""

import os
import tempfile
import unittest

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from postprocess import PostProcessor


class TestPostProcessor(unittest.TestCase):
    def setUp(self):
        # LanguageToolを無効にしてテスト
        self.processor = PostProcessor(enable_language_tool=False)
    
    def test_remove_conflict_markers(self):
        """コンフリクトマーカー除去のテスト"""
        content_with_conflicts = """# Test Document

Some content here.

<<<<<<< HEAD
This is the current version.
This line should be kept.
=======
This is the incoming version.
This line should be removed.
>>>>>>> upstream/main

More content after conflict.
"""
        
        expected_content = """# Test Document

Some content here.

This is the current version.
This line should be kept.
This is the incoming version.
This line should be removed.

More content after conflict.
"""
        
        result = self.processor.remove_conflict_markers(content_with_conflicts)
        self.assertEqual(result, expected_content)
    
    def test_remove_conflict_markers_no_conflicts(self):
        """コンフリクトマーカーなしのコンテンツのテスト"""
        clean_content = """# Test Document

This is a clean document.
No conflicts here.
"""
        
        result = self.processor.remove_conflict_markers(clean_content)
        self.assertEqual(result, clean_content)
    
    def test_validate_markdown_structure(self):
        """マークダウン構造検証のテスト"""
        # 正常なマークダウン
        good_markdown = """# Title

[Valid Link](https://example.com)

```javascript
console.log("test");
```
"""
        
        issues = self.processor.validate_markdown_structure(good_markdown)
        self.assertEqual(len(issues), 0)
        
        # 問題のあるマークダウン
        bad_markdown = """# Title

[Empty Link]()

[Another Bad Link](   )
"""
        
        issues = self.processor.validate_markdown_structure(bad_markdown)
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("Empty link URL" in issue for issue in issues))
    
    def test_process_file(self):
        """ファイル処理のテスト"""
        # テスト用コンテンツ（コンフリクトマーカー付き）
        test_content = """# Test Document

Some content.

<<<<<<< HEAD
Original content
=======
New content
>>>>>>> branch

End of document.
"""
        
        expected_content = """# Test Document

Some content.

Original content
New content

End of document.
"""
        
        # 一時ファイルでテスト
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(test_content)
            test_file = f.name
        
        try:
            # ファイル処理実行
            result = self.processor.process_file(test_file)
            
            # 成功したことを確認
            self.assertTrue(result)
            
            # ファイル内容が正しく処理されたことを確認
            with open(test_file, 'r', encoding='utf-8') as f:
                processed_content = f.read()
            
            self.assertEqual(processed_content, expected_content)
            
        finally:
            os.unlink(test_file)
    
    def test_check_line_count_consistency(self):
        """行数一致チェックのテスト"""
        # 同じ行数のファイル
        content1 = "Line 1\nLine 2\nLine 3\n"
        content2 = "行 1\n行 2\n行 3\n"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f1, \
             tempfile.NamedTemporaryFile(mode='w', delete=False) as f2:
            f1.write(content1)
            f2.write(content2)
            file1, file2 = f1.name, f2.name
        
        try:
            result = self.processor.check_line_count_consistency(file1, file2)
            self.assertTrue(result)
        finally:
            os.unlink(file1)
            os.unlink(file2)
        
        # 異なる行数のファイル
        content3 = "Line 1\nLine 2\n"
        content4 = "行 1\n行 2\n行 3\n行 4\n"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f3, \
             tempfile.NamedTemporaryFile(mode='w', delete=False) as f4:
            f3.write(content3)
            f4.write(content4)
            file3, file4 = f3.name, f4.name
        
        try:
            result = self.processor.check_line_count_consistency(file3, file4)
            self.assertFalse(result)
        finally:
            os.unlink(file3)
            os.unlink(file4)


class TestPostProcessorWithLanguageTool(unittest.TestCase):
    """LanguageTool有効時のテスト"""
    
    def test_grammar_check_disabled(self):
        """文法チェック無効時のテスト"""
        processor = PostProcessor(enable_language_tool=False)
        
        text = "これは文法チェックのテストです。"
        issues = processor.check_grammar(text)
        
        # LanguageToolが無効の場合、空のリストが返される
        self.assertEqual(issues, [])
    
    # 注意: 実際のLanguageToolを使用するテストは時間がかかるため、
    # CI環境では適切にスキップするか、モックを使用することを推奨


if __name__ == '__main__':
    unittest.main()