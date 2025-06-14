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
from typing import Optional, Dict, List
import google.generativeai as genai


class CommitAndPRManager:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.bot_user = os.getenv("BOT_GIT_USER", "jhipster-auto-translation-bot")
        self.bot_email = os.getenv("BOT_GIT_EMAIL", "bot@jhipster.tech")
        
        # Gemini API初期化
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and api_key != "fake_api_key_for_development":
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            self.model = None
    
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
    
    def analyze_translation_quality_with_llm(self, upstream_content: str, translated_content: str, file_path: str) -> Dict:
        """LLMを使って翻訳品質を分析"""
        if not self.model:
            return {"has_issues": False, "analysis": "LLM not available"}
        
        prompt = f"""以下の英語文書とその日本語翻訳を比較し、翻訳の品質問題を分析してください。

**翻訳前（英語原文）:**
```
{upstream_content}
```

**翻訳後（日本語版）:**
```
{translated_content}
```

**分析項目:**
1. 重要な情報の欠落（import文、画像、リンク、コンポーネントなど）
2. 構造的な変更（セクション、段落の削除・追加）
3. マークダウン記法の問題
4. 意図しない内容の重複
5. 翻訳の一貫性

**出力形式（JSON）:**
```json
{{
  "has_issues": true/false,
  "issues": [
    {{
      "type": "missing_content|structural_change|markdown_issue|duplication|inconsistency",
      "severity": "high|medium|low",
      "description": "具体的な問題の説明",
      "location": "問題のある箇所（可能な場合）"
    }}
  ],
  "summary": "分析結果の要約"
}}
```

JSON形式で回答してください。"""
        
        try:
            response = self.model.generate_content(prompt)
            if response.text:
                # JSONの抽出を試行
                response_text = response.text.strip()
                if response_text.startswith("```json"):
                    response_text = response_text[7:-3].strip()
                elif response_text.startswith("```"):
                    response_text = response_text[3:-3].strip()
                
                analysis = json.loads(response_text)
                return analysis
            else:
                return {"has_issues": False, "analysis": "No response from LLM"}
                
        except Exception as e:
            print(f"⚠️ Error in LLM analysis for {file_path}: {e}")
            return {"has_issues": False, "analysis": f"Analysis failed: {e}"}
    
    def check_line_count_differences(self, commit_hash: str, classification_file: Optional[str] = None, threshold: int = 1) -> List[Dict]:
        """行数差をチェックし、差があるファイルを返す"""
        files_with_line_differences = []
        
        # 分類ファイルから翻訳対象ファイルを取得
        files_to_check = []
        if classification_file and os.path.exists(classification_file):
            try:
                with open(classification_file, 'r', encoding='utf-8') as f:
                    classification = json.load(f)
                
                # 翻訳対象ファイル（a, b-1, b-2）を収集
                summary = classification.get("summary", {})
                files_to_check.extend(summary.get("a", []))
                files_to_check.extend(summary.get("b-1", []))
                files_to_check.extend(summary.get("b-2", []))
                
            except Exception as e:
                print(f"⚠️ Error reading classification file for line count check: {e}")
                return files_with_line_differences
        
        # 各ファイルの行数をチェック
        for file_path in files_to_check:
            try:
                # 現在のファイル内容と行数
                if not os.path.exists(file_path):
                    continue
                    
                with open(file_path, 'r', encoding='utf-8') as f:
                    current_content = f.read()
                    current_lines = len(current_content.split('\n'))
                
                # 上流コミットでのファイル内容と行数
                try:
                    result = subprocess.run(
                        ["git", "show", f"{commit_hash}:{file_path}"],
                        capture_output=True, text=True, check=True
                    )
                    upstream_content = result.stdout
                    upstream_lines = len(upstream_content.split('\n'))
                    
                    # 行数の差をチェック（1行でも差があれば検出）
                    line_diff = abs(current_lines - upstream_lines)
                    if line_diff >= threshold:
                        diff_ratio = (line_diff / upstream_lines * 100) if upstream_lines > 0 else 0
                        files_with_line_differences.append({
                            "file": file_path,
                            "upstream_lines": upstream_lines,
                            "current_lines": current_lines,
                            "line_diff": line_diff,
                            "diff_ratio": round(diff_ratio, 1),
                            "upstream_content": upstream_content,
                            "current_content": current_content
                        })
                        print(f"📏 Line count difference detected in {file_path}: {upstream_lines} → {current_lines} (差:{line_diff}行)")
                    
                except subprocess.CalledProcessError:
                    # 上流にファイルが存在しない場合
                    continue
                    
            except Exception as e:
                print(f"⚠️ Error checking line count for {file_path}: {e}")
                continue
        
        return files_with_line_differences
    
    def check_translation_quality(self, commit_hash: str, classification_file: Optional[str] = None) -> Dict[str, List[Dict]]:
        """行数差があるファイルのみLLMで翻訳品質を分析"""
        results = {"files_with_issues": [], "analysis_summary": [], "line_count_differences": []}
        
        # 1. まず行数差をチェック
        files_with_line_differences = self.check_line_count_differences(commit_hash, classification_file)
        results["line_count_differences"] = files_with_line_differences
        
        if not files_with_line_differences:
            print("✅ No significant line count differences detected")
            return results
        
        if not self.model:
            print("⚠️ LLM not available for detailed analysis of files with line differences")
            return results
        
        print(f"🔍 Found {len(files_with_line_differences)} files with line count differences, analyzing with LLM...")
        
        # 2. 行数差があるファイルのみLLMで詳細分析
        for file_info in files_with_line_differences:
            file_path = file_info["file"]
            upstream_content = file_info["upstream_content"]
            current_content = file_info["current_content"]
            
            try:
                print(f"🤖 LLM analyzing {file_path}...")
                analysis = self.analyze_translation_quality_with_llm(
                    upstream_content, current_content, file_path
                )
                
                # 行数情報を分析結果に追加
                analysis["line_info"] = {
                    "upstream_lines": file_info["upstream_lines"],
                    "current_lines": file_info["current_lines"],
                    "line_diff": file_info["line_diff"],
                    "diff_ratio": file_info["diff_ratio"]
                }
                
                if analysis.get("has_issues", False):
                    results["files_with_issues"].append({
                        "file": file_path,
                        "analysis": analysis
                    })
                
                results["analysis_summary"].append({
                    "file": file_path,
                    "has_issues": analysis.get("has_issues", False),
                    "summary": analysis.get("summary", "No summary available"),
                    "line_info": analysis["line_info"]
                })
                
            except Exception as e:
                print(f"⚠️ Error in LLM analysis for {file_path}: {e}")
                # LLM分析に失敗した場合でも行数情報は記録
                results["analysis_summary"].append({
                    "file": file_path,
                    "has_issues": True,
                    "summary": f"LLM analysis failed: {e}",
                    "line_info": {
                        "upstream_lines": file_info["upstream_lines"],
                        "current_lines": file_info["current_lines"],
                        "line_diff": file_info["line_diff"],
                        "diff_ratio": file_info["diff_ratio"]
                    }
                })
        
        return results
    
    def check_changes_exist(self) -> bool:
        """変更があるかチェック（コミット前の確認用）"""
        try:
            # 変更されたファイルを確認（ステージされていない変更も含む）
            result = subprocess.run(
                ["git", "diff", "--name-only", "HEAD"],
                capture_output=True, text=True, check=True
            )
            
            changed_files = [f for f in result.stdout.strip().split('\n') if f]
            
            if changed_files:
                print(f"📋 Found {len(changed_files)} changed files")
                for file in changed_files[:10]:  # 最初の10ファイルのみ表示
                    print(f"   - {file}")
                if len(changed_files) > 10:
                    print(f"   ... and {len(changed_files) - 10} more files")
                return True
            else:
                print("📋 No changes detected")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error checking changes: {e}")
            return False
    
    def create_commit(self, commit_hash: str) -> bool:
        """翻訳済み変更をコミット（二次コミット）"""
        commit_message = f"docs(sync): upstream {commit_hash} 翻訳\n\n🤖 Generated with [Claude Code](https://claude.ai/code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>"
        
        try:
            if not self.dry_run:
                # ステージング（翻訳済みファイルを含む全変更）
                subprocess.run(["git", "add", "-A"], check=True)
                
                # 二次コミット
                subprocess.run(
                    ["git", "commit", "-m", commit_message],
                    check=True
                )
            else:
                print("DRY RUN: Would stage and commit with message:")
                print(f"   git add -A")
                print(f"   git commit -m \"{commit_message}\"")
            
            print(f"✅ Created translation commit: docs(sync): upstream {commit_hash} 翻訳")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating translation commit: {e}")
            return False
    
    def check_conflict_markers_in_changed_files(self) -> List[str]:
        """syncブランチで変更された翻訳対象ファイルでコンフリクトマーカーの存在をチェック"""
        files_with_conflicts = []
        
        try:
            # git diff --name-onlyで変更されたファイルを取得
            result = subprocess.run(
                ["git", "diff", "--name-only", "origin/main..HEAD"],
                capture_output=True, text=True, check=True
            )
            
            changed_files = [f for f in result.stdout.strip().split('\n') if f]
            
            for file_path in changed_files:
                if not file_path or not os.path.exists(file_path):
                    continue
                
                # ルートディレクトリの '.' で始まるファイル・フォルダを除外（翻訳対象外）
                if file_path.startswith('.'):
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if any(marker in content for marker in ['<<<<<<<', '=======', '>>>>>>>']):
                            files_with_conflicts.append(file_path)
                except Exception:
                    # ファイル読み込みエラーは無視
                    continue
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Error checking conflict markers: {e}")
        
        return files_with_conflicts

    def generate_pr_body(self, classification_file: Optional[str] = None, commit_hash: Optional[str] = None) -> str:
        """PR本文を生成"""
        body_parts = []
        
        body_parts.append("## 🔄 Upstream同期と翻訳")
        body_parts.append("")
        body_parts.append("このPRは、JHipster upstream リポジトリからの変更を自動的に翻訳したものです。")
        body_parts.append("")
        
        # コミットハッシュ情報を追加
        if commit_hash:
            body_parts.append("### 📍 翻訳元情報")
            body_parts.append("")
            body_parts.append(f"- **Upstream commit**: [{commit_hash}](https://github.com/jhipster/jhipster.github.io/commit/{commit_hash})")
            body_parts.append("")
            
            # 翻訳品質分析を実行（行数差チェック → LLM分析）
            quality_results = self.check_translation_quality(commit_hash, classification_file)
            
            if quality_results["line_count_differences"]:
                body_parts.append("### 📏 行数差異検出結果")
                body_parts.append("")
                body_parts.append("以下のファイルで上流版と行数差が検出されました：")
                body_parts.append("")
                
                for line_diff in quality_results["line_count_differences"]:
                    body_parts.append(f"- `{line_diff['file']}`: {line_diff['upstream_lines']}行 → {line_diff['current_lines']}行 (差:{line_diff['line_diff']}行)")
                body_parts.append("")
                
                if quality_results["files_with_issues"]:
                    body_parts.append("### 🤖 LLM詳細分析結果")
                    body_parts.append("")
                    body_parts.append("行数差異が検出されたファイルのLLM分析結果：")
                    body_parts.append("")
                    
                    for file_result in quality_results["files_with_issues"]:
                        file_path = file_result["file"]
                        analysis = file_result["analysis"]
                        line_info = analysis.get("line_info", {})
                        
                        body_parts.append(f"#### 📄 `{file_path}`")
                        body_parts.append("")
                        body_parts.append(f"**行数**: {line_info.get('upstream_lines', 'N/A')}行 → {line_info.get('current_lines', 'N/A')}行 (差:{line_info.get('line_diff', 'N/A')}行)")
                        body_parts.append(f"**LLM分析**: {analysis.get('summary', 'N/A')}")
                        body_parts.append("")
                        
                        issues = analysis.get("issues", [])
                        if issues:
                            body_parts.append("**検出された問題:**")
                            for issue in issues:
                                severity_emoji = {"high": "🚨", "medium": "⚠️", "low": "ℹ️"}.get(issue.get("severity", "low"), "ℹ️")
                                body_parts.append(f"- {severity_emoji} **{issue.get('type', 'unknown')}**: {issue.get('description', 'N/A')}")
                                if issue.get('location'):
                                    body_parts.append(f"  - 箇所: {issue['location']}")
                            body_parts.append("")
                    
                    body_parts.append("**🔍 手動レビューを強く推奨します。**")
                    body_parts.append("")
                    
                elif quality_results["analysis_summary"]:
                    body_parts.append("### ✅ LLM分析結果")
                    body_parts.append("")
                    body_parts.append("行数差異があるファイルをLLM分析しましたが、重大な問題は検出されませんでした：")
                    body_parts.append("")
                    
                    for summary in quality_results["analysis_summary"]:
                        line_info = summary.get("line_info", {})
                        body_parts.append(f"- ✅ `{summary['file']}` ({line_info.get('upstream_lines', 'N/A')} → {line_info.get('current_lines', 'N/A')}行, 差:{line_info.get('line_diff', 'N/A')}行): {summary['summary']}")
                    body_parts.append("")
                else:
                    body_parts.append("⚠️ 行数差異ファイルのLLM分析ができませんでした（LLM未利用）。手動確認を推奨します。")
                    body_parts.append("")
                    
            else:
                body_parts.append("### ✅ 翻訳品質チェック結果")
                body_parts.append("")
                body_parts.append("行数チェックで大幅な差異は検出されませんでした。翻訳品質に問題はないと判断されます。")
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
        
        # コンフリクトマーカーチェック
        files_with_conflicts = self.check_conflict_markers_in_changed_files()
        if files_with_conflicts:
            body_parts.append("### ⚠️ コンフリクトマーカー検出")
            body_parts.append("")
            body_parts.append("以下のファイルにコンフリクトマーカーが残っています：")
            body_parts.append("")
            for conflict_file in files_with_conflicts:
                body_parts.append(f"- ⚠️ `{conflict_file}` - コンフリクトマーカーが含まれています")
            body_parts.append("")
            body_parts.append("**🚨 これらのファイルは手動で修正が必要です。**")
            body_parts.append("")
        
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
    
    def get_base_branch(self, branch_name: str) -> str:
        """ブランチの派生元を検出してベースブランチを決定"""
        try:
            # 候補ブランチリスト（優先順位順）
            candidate_branches = ["main", "auto-translation"]
            
            best_base = "main"  # デフォルト
            best_distance = float('inf')
            
            for candidate in candidate_branches:
                try:
                    # 現在のブランチと候補ブランチの共通祖先を取得
                    result = subprocess.run(
                        ["git", "merge-base", "HEAD", candidate],
                        capture_output=True, text=True, check=True
                    )
                    merge_base = result.stdout.strip()
                    
                    # 共通祖先から現在のブランチまでのコミット数を取得
                    result = subprocess.run(
                        ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
                        capture_output=True, text=True, check=True
                    )
                    distance = int(result.stdout.strip())
                    
                    # より近い祖先を持つブランチを選択
                    if distance < best_distance:
                        best_distance = distance
                        best_base = candidate
                        
                except subprocess.CalledProcessError:
                    # ブランチが存在しない場合は無視
                    continue
            
            print(f"📍 Detected base branch: {best_base} (distance: {best_distance} commits)")
            return best_base
            
        except Exception as e:
            print(f"⚠️ Error detecting base branch: {e}, using default 'main'")
            return "main"

    def create_pull_request(self, branch_name: str, commit_hash: str, classification_file: Optional[str] = None) -> bool:
        """プルリクエストを作成"""
        pr_title = f"docs: upstream {commit_hash} Translation"
        pr_body = self.generate_pr_body(classification_file, commit_hash)
        
        # ベースブランチを自動検出
        base_branch = self.get_base_branch(branch_name)
        
        # ドライラン時は常にPR本文を標準出力
        if self.dry_run:
            print("=" * 80)
            print("DRY RUN: PR本文（Markdown形式）")
            print("=" * 80)
            print()
            print(f"# {pr_title}")
            print(f"Base branch: {base_branch}")
            print()
            print(pr_body)
            print()
            print("=" * 80)
            return True
        
        try:
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
                "--base", base_branch
            ], check=True)
            
            print(f"✅ Created pull request: {pr_title} (base: {base_branch})")
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
    
    # 変更があるかチェック
    has_changes = manager.check_changes_exist()
    
    # 変更がない場合
    if not has_changes:
        print("📋 No changes to commit")
        # ドライラン時はPR本文生成のみ実行
        if dry_run and create_pr:
            manager.create_pull_request(branch_name, commit_hash, args.classification)
            print("✅ Dry run completed")
        sys.exit(0)
    
    # 通常モード：コミットを作成
    if not dry_run:
        if not manager.create_commit(commit_hash):
            sys.exit(1)
    else:
        print(f"DRY RUN: Would create commit with message: docs(sync): upstream {commit_hash} 翻訳")
    
    # originにプッシュ
    if push_origin and not dry_run:
        if not manager.push_to_origin(branch_name):
            sys.exit(1)
    elif push_origin and dry_run:
        print(f"DRY RUN: Would push branch {branch_name} to origin")
    
    # プルリクエストを作成
    if create_pr:
        if not manager.create_pull_request(branch_name, commit_hash, args.classification):
            if not dry_run:  # ドライラン時はエラー終了しない
                sys.exit(1)
    
    completion_msg = "✅ Dry run completed" if dry_run else "✅ All operations completed successfully"
    print(completion_msg)


if __name__ == "__main__":
    main()