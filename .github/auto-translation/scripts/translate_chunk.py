#!/usr/bin/env python3
"""
JHipster日本語ドキュメント自動翻訳システム
Gemini翻訳スクリプト
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple, Dict

import google.generativeai as genai


def find_project_root() -> Path:
    """プロジェクトルートディレクトリを見つける"""
    current = Path(__file__).parent
    while current != current.parent:
        if (current / '.git').exists() or (current / 'package.json').exists():
            return current
        current = current.parent
    return Path.cwd()


class GeminiTranslator:
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash", commit_hash: Optional[str] = None):
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = 4096
        self.style_guide_content = ""
        self.project_root = find_project_root()
        self.commit_hash = commit_hash  # upstream commit hash for diff-based translation
        
        # Gemini APIを設定
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
        # スタイルガイドを読み込み
        self.load_style_guide()
    
    def load_style_guide(self):
        """基本スタイルガイドを読み込み"""
        # プロジェクトルートから相対パスで探索
        style_guide_path = self.project_root / ".github/auto-translation/docs/style-guide.md"
        
        if style_guide_path.exists():
            try:
                with open(style_guide_path, 'r', encoding='utf-8') as f:
                    self.style_guide_content = f.read()
                print(f"✅ Loaded base style guide: {style_guide_path}")
            except Exception as e:
                print(f"⚠️ Error loading base style guide: {e}")
        else:
            print(f"⚠️ Base style guide not found: {style_guide_path}")
    
    def get_custom_style_guide_for_path(self, file_path: str) -> str:
        """ファイルパスに応じたカスタムスタイルガイドを取得"""
        custom_style_guide = ""
        
        # docs/releases フォルダの場合、リリース用スタイルガイドを適用
        if file_path.startswith("docs/releases/"):
            release_style_guide_path = self.project_root / ".github/auto-translation/docs/style-guide-release.md"
            if release_style_guide_path.exists():
                try:
                    with open(release_style_guide_path, 'r', encoding='utf-8') as f:
                        custom_style_guide = f.read()
                    print(f"✅ Applied custom style guide for releases: {file_path}")
                except Exception as e:
                    print(f"⚠️ Error loading release style guide: {e}")
        
        # 他のフォルダ固有のスタイルガイドもここに追加可能
        
        return custom_style_guide
    
    def count_tokens_estimate(self, text: str) -> int:
        """テキストのトークン数を概算"""
        # 簡易的な計算：日本語は1文字=1.5トークン、英語は1単語=1トークン
        japanese_chars = len(re.findall(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]', text))
        english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
        other_chars = len(text) - japanese_chars - english_words
        
        return int(japanese_chars * 1.5 + english_words + other_chars * 0.3)
    
    def _is_japanese_content(self, content: str) -> bool:
        """コンテンツが日本語コンテンツかどうかを判定"""
        # 日本語文字の比率が10%以上であれば日本語コンテンツとみなす
        # Unicode範囲での日本語文字検出
        japanese_chars = len(re.findall(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]', content))
        total_chars = len(content)
        
        if total_chars == 0:
            return False
        
        japanese_ratio = japanese_chars / total_chars
        return japanese_ratio > 0.1
    
    def get_file_diff(self, file_path: str, commit_hash: str) -> Optional[str]:
        """指定したコミットでのファイル差分を取得"""
        try:
            # upstreamリモートの設定確認
            upstream_cmd = ["git", "remote", "get-url", "upstream"]
            upstream_result = subprocess.run(
                upstream_cmd, 
                cwd=self.project_root, 
                capture_output=True, 
                text=True, 
                check=False
            )
            
            if upstream_result.returncode != 0:
                print(f"⚠️  Upstream remote not found, adding upstream remote...")
                add_upstream_cmd = [
                    "git", "remote", "add", "upstream", 
                    "https://github.com/jhipster/jhipster.github.io.git"
                ]
                subprocess.run(add_upstream_cmd, cwd=self.project_root, check=True)
                
                # Fetch upstream
                fetch_cmd = ["git", "fetch", "upstream"]
                subprocess.run(fetch_cmd, cwd=self.project_root, check=True)
            
            # 差分を取得 (unified=3で前後3行のコンテキスト付き)
            diff_cmd = [
                "git", "show", "--unified=3", f"{commit_hash}", "--", file_path
            ]
            
            result = subprocess.run(
                diff_cmd, 
                cwd=self.project_root, 
                capture_output=True, 
                text=True, 
                check=False
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"⚠️  No diff found for {file_path} at commit {commit_hash}")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error getting diff for {file_path}: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error getting diff for {file_path}: {e}")
            return None
    
    def add_line_numbers(self, content: str) -> str:
        """テキストに行番号を付与 (L0001=形式)"""
        lines = content.split('\n')
        numbered_lines = []
        
        for i, line in enumerate(lines, 1):
            numbered_lines.append(f"L{i:04d}={line}")
        
        return '\n'.join(numbered_lines)
    
    def remove_line_numbers(self, content: str) -> str:
        """行番号付きテキストから行番号を除去"""
        lines = content.split('\n')
        clean_lines = []
        
        for line in lines:
            # L0001=形式の行番号を除去
            if re.match(r'^L\d{4}=', line):
                clean_lines.append(line[6:])  # L0001=の6文字を除去
            else:
                clean_lines.append(line)
        
        return '\n'.join(clean_lines)
    
    def validate_line_count_consistency(self, original: str, translated: str) -> bool:
        """翻訳前後の行数一致を検証"""
        original_lines = original.count('\n') + (1 if original else 0)
        translated_lines = translated.count('\n') + (1 if translated else 0)
        
        if original_lines != translated_lines:
            print(f"⚠️  Line count mismatch: original={original_lines}, translated={translated_lines}")
            return False
        
        return True
    
    def create_diff_based_translation_prompt(self, japanese_content: str, diff_content: str, file_path: str = "") -> str:
        """差分ベース翻訳用プロンプトを作成"""
        # カスタムスタイルガイドを取得
        custom_style_guide = self.get_custom_style_guide_for_path(file_path)
        
        # 基本スタイルガイドとカスタムスタイルガイドを統合
        style_guide_section = ""
        if self.style_guide_content or custom_style_guide:
            combined_style_guide = ""
            
            if self.style_guide_content:
                combined_style_guide += f"## 基本スタイルガイド\n\n{self.style_guide_content}\n\n"
            
            if custom_style_guide:
                combined_style_guide += f"## カスタムスタイルガイド（{file_path}）\n\n{custom_style_guide}\n\n"
                combined_style_guide += "**重要**: カスタムスタイルガイドの指示が基本スタイルガイドと異なる場合は、カスタムスタイルガイドを優先してください。\n\n"
            
            style_guide_section = f"""
