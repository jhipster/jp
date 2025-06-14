#!/usr/bin/env python3
"""
JHipster日本語ドキュメント自動翻訳システム
Gemini翻訳スクリプト
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple

import google.generativeai as genai


class GeminiTranslator:
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = 4096
        self.style_guide_content = ""
        
        # Gemini APIを設定
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
        # スタイルガイドを読み込み
        self.load_style_guide()
    
    def load_style_guide(self):
        """スタイルガイドを読み込み"""
        # 実行位置に関係なく、正しいパスを探索
        possible_paths = [
            Path("docs/style-guide.md"),
            Path(".github/auto-translation/docs/style-guide.md"),
            Path("../docs/style-guide.md"),
            Path("../../docs/style-guide.md")
        ]
        
        style_guide_path = None
        for path in possible_paths:
            if path.exists():
                style_guide_path = path
                break
        if style_guide_path and style_guide_path.exists():
            try:
                with open(style_guide_path, 'r', encoding='utf-8') as f:
                    self.style_guide_content = f.read()
                print(f"✅ Loaded style guide: {style_guide_path}")
            except Exception as e:
                print(f"⚠️ Error loading style guide: {e}")
        else:
            print(f"⚠️ Style guide not found in any of the expected locations")
    
    def count_tokens_estimate(self, text: str) -> int:
        """テキストのトークン数を概算"""
        # 簡易的な計算：日本語は1文字=1.5トークン、英語は1単語=1トークン
        japanese_chars = len(re.findall(r'[ひらがなカタカナ漢字]', text))
        english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
        other_chars = len(text) - japanese_chars - english_words
        
        return int(japanese_chars * 1.5 + english_words + other_chars * 0.3)
    
    def split_content_by_paragraphs(self, content: str) -> List[str]:
        """内容を段落単位で分割"""
        # 空行で分割
        paragraphs = re.split(r'\n\s*\n', content)
        
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # 現在のチャンクに段落を追加した場合のトークン数を計算
            test_chunk = f"{current_chunk}\n\n{paragraph}".strip()
            if self.count_tokens_estimate(test_chunk) > self.max_tokens and current_chunk:
                # 現在のチャンクを保存し、新しいチャンクを開始
                chunks.append(current_chunk)
                current_chunk = paragraph
            else:
                current_chunk = test_chunk
        
        # 最後のチャンクを追加
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def create_translation_prompt(self, content: str) -> str:
        """翻訳用プロンプトを作成"""
        style_guide_section = ""
        if self.style_guide_content:
            style_guide_section = f"""
以下のスタイルガイドに従って翻訳してください：

{self.style_guide_content}

---

"""
        
        prompt = f"""{style_guide_section}以下の英語のJHipsterドキュメントを日本語に翻訳してください。

重要な注意事項：
1. マークダウン形式を保持してください
2. コードブロック、URL、ファイルパス、コマンドは翻訳しないでください
3. 技術用語は適切な日本語に翻訳するか、必要に応じて英語のまま残してください
4. 文体は常体（である調）を使用してください
5. 元の文書の構造と改行を保持してください
6. HTMLタグやマークダウン記法は変更しないでください

翻訳対象テキスト：

{content}

