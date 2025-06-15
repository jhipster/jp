#!/usr/bin/env python3
"""
JHipster日本語ドキュメント自動翻訳システム
ポストプロセッシングスクリプト
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Optional


def find_project_root() -> Path:
    """プロジェクトルートディレクトリを見つける"""
    current = Path(__file__).parent
    while current != current.parent:
        if (current / '.git').exists() or (current / 'package.json').exists():
            return current
        current = current.parent
    return Path.cwd()

try:
    import language_tool_python
    LANGUAGE_TOOL_AVAILABLE = True
except ImportError:
    LANGUAGE_TOOL_AVAILABLE = False
    print("⚠️ language-tool-python not available, skipping grammar check")


class PostProcessor:
    def __init__(self, enable_language_tool: bool = True):
        self.enable_language_tool = enable_language_tool and LANGUAGE_TOOL_AVAILABLE
        self.language_tool = None
        self.project_root = find_project_root()
        
        if self.enable_language_tool:
            try:
                self.language_tool = language_tool_python.LanguageTool('ja')
                print("✅ LanguageTool initialized for Japanese")
            except Exception as e:
                print(f"⚠️ Failed to initialize LanguageTool: {e}")
                self.enable_language_tool = False
    
    def remove_conflict_markers(self, content: str) -> str:
        """Git コンフリクトマーカーを除去"""
        # コンフリクトマーカーのパターン
        patterns = [
            r'^<{4,7} .*\n',  # <<<<<<< HEAD
            r'^={4,7}\n',     # =======
            r'^>{4,7} .*\n',  # >>>>>>> branch
        ]
        
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            is_conflict_marker = False
            for pattern in patterns:
                if re.match(pattern, line + '\n', re.MULTILINE):
                    is_conflict_marker = True
                    break
            
            if not is_conflict_marker:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def check_line_count_consistency(self, original_file: str, processed_file: str) -> bool:
        """原文と翻訳の行数一致を確認"""
        try:
            original_path = self.project_root / original_file
            processed_path = self.project_root / processed_file
            
            with open(original_path, 'r', encoding='utf-8') as f:
                original_lines = len(f.readlines())
            
            with open(processed_path, 'r', encoding='utf-8') as f:
                processed_lines = len(f.readlines())
            
            if original_lines != processed_lines:
                print(f"⚠️ Line count mismatch: {original_file}({original_lines}) vs {processed_file}({processed_lines})")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error checking line count: {e}")
            return False
    
    def check_grammar(self, text: str) -> List[dict]:
        """文法チェック（LanguageToolを使用）"""
        if not self.enable_language_tool or not self.language_tool:
            return []
        
        try:
            matches = self.language_tool.check(text)
            return [
                {
                    "message": match.message,
                    "offset": match.offset,
                    "length": match.length,
                    "context": match.context,
                    "suggestions": [r for r in match.replacements[:3]]  # 最初の3つの提案のみ
                }
                for match in matches
            ]
        except Exception as e:
            print(f"⚠️ Grammar check error: {e}")
            return []
    
    def validate_markdown_structure(self, content: str) -> List[str]:
        """マークダウン構造の検証"""
        issues = []
        lines = content.split('\n')
        
        # 基本的な検証
        for i, line in enumerate(lines, 1):
            # コードブロックの対称性チェック
            if line.strip().startswith('```'):
                # この実装は簡単化されています
                pass
            
            # リンクの形式チェック
            if '[' in line and ']' in line:
                # マークダウンリンクの基本的な形式チェック
                link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
                links = re.findall(link_pattern, line)
                for text, url in links:
                    if not url or url.isspace():
                        issues.append(f"Line {i}: Empty link URL")
        
        return issues
    
    def process_file(self, file_path: str, output_path: Optional[str] = None) -> bool:
        """ファイルをポストプロセッシング"""
        try:
            full_file_path = self.project_root / file_path
            with open(full_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"📝 Post-processing: {file_path}")
            
            # コンフリクトマーカーを除去
            original_content = content
            content = self.remove_conflict_markers(content)
            
            if content != original_content:
                print("   ✅ Removed conflict markers")
            
            # マークダウン構造検証
            markdown_issues = self.validate_markdown_structure(content)
            if markdown_issues:
                print("   ⚠️ Markdown structure issues:")
                for issue in markdown_issues[:5]:  # 最初の5つのみ表示
                    print(f"      - {issue}")
            
            # 文法チェック
            if self.enable_language_tool:
                # 長すぎるテキストは分割してチェック
                max_chunk_size = 5000
                if len(content) > max_chunk_size:
                    print("   📝 Running grammar check (in chunks)...")
                    chunks = [content[i:i+max_chunk_size] for i in range(0, len(content), max_chunk_size)]
                    all_grammar_issues = []
                    for chunk in chunks:
                        chunk_issues = self.check_grammar(chunk)
                        all_grammar_issues.extend(chunk_issues)
                else:
                    print("   📝 Running grammar check...")
                    all_grammar_issues = self.check_grammar(content)
                
                if all_grammar_issues:
                    print(f"   ⚠️ Found {len(all_grammar_issues)} potential grammar issues")
                    for issue in all_grammar_issues[:3]:  # 最初の3つのみ表示
                        print(f"      - {issue['message']}")
                        if issue['suggestions']:
                            print(f"        Suggestions: {', '.join(issue['suggestions'])}")
                else:
                    print("   ✅ No grammar issues found")
            
            # 出力ファイルパスを決定
            if output_path is None:
                full_output_path = full_file_path
            else:
                full_output_path = self.project_root / output_path
            
            # 処理結果を保存
            full_output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Post-processing completed: {full_output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error post-processing file {file_path}: {e}")
            return False
    
    def process_files_from_classification(self, classification_file: str) -> bool:
        """分類結果からファイルをポストプロセッシング"""
        try:
            full_classification_path = self.project_root / classification_file
            with open(full_classification_path, 'r', encoding='utf-8') as f:
                classification = json.load(f)
            
            # 翻訳済みファイルを対象とする
            files_to_process = []
            files_to_process.extend(classification["summary"]["a"])
            files_to_process.extend(classification["summary"]["b-1"])
            files_to_process.extend(classification["summary"]["b-2"])
            
            if not files_to_process:
                print("📋 No files to post-process")
                return True
            
            print(f"📋 Found {len(files_to_process)} files to post-process")
            
            success_count = 0
            for file_path in files_to_process:
                full_file_path = self.project_root / file_path
                if full_file_path.exists():
                    if self.process_file(file_path):
                        success_count += 1
                    else:
                        print(f"❌ Failed to post-process: {file_path}")
                else:
                    print(f"⚠️ File not found: {file_path}")
            
            print(f"✅ Post-processing completed: {success_count}/{len(files_to_process)} files")
            return success_count == len(files_to_process)
            
        except Exception as e:
            print(f"❌ Error in batch post-processing: {e}")
            return False
    
    def cleanup(self):
        """リソースクリーンアップ"""
        if self.language_tool:
            self.language_tool.close()


def main():
    parser = argparse.ArgumentParser(description="Post-process translated files")
    parser.add_argument(
        "--file",
        help="Single file to post-process"
    )
    parser.add_argument(
        "--classification",
        help="Classification JSON file for batch post-processing"
    )
    parser.add_argument(
        "--output",
        help="Output file path (for single file processing)"
    )
    parser.add_argument(
        "--no-grammar-check",
        action="store_true",
        help="Disable grammar checking"
    )
    
    args = parser.parse_args()
    
    # LanguageTool設定
    enable_language_tool = not args.no_grammar_check
    if os.getenv("LANGUAGE_TOOL_ENABLED", "true").lower() == "false":
        enable_language_tool = False
    
    processor = PostProcessor(enable_language_tool)
    
    try:
        if args.file:
            # 単一ファイル処理
            success = processor.process_file(args.file, args.output)
            sys.exit(0 if success else 1)
        elif args.classification:
            # バッチ処理
            success = processor.process_files_from_classification(args.classification)
            sys.exit(0 if success else 1)
        else:
            print("❌ Either --file or --classification must be specified")
            sys.exit(1)
    finally:
        processor.cleanup()


if __name__ == "__main__":
    main()