以下のスタイルガイドに従って翻訳してください：

{combined_style_guide}---

"""
        
        # 行番号付き日本語コンテンツ
        numbered_japanese = self.add_line_numbers(japanese_content)
        
        prompt = f"""{style_guide_section}## 差分ベース最小限翻訳タスク

あなたは、JHipsterドキュメントの日本語翻訳において、**必要最小限の変更のみ**を行う翻訳専門家です。

### upstream英語版の変更差分
以下が、upstream（英語版）リポジトリでの実際の変更差分です：

```diff
{diff_content}
```

### 現在の日本語版（行番号付き）
以下が現在の日本語版の内容です（各行にL0001=形式で行番号が付いています）：

```
{numbered_japanese}
```

### 翻訳指示

**最重要原則**: 意味の変更がない英文修正（typo修正、URL変更、記号変更、大文字小文字変更など）については、対応する日本語行を**一切変更しないでください**。

1. **差分分析**: upstream差分を詳細に分析し、以下を区別してください：
   - 意味的変更: 新しい情報追加、内容の修正、構造変更 → 翻訳更新が必要
   - 表面的変更: typo修正、URL更新、記号変更、空白調整 → 日本語は変更しない

2. **行番号形式維持**: 出力は必ずL0001=形式で各行に行番号を付けてください

3. **変更最小化**: 
   - 意味的変更がある行のみ翻訳を更新
   - 表面的変更のみの行は既存日本語をそのまま維持
   - 変更不要な行は完全に元の内容を保持

4. **保護領域**: 以下は絶対に変更しないでください：
   - コードブロック（```で囲まれた部分）
   - インラインコード（`で囲まれた部分）
   - URL、ファイルパス
   - import/export文
   - JSX属性、HTMLタグ
   - フロントマター（---で囲まれた部分）

5. **行数一致**: 出力の総行数は入力と完全に一致させてください

6. **コンフリクトマーカー**: `<<<<<<<`、`=======`、`>>>>>>>`が残っている場合は、差分情報に基づいて適切に解消してください