翻訳結果（日本語のみ）："""
        
        return prompt
    
    def translate_chunk(self, content: str, retry_count: int = 3) -> Optional[str]:
        """単一チャンクを翻訳"""
        prompt = self.create_translation_prompt(content)
        
        for attempt in range(retry_count):
            try:
                response = self.model.generate_content(prompt)
                
                if response.text:
                    translated = response.text.strip()
                    
                    # 行数チェック
                    original_lines = len(content.split('\n'))
                    translated_lines = len(translated.split('\n'))
                    
                    # 行数の差が20%を超える場合は警告
                    if abs(original_lines - translated_lines) / max(original_lines, 1) > 0.2:
                        print(f"⚠️ Line count mismatch: {original_lines} -> {translated_lines}")
                    
                    return translated
                else:
                    print(f"⚠️ Empty response from Gemini (attempt {attempt + 1})")
                    
            except Exception as e:
                print(f"⚠️ Translation error (attempt {attempt + 1}): {e}")
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)  # 指数バックオフ
        
        return None
    
    def translate_file(self, file_path: str, output_path: Optional[str] = None) -> bool:
        """ファイル全体を翻訳"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"📝 Translating: {file_path}")
            
            # コンテンツを分割
            chunks = self.split_content_by_paragraphs(content)
            print(f"   Split into {len(chunks)} chunks")
            
            translated_chunks = []
            for i, chunk in enumerate(chunks):
                print(f"   Translating chunk {i + 1}/{len(chunks)}...")
                translated_chunk = self.translate_chunk(chunk)
                
                if translated_chunk is None:
                    print(f"❌ Failed to translate chunk {i + 1}")
                    return False
                
                translated_chunks.append(translated_chunk)
                
                # API制限を避けるための待機
                if i < len(chunks) - 1:
                    time.sleep(1)
            
            # 翻訳結果を結合
            translated_content = '\n\n'.join(translated_chunks)
            
            # 出力ファイルパスを決定
            if output_path is None:
                output_path = file_path
            
            # 翻訳結果を保存
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            print(f"✅ Translation completed: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error translating file {file_path}: {e}")
            return False
    
    def translate_files_from_classification(self, classification_file: str, mode: str = "all") -> bool:
        """分類結果から翻訳対象ファイルを翻訳"""
        try:
            with open(classification_file, 'r', encoding='utf-8') as f:
                classification = json.load(f)
            
            files_to_translate = []
            
            if mode == "all":
                # a, b-1, b-2のすべてを翻訳
                files_to_translate.extend(classification["summary"]["a"])
                files_to_translate.extend(classification["summary"]["b-1"])
                files_to_translate.extend(classification["summary"]["b-2"])
            elif mode == "selective":
                # aとb-1のみを翻訳（衝突があるファイルは除外）
                files_to_translate.extend(classification["summary"]["a"])
                files_to_translate.extend(classification["summary"]["b-1"])
            elif mode == "new-only":
                # 新規ファイルのみを翻訳
                files_to_translate.extend(classification["summary"]["a"])
            
            if not files_to_translate:
                print("📋 No files to translate")
                return True
            
            print(f"📋 Found {len(files_to_translate)} files to translate")
            
            success_count = 0
            for file_path in files_to_translate:
                if self.translate_file(file_path):
                    success_count += 1
                else:
                    print(f"❌ Failed to translate: {file_path}")
            
            print(f"✅ Translation completed: {success_count}/{len(files_to_translate)} files")
            return success_count == len(files_to_translate)
            
        except Exception as e:
            print(f"❌ Error in batch translation: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="Translate files using Gemini API")
    parser.add_argument(
        "--file",
        help="Single file to translate"
    )
    parser.add_argument(
        "--classification",
        help="Classification JSON file for batch translation"
    )
    parser.add_argument(
        "--mode",
        choices=["all", "selective", "new-only"],
        default="selective",
        help="Translation mode for batch processing"
    )
    parser.add_argument(
        "--output",
        help="Output file path (for single file translation)"
    )
    
    args = parser.parse_args()
    
    # API キーをチェック
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "fake_api_key_for_development":
        print("❌ GEMINI_API_KEY environment variable is required")
        sys.exit(1)
    
    translator = GeminiTranslator(api_key)
    
    if args.file:
        # 単一ファイル翻訳
        success = translator.translate_file(args.file, args.output)
        sys.exit(0 if success else 1)
    elif args.classification:
        # バッチ翻訳
        success = translator.translate_files_from_classification(args.classification, args.mode)
        sys.exit(0 if success else 1)
    else:
        print("❌ Either --file or --classification must be specified")
        sys.exit(1)


if __name__ == "__main__":
    main()