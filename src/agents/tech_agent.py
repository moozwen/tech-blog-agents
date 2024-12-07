from typing import Dict, Any
from langchain.prompts import ChatPromptTemplate
from .base_agent import BaseAgent

class TechnicalAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Technical Reviewer")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "あなたは技術文書の正確性を検証する専門家です。"
                      "技術的な誤り、不正確な説明、誤解を招く表現を見つけ、修正してください。"
                      "必要に応じて、技術的な補足説明も追加してください。"),
            ("user", "以下の技術ブログ記事の技術的な正確性を確認し、必要な修正を行ってください：\n\n{content}")
        ])
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content = input_data.get("content", "")
        
        chain = self.prompt | self.llm
        response = await chain.ainvoke({"content": content})
        
        result = {
            "content": response.content,
            "status": "technically_reviewed",
            "changes": self._extract_changes(content, response.content)
        }
        
        self._log_process(input_data, result)
        return result
    
    def _extract_changes(self, original: str, updated: str) -> list:
        """技術的な変更点をリストアップ"""
        # TODO: より詳細な差分分析の実装
        return ["技術的な修正点のリスト"] 