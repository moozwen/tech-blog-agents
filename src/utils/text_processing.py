from typing import List, Dict
import os
from datetime import datetime
from src.config.settings import settings

def save_blog_to_markdown(content: str, title: str, metadata: Dict = None) -> str:
    """
    ブログ記事をMarkdownファイルとして保存
    
    Args:
        content: 記事本文
        title: 記事タイトル
        metadata: メタデータ（オプション）
    
    Returns:
        保存したファイルのパス
    """
    # ファイル名用に日付を取得
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{date_str}-{title.replace(' ', '-').lower()}.md"
    
    # 出力ディレクトリの作成
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(settings.OUTPUT_DIR, filename)
    
    # メタデータの準備
    metadata_text = ""
    if metadata:
        metadata_text = "---\n"
        for key, value in metadata.items():
            if isinstance(value, list):
                metadata_text += f"{key}:\n"
                for item in value:
                    metadata_text += f"  - {item}\n"
            else:
                metadata_text += f"{key}: {value}\n"
        metadata_text += "---\n\n"
    
    # 記事の構造化
    article_text = [
        metadata_text,
        f"# {title}\n",
        content,
        "\n---\n",
        f"*この記事は{datetime.now().strftime('%Y年%m月%d日')}に生成されました。*"
    ]
    
    # ファイルの保存
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(article_text))
    
    return filepath

def calculate_diff(original: str, updated: str) -> str:
    """
    オリジナルテキストと更新後テキストの差分を計算
    
    Args:
        original: オリジナルテキスト
        updated: 更新後テキスト
    
    Returns:
        差分の説明
    """
    # TODO: より高度な差分計算アルゴリズムの実装
    return "変更点のサマリー" 