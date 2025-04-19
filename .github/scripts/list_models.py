#!/usr/bin/env python3
import os
import sys

try:
    import google.generativeai as genai
except ImportError:
    print("google.generativeai ライブラリがインストールされていません")
    print("以下のコマンドでインストールしてください:")
    print("pip install google-generativeai")
    sys.exit(1)

# .envファイルまたは環境変数からAPI Keyを読み込む
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("環境変数GEMINI_API_KEYが設定されていません")
    print("以下のコマンドを実行して.envファイルを読み込むか、手動で環境変数を設定してください:")
    print("source .env")
    sys.exit(1)

# Gemini APIを設定
genai.configure(api_key=api_key)

# 利用可能なモデル一覧を取得
try:
    models = genai.list_models()
    
    print("\n=== 利用可能なGemini モデル一覧 ===")
    for model in models:
        print(f"モデル名: {model.name}")
        print(f"表示名: {model.display_name}")
        print(f"説明: {model.description}")
        print(f"サポート機能: {', '.join(model.supported_generation_methods)}")
        print("----------------------------")

    # 特に翻訳に適したモデルをハイライト表示
    print("\n=== 翻訳に適したモデル ===")
    translation_models = [
        model.name for model in models 
        if "generateContent" in model.supported_generation_methods
    ]
    
    for model_name in translation_models:
        print(f"- {model_name}")

    # 結果を要約
    print(f"\n合計 {len(models)} モデルが利用可能、うち翻訳向け {len(translation_models)} モデル")
    
except Exception as e:
    print(f"エラーが発生しました: {e}")