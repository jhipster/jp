#!/usr/bin/env python3
"""
JHipster日本語ドキュメント自動翻訳システム
翻訳機能テスト
"""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from translate_chunk import GeminiTranslator


class TestGeminiTranslator(unittest.TestCase):
    def setUp(self):
        # テスト用のダミーAPIキー
        self.api_key = "test_api_key"
        
        # Gemini APIの初期化をモック
        with patch('google.generativeai.configure'), \
             patch('google.generativeai.GenerativeModel') as mock_model:
            self.translator = GeminiTranslator(self.api_key)
            self.mock_model = mock_model.return_value
    
    def test_count_tokens_estimate(self):
        """トークン数概算のテスト"""
        # 英語テキスト
        english_text = "Hello world this is a test"
        tokens = self.translator.count_tokens_estimate(english_text)
        self.assertGreater(tokens, 0)
        
        # 日本語テキスト
        japanese_text = "これはテストです"
        tokens = self.translator.count_tokens_estimate(japanese_text)
        self.assertGreater(tokens, 0)
        
        # 混在テキスト
        mixed_text = "これはJHipsterのtest文書です"
        tokens = self.translator.count_tokens_estimate(mixed_text)
        self.assertGreater(tokens, 0)
    
    def test_split_content_by_paragraphs(self):
        """段落分割のテスト"""
        content = """# Title

This is the first paragraph.

This is the second paragraph.
It has multiple lines.

## Subtitle

Another paragraph here.

```code
// Code block should not be split
function test() {
    return true;
}
```

Final paragraph."""
        
        chunks = self.translator.split_content_by_paragraphs(content)
        
        # 少なくとも複数のチャンクに分割されることを確認
        self.assertGreater(len(chunks), 1)
        
        # 各チャンクが文字列であることを確認
        for chunk in chunks:
            self.assertIsInstance(chunk, str)
            self.assertGreater(len(chunk.strip()), 0)
    
    def test_create_translation_prompt(self):
        """翻訳プロンプト作成のテスト"""
        content = "This is a test document for JHipster."
        prompt = self.translator.create_translation_prompt(content)
        
        # プロンプトに必要な要素が含まれていることを確認
        self.assertIn("日本語に翻訳", prompt)
        self.assertIn("マークダウン形式", prompt)
        self.assertIn("常体", prompt)
        self.assertIn(content, prompt)
    
    @patch.object(GeminiTranslator, 'translate_chunk')
    def test_translate_file(self, mock_translate_chunk):
        """ファイル翻訳のテスト"""
        # モックの設定
        mock_translate_chunk.return_value = "これはテスト文書です。"
        
        # テスト用の一時ファイルを作成
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Test Document\n\nThis is a test document.")
            test_file = f.name
        
        try:
            # 翻訳実行
            result = self.translator.translate_file(test_file)
            
            # 成功したことを確認
            self.assertTrue(result)
            
            # translate_chunkが呼ばれたことを確認
            mock_translate_chunk.assert_called()
            
            # ファイルが更新されたことを確認
            with open(test_file, 'r', encoding='utf-8') as f:
                translated_content = f.read()
            
            self.assertEqual(translated_content, "これはテスト文書です。")
            
        finally:
            os.unlink(test_file)
    
    @patch.object(GeminiTranslator, 'translate_file')
    def test_translate_files_from_classification(self, mock_translate_file):
        """分類結果からの翻訳のテスト"""
        # モックの設定
        mock_translate_file.return_value = True
        
        # 分類結果のテストデータ
        classification_data = {
            "summary": {
                "a": ["docs/new.md"],
                "b-1": ["docs/updated.md"],
                "b-2": ["docs/conflict.md"],
                "c": ["package.json"]
            }
        }
        
        # 一時ファイルに分類結果を保存
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            import json
            json.dump(classification_data, f)
            classification_file = f.name
        
        try:
            # selective modeでテスト
            result = self.translator.translate_files_from_classification(
                classification_file, mode="selective"
            )
            
            # 成功したことを確認
            self.assertTrue(result)
            
            # 期待されるファイル数が翻訳されたことを確認
            # selective mode: a + b-1 = 2ファイル
            self.assertEqual(mock_translate_file.call_count, 2)
            
        finally:
            os.unlink(classification_file)


class TestGeminiTranslatorIntegration(unittest.TestCase):
    """統合テスト（実際のAPI呼び出しなし）"""
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_translation_workflow(self, mock_model_class, mock_configure):
        """翻訳ワークフロー全体のテスト"""
        # APIレスポンスをモック
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "これはJHipsterのテスト文書である。"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        translator = GeminiTranslator("test_api_key")
        
        # テスト用コンテンツ
        test_content = "This is a JHipster test document."
        
        # 翻訳実行
        result = translator.translate_chunk(test_content)
        
        # 結果確認
        self.assertEqual(result, "これはJHipsterのテスト文書である。")
        
        # APIが正しく呼ばれたことを確認
        mock_configure.assert_called_once_with(api_key="test_api_key")
        mock_model.generate_content.assert_called_once()


if __name__ == '__main__':
    unittest.main()