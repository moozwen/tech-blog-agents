from typing import Dict, Any
from langchain.prompts import ChatPromptTemplate
from .base_agent import BaseAgent
from src.config.settings import settings

class DraftAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Draft Generator")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", f"""あなたは技術ブログの記事を執筆する専門家です。
与えられた断片的な情報から、技術ブログ記事の初稿を作成してください。

要件：
- 文字数: {settings.TARGET_WORD_COUNT}文字程度
- 技術的な正確性を重視
- コード例を含める
- 段階的な説明
- 読者が実践できる具体的な手順
- 見出しを適切に使用した構造化

出力形式:
# タイトル

## はじめに
(概要、背景)

## 技術解説
(主要な技術の説明)

## 実装手順
(具体的な実装ステップ)

## コード例
(実際のコードと説明)

## まとめ
(結論、次のステップ)
"""),
            ("user", "以下の情報をもとに、技術ブログ記事の初稿を作成してください：\n\n{fragments}")
        ])
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        fragments = input_data.get("fragments", [])
        
        # 断片をテキストに結合
        fragments_text = "\n".join(fragments) if isinstance(fragments, list) else fragments
        
        # LLMで記事生成
        chain = self.prompt | self.llm
        response = await chain.ainvoke({"fragments": fragments_text})
        
        result = {
            "draft": response.content,
            "status": "draft_generated"
        }
        
        self._log_process(input_data, result)
        return result 