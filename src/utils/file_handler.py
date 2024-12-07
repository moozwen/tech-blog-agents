import os
from typing import Dict, Any, Tuple
import yaml
from pathlib import Path

def read_input_file(filename: str) -> Tuple[str, Dict[str, Any], list]:
    """
    入力ファイルを読み込む
    
    Args:
        filename: 入力ファイル名
    
    Returns:
        (タイトル, メタデータ, フラグメントのリスト)
    """
    input_dir = Path("input/fragments")
    file_path = input_dir / filename
    
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        # YAMLフロントマターとコンテンツを分離
        content = f.read()
        if content.startswith("---"):
            _, front_matter, *contents = content.split("---", 2)
            metadata = yaml.safe_load(front_matter)
            main_content = "---".join(contents)
        else:
            metadata = {}
            main_content = content
    
    # フラグメントを抽出（行ごとに分割し、空行を除去）
    fragments = [
        line.strip().lstrip("- ")
        for line in main_content.split("\n")
        if line.strip() and not line.startswith("#")
    ]
    
    return metadata.get("title", ""), metadata, fragments

def save_draft_for_review(content: str, filepath: str) -> str:
    """
    レビュー用の下書きを保存
    
    Args:
        content: 記事の内容
        filepath: 保存先のパス
    
    Returns:
        保存したファイルのパス
    """
    review_dir = Path("output/drafts")
    review_dir.mkdir(parents=True, exist_ok=True)
    
    draft_path = review_dir / f"draft_{Path(filepath).name}"
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return str(draft_path)

def read_feedback(draft_path: str) -> str:
    """
    ユーザーからのフィードバックを読み込む
    
    Args:
        draft_path: 下書きファイルのパス
    
    Returns:
        フィードバックの内容
    """
    feedback_path = Path(draft_path).with_suffix(".feedback.md")
    
    print(f"\n=== フィードバックの入力 ===")
    print(f"1. 下書きファイルを確認: {draft_path}")
    print(f"2. フィードバックファイルを編集: {feedback_path}")
    
    # フィードバックファイルが存在しない場合は作成
    if not feedback_path.exists():
        with open(feedback_path, "w", encoding="utf-8") as f:
            f.write("# フィードバック\n\n")
            f.write("以下に改善点や要望を記入してください：\n\n")
            f.write("- \n")
    
    print("\nフィードバックファイルを作成しました。")
    print("エディタでファイルを開いて編集してください。")
    input("編集が完了したらEnterを押してください...")
    
    if not feedback_path.exists():
        return ""
    
    with open(feedback_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        # テンプレートのみの場合は空とみなす
        if content in ["# フィードバック\n\n以下に改善点や要望を記入してください：\n\n- \n", ""]:
            return ""
        return content 