### 出力形式
```
L0001=（翻訳された1行目またはそのまま維持）
L0002=（翻訳された2行目またはそのまま維持）
...
```

**注意**: 上記差分で実際に意味が変わった箇所のみを翻訳更新し、他はすべて既存の日本語をそのまま維持してください。"""
        
        return prompt
    
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
    
    def create_translation_prompt(self, content: str, file_path: str = "") -> str:
        """翻訳用プロンプトを作成"""
        # カスタムスタイルガイドを取得
        custom_style_guide = self.get_custom_style_guide_for_path(file_path)
        
        # 基本スタイルガイドとカスタムスタイルガイドを統合
        style_guide_section = ""
        if self.style_guide_content or custom_style_guide:
            combined_style_guide = ""
            
            if self.style_guide_content:
                combined_style_guide += f"## 基本スタイルガイド\n\n{self.style_guide_content}\n\n"
            
            if custom_style_guide:
                combined_style_guide += f"## カスタムスタイルガイド（{file_path}）\n\n{custom_style_guide}\n\n"
                combined_style_guide += "**重要**: カスタムスタイルガイドの指示が基本スタイルガイドと異なる場合は、カスタムスタイルガイドを優先してください。\n\n"
            
            style_guide_section = f"""
以下のスタイルガイドに従って翻訳してください：

{combined_style_guide}---

"""
        
        prompt = f"""{style_guide_section}以下の英語のJHipsterドキュメントを日本語に翻訳してください。

重要な注意事項：
1. マークダウン形式を保持してください
2. コードブロック、URL、ファイルパス、コマンドは翻訳しないでください
3. 技術用語は適切な日本語に翻訳するか、必要に応じて英語のまま残してください
4. 文体は常体（である調）を使用してください
5. **CRITICAL**: 元の文書の行数と改行位置を厳密に保持してください（行の追加・削除は禁止）
6. **CRITICAL**: すでにある日本語は変更せずそのまま維持
7. HTMLタグやマークダウン記法は変更しないでください
8. 空行、段落区切りを完全に維持してください

翻訳対象テキスト：

{content}

翻訳結果（日本語のみ）："""
        
        return prompt
    
    def create_conflict_translation_prompt(self, content: str, stage: str, file_path: str = "") -> str:
        """2段階コンフリクト翻訳用プロンプト（差分ベース強化版）"""
        # カスタムスタイルガイドを取得
        custom_style_guide = self.get_custom_style_guide_for_path(file_path)
        
        # 基本スタイルガイドとカスタムスタイルガイドを統合
        style_guide_section = ""
        if self.style_guide_content or custom_style_guide:
            combined_style_guide = ""
            
            if self.style_guide_content:
                combined_style_guide += f"## 基本スタイルガイド\n\n{self.style_guide_content}\n\n"
            
            if custom_style_guide:
                combined_style_guide += f"## カスタムスタイルガイド（{file_path}）\n\n{custom_style_guide}\n\n"
                combined_style_guide += "**重要**: カスタムスタイルガイドの指示が基本スタイルガイドと異なる場合は、カスタムスタイルガイドを優先してください。\n\n"
            
            style_guide_section = f"""
以下のスタイルガイドに従って翻訳してください：

{combined_style_guide}---

"""
        
        # 差分情報を取得（利用可能であれば）
        diff_section = ""
        if self.commit_hash:
            diff_content = self.get_file_diff(file_path, self.commit_hash)
            if diff_content:
                diff_section = f"""
### 参考：upstream差分情報
以下は、この変更に関連するupstream差分です（判断の参考にしてください）：

```diff
{diff_content}
```

**差分の活用**: 上記差分から、意味の変更がない表面的修正（typo、URL変更等）と、実際の内容変更を区別してください。

"""
        
        if stage == "translate":
            # 第1段階：新規英文を既存日本語スタイルで翻訳
            return f"""{style_guide_section}{diff_section}以下のテキストはGitマージコンフリクトを含むJHipsterドキュメントです。第1段階として、新規英語内容を既存日本語のスタイルに合わせて翻訳してください。

重要：コンフリクトマーカー（<<<<<<<、=======、>>>>>>>）は削除せず、そのまま保持してください。

