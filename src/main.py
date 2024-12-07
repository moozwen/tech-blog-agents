import asyncio
import traceback
import argparse
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from src.graph.blog_graph import BlogGraph
from src.utils.text_processing import save_blog_to_markdown
from src.utils.file_handler import read_input_file, save_draft_for_review, read_feedback
from src.utils.logger import app_logger

async def generate_blog(
    fragments: List[str],
    title: str,
    metadata: Dict[str, Any] = None,
    feedback: str = None,
    revision_history: List[str] = None
) -> Dict[str, Any]:
    """
    ブログ記事を生成する
    
    Args:
        fragments: 記事の断片情報
        title: 記事タイトル
        metadata: メタデータ（オプション）
        feedback: ユーザーからのフィードバック（オプション）
        revision_history: リビジョン履歴（オプション）
    
    Returns:
        生成された記事の情報
    """
    try:
        # ワークフローの実行
        graph = BlogGraph()
        result = await graph.run(fragments)
        
        # メタデータの準備
        combined_metadata = {
            **(metadata or {}),
            **result["metadata"],
            "created_at": datetime.now().isoformat(),
            "word_count": len(result["content"]),
            "revision_count": result["revision_count"]
        }
        
        # Markdownファイルとして保存
        filepath = save_blog_to_markdown(
            content=result["content"],
            title=title,
            metadata=combined_metadata
        )
        
        app_logger.info(f"Blog post saved to: {filepath}")
        
        # リビジョン履歴の管理
        if revision_history is None:
            revision_history = []
        revision_history.append(filepath)
        
        # 下書きを保存してフィードバックを待つ
        if not feedback:
            while True:
                draft_path = save_draft_for_review(result["content"], filepath)
                feedback = read_feedback(draft_path)
                
                if feedback:
                    print("\n=== フィードバックを反映して記事を再生成します ===")
                    # フィードバックがある場合は再生成
                    return await generate_blog(
                        fragments=fragments,
                        title=title,
                        metadata=combined_metadata,
                        feedback=feedback,
                        revision_history=revision_history
                    )
                else:
                    # フィードバックがない場合、ユーザーに確認
                    if input("\n記事の内容に満足しましたか？ (y/N): ").lower() == 'y':
                        print("\n=== 記事が完成しました ===")
                        break
                    else:
                        print("\n=== 新しいフィードバックを入力してください ===")
                        continue
        
        # リビジョン履歴をメタデータに追加
        combined_metadata["revision_history"] = revision_history
        
        return {
            "content": result["content"],
            "metadata": combined_metadata,
            "status": result["status"],
            "filepath": filepath,
            "revision_history": revision_history
        }
    
    except Exception as e:
        app_logger.error(f"Error generating blog: {str(e)}")
        raise

async def main():
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description="技術ブログ記事生成ツール")
    parser.add_argument(
        "input_file",
        help="入力ファイル名（input/fragments/配下のMarkdownファイル）"
    )
    parser.add_argument(
        "--no-feedback",
        action="store_true",
        help="フィードバックプロセスをスキップする"
    )
    args = parser.parse_args()
    
    try:
        # 入力ファイルの読み込み
        title, metadata, fragments = read_input_file(args.input_file)
        
        # ブログ生成の実行（フィードバックスキップオプション付き）
        result = await generate_blog(
            fragments=fragments,
            title=title,
            metadata=metadata,
            feedback="" if args.no_feedback else None
        )
        
        print("\n=== ブログ生成完了 ===")
        print(f"保存先: {result['filepath']}")
        print("\n=== メタデータ ===")
        for key, value in result["metadata"].items():
            print(f"{key}: {value}")
        
        # 生成された記事の内容を表示
        print("\n=== 生成された記事 ===")
        with open(result["filepath"], "r", encoding="utf-8") as f:
            print(f.read())
    
    except Exception as e:
        print(f"\nエラーが発生しました: {str(e)}")
        print("\nスタックトレース:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 