翻訳指示：
1. <<<<<<< HEAD と ======= の間：既存の日本語版 → 参考として利用（翻訳スタイル、用語選択の基準）
2. ======= と >>>>>>> の間：上流の新規英語版 → 既存日本語のスタイルに合わせて翻訳
3. 既存日本語の文体、用語選択、表現方法を参考にして新規英語を翻訳
4. コンフリクトマーカーは削除しない
5. **CRITICAL**: 行数と改行位置を厳密に保持（行の追加・削除は禁止）
6. **CRITICAL**: コンフリクトマーカーで囲まれた箇所のみ翻訳。他は変更せずそのまま維持
7. マークダウン形式、URL、コマンドは翻訳しない
8. 文体は既存部分と同じ常体（である調）を使用
9. **差分最小化**: 表面的変更のみの場合は既存日本語を最大限保持

入力テキスト：

{content}

第1段階結果（新規英文を既存スタイルで翻訳済み、マーカー保持）："""
        else:  # stage == "merge"
            # 第2段階：HEAD側を削除し、翻訳された新規内容を採用
            return f"""{style_guide_section}{diff_section}以下のテキストはコンフリクトマーカーを含む文書です。第2段階として、HEAD側を完全に削除し、新規翻訳内容のみを採用してください。

マージ指示：
1. <<<<<<< HEAD と ======= の間：既存バージョン → 完全に削除
2. ======= と >>>>>>> の間：翻訳済み新規バージョン → これを採用
3. HEAD側の内容は削除し、新規翻訳内容で完全に置き換える
4. コンフリクトマーカーを完全に削除
5. 最終的には翻訳済み新規内容のみが残る
6. **CRITICAL**: 翻訳後の行数と改行位置を厳密に保持
7. **CRITICAL**: 新規翻訳内容以外の箇所は変更せずそのまま維持
8. マークダウン構造は保持

入力テキスト：

{content}

第2段階結果（HEAD削除、新規翻訳内容のみ採用）："""

    def translate_chunk_diff_based(self, japanese_content: str, file_path: str = "", retry_count: int = 3) -> Optional[str]:
        """差分ベース翻訳を実行"""
        if not self.commit_hash:
            print("   ⚠️  No commit hash provided, falling back to regular translation")
            return self.translate_chunk(japanese_content, file_path, retry_count)
        
        print(f"   Using diff-based translation for commit {self.commit_hash}")
        
        # 差分を取得
        diff_content = self.get_file_diff(file_path, self.commit_hash)
        if not diff_content:
            print(f"   ⚠️  No diff available for {file_path}, using regular translation")
            return self.translate_chunk(japanese_content, file_path, retry_count)
        
        # 差分ベース翻訳プロンプトを作成
        prompt = self.create_diff_based_translation_prompt(japanese_content, diff_content, file_path)
        
        # デバッグ用にプロンプトとdiffをログファイルに保存
        self._save_debug_artifacts(file_path, prompt, diff_content, japanese_content)
        
        # 複数回試行
        for attempt in range(retry_count):
            try:
                response = self.model.generate_content(prompt)
                if response.text:
                    result_with_numbers = response.text.strip()
                    
                    # 行番号を除去
                    final_result = self.remove_line_numbers(result_with_numbers)
                    
                    # 行数一致を検証
                    if self.validate_line_count_consistency(japanese_content, final_result):
                        print(f"   ✅ Diff-based translation completed (attempt {attempt + 1})")
                        
                        # 成功時もartifactに記録
                        self._save_translation_result(file_path, final_result, attempt + 1)
                        return final_result
                    else:
                        print(f"   ⚠️  Line count mismatch in attempt {attempt + 1}, retrying...")
                        
            except Exception as e:
                print(f"   ❌ Diff-based translation attempt {attempt + 1} failed: {e}")
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)
        
        # 差分ベース翻訳が失敗した場合、通常翻訳にフォールバック
        print("   ⚠️  Diff-based translation failed, falling back to regular translation")
        return self.translate_chunk(japanese_content, file_path, retry_count)
    
    def _save_debug_artifacts(self, file_path: str, prompt: str, diff_content: str, japanese_content: str) -> None:
        """デバッグ用のartifactを保存"""
        try:
            artifacts_dir = self.project_root / ".github/auto-translation/artifacts"
            artifacts_dir.mkdir(exist_ok=True)
            
            # ファイル名を安全にする
            safe_file_name = file_path.replace("/", "_").replace("\\", "_")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            
            # プロンプト保存
            prompt_file = artifacts_dir / f"prompt_{safe_file_name}_{timestamp}.md"
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(f"# Diff-based Translation Prompt\n\n")
                f.write(f"**File:** {file_path}\n")
                f.write(f"**Commit:** {self.commit_hash}\n")
                f.write(f"**Timestamp:** {timestamp}\n\n")
                f.write(f"## Prompt Content\n\n")
                f.write(prompt)
            
            # 差分保存
            diff_file = artifacts_dir / f"diff_{safe_file_name}_{timestamp}.diff"
            with open(diff_file, 'w', encoding='utf-8') as f:
                f.write(f"# Upstream Diff for {file_path}\n")
                f.write(f"# Commit: {self.commit_hash}\n")
                f.write(f"# Timestamp: {timestamp}\n\n")
                f.write(diff_content)
            
            # 元の日本語コンテンツ保存
            content_file = artifacts_dir / f"original_{safe_file_name}_{timestamp}.md"
            with open(content_file, 'w', encoding='utf-8') as f:
                f.write(f"# Original Japanese Content for {file_path}\n")
                f.write(f"# Commit: {self.commit_hash}\n")
                f.write(f"# Timestamp: {timestamp}\n\n")
                f.write(japanese_content)
            
            print(f"   📝 Debug artifacts saved: {artifacts_dir}")
            
        except Exception as e:
            print(f"   ⚠️  Failed to save debug artifacts: {e}")
    
    def _save_translation_result(self, file_path: str, result: str, attempt: int) -> None:
        """翻訳結果を保存"""
        try:
            artifacts_dir = self.project_root / ".github/auto-translation/artifacts"
            artifacts_dir.mkdir(exist_ok=True)
            
            # ファイル名を安全にする
            safe_file_name = file_path.replace("/", "_").replace("\\", "_")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            
            # 翻訳結果保存
            result_file = artifacts_dir / f"result_{safe_file_name}_{timestamp}_attempt{attempt}.md"
            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"# Diff-based Translation Result\n\n")
                f.write(f"**File:** {file_path}\n")
                f.write(f"**Commit:** {self.commit_hash}\n")
                f.write(f"**Attempt:** {attempt}\n")
                f.write(f"**Timestamp:** {timestamp}\n\n")
                f.write(f"## Translation Result\n\n")
                f.write(result)
            
        except Exception as e:
            print(f"   ⚠️  Failed to save translation result: {e}")
    
    def _save_conflict_debug_artifacts(self, file_path: str, content: str, prompt: str, stage: str) -> None:
        """コンフリクト翻訳用のartifactを保存"""
        try:
            artifacts_dir = self.project_root / ".github/auto-translation/artifacts"
            artifacts_dir.mkdir(exist_ok=True)
            
            # ファイル名を安全にする
            safe_file_name = file_path.replace("/", "_").replace("\\", "_")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            
            # ステージ別プロンプト保存
            prompt_file = artifacts_dir / f"conflict_{stage}_prompt_{safe_file_name}_{timestamp}.md"
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(f"# 2-Stage Conflict Translation Prompt ({stage.upper()})\n\n")
                f.write(f"**File:** {file_path}\n")
                f.write(f"**Commit:** {self.commit_hash or 'N/A'}\n")
                f.write(f"**Stage:** {stage}\n")
                f.write(f"**Timestamp:** {timestamp}\n\n")
                f.write(f"## Input Content\n\n")
                f.write(f"```\n{content}\n```\n\n")
                f.write(f"## Prompt Content\n\n")
                f.write(prompt)
            
        except Exception as e:
            print(f"   ⚠️  Failed to save conflict debug artifacts: {e}")
    
    def _save_conflict_translation_result(self, file_path: str, result: str, attempt: int) -> None:
        """コンフリクト翻訳結果を保存"""
        try:
            artifacts_dir = self.project_root / ".github/auto-translation/artifacts"
            artifacts_dir.mkdir(exist_ok=True)
            
            # ファイル名を安全にする
            safe_file_name = file_path.replace("/", "_").replace("\\", "_")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            
            # 翻訳結果保存
            result_file = artifacts_dir / f"conflict_result_{safe_file_name}_{timestamp}_attempt{attempt}.md"
            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"# 2-Stage Conflict Translation Result\n\n")
                f.write(f"**File:** {file_path}\n")
                f.write(f"**Commit:** {self.commit_hash or 'N/A'}\n")
                f.write(f"**Attempt:** {attempt}\n")
                f.write(f"**Timestamp:** {timestamp}\n\n")
                f.write(f"## Translation Result\n\n")
                f.write(result)
            
        except Exception as e:
            print(f"   ⚠️  Failed to save conflict translation result: {e}")

    def translate_chunk_two_stage(self, content: str, file_path: str = "", retry_count: int = 3) -> Optional[str]:
        """2段階でコンフリクト翻訳"""
        print("   Using 2-stage conflict resolution...")
        
        # 第1段階：英文翻訳（マーカー保持）
        stage1_prompt = self.create_conflict_translation_prompt(content, "translate", file_path)
        
        # Conflict翻訳のartifactsを保存
        self._save_conflict_debug_artifacts(file_path, content, stage1_prompt, "stage1")
        
        stage1_result = None
        
        for attempt in range(retry_count):
            try:
                response = self.model.generate_content(stage1_prompt)
                if response.text:
                    stage1_result = response.text.strip()
                    print(f"   Stage 1 completed (attempt {attempt + 1})")
                    break
            except Exception as e:
                print(f"   Stage 1 attempt {attempt + 1} failed: {e}")
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)
        
        if not stage1_result:
            print("   Stage 1 failed completely")
            return None
        
        # 第2段階：マージ（マーカー削除）
        stage2_prompt = self.create_conflict_translation_prompt(stage1_result, "merge", file_path)
        
        # Stage2のartifactsを保存
        self._save_conflict_debug_artifacts(file_path, stage1_result, stage2_prompt, "stage2")
        
        for attempt in range(retry_count):
            try:
                response = self.model.generate_content(stage2_prompt)
                if response.text:
                    final_result = response.text.strip()
                    print(f"   Stage 2 completed (attempt {attempt + 1})")
                    
                    # 最終結果を保存
                    self._save_conflict_translation_result(file_path, final_result, attempt + 1)
                    return final_result
            except Exception as e:
                print(f"   Stage 2 attempt {attempt + 1} failed: {e}")
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)
        
        print("   Stage 2 failed, returning stage 1 result")
        return stage1_result

    def translate_chunk(self, content: str, file_path: str = "", retry_count: int = 3) -> Optional[str]:
        """単一チャンクを翻訳"""
        # コンフリクトマーカーがあるかチェック
        has_conflicts = any(marker in content for marker in ['<<<<<<<', '=======', '>>>>>>>'])
        
        if has_conflicts:
            return self.translate_chunk_two_stage(content, file_path, retry_count)
        
        # 差分ベース翻訳が利用可能で、既存の日本語コンテンツの場合は差分ベース翻訳を使用
        if self.commit_hash and self._is_japanese_content(content):
            return self.translate_chunk_diff_based(content, file_path, retry_count)
        
        # 通常翻訳（新規ファイルや英語コンテンツの場合）
        prompt = self.create_translation_prompt(content, file_path)
        
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
            # プロジェクトルートからの相対パスでファイルを読み込み
            full_file_path = self.project_root / file_path
            with open(full_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"📝 Translating: {file_path}")
            
            # コンテンツを分割
            chunks = self.split_content_by_paragraphs(content)
            print(f"   Split into {len(chunks)} chunks")
            
            translated_chunks = []
            for i, chunk in enumerate(chunks):
                print(f"   Translating chunk {i + 1}/{len(chunks)}...")
                translated_chunk = self.translate_chunk(chunk, file_path)
                
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
                full_output_path = full_file_path
            else:
                full_output_path = self.project_root / output_path
            
            # 翻訳結果を保存
            full_output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_output_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            print(f"✅ Translation completed: {full_output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error translating file {file_path}: {e}")
            return False
    
    def translate_files_from_classification(self, classification_file: str, mode: str = "all") -> bool:
        """分類結果から翻訳対象ファイルを翻訳"""
        try:
            # プロジェクトルートからの相対パスで分類ファイルを読み込み
            full_classification_path = self.project_root / classification_file
            with open(full_classification_path, 'r', encoding='utf-8') as f:
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
    parser.add_argument(
        "--commit-hash",
        help="Upstream commit hash for diff-based translation"
    )
    
    args = parser.parse_args()
    
    # API キーをチェック
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "fake_api_key_for_development":
        print("❌ GEMINI_API_KEY environment variable is required")
        sys.exit(1)
    
    translator = GeminiTranslator(api_key, commit_hash=args.commit_hash)
    
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