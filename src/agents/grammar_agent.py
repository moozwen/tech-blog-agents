from typing import Dict, Any
from langchain.prompts import ChatPromptTemplate
from .base_agent import BaseAgent

class GrammarAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Grammar Checker")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "あなたは文法と表記の専門家です。"
                      "文法的な誤り、誤字脱字、表記の一貫性などをチェックし、修正してください。"),
            ("user", "以下の技術ブログ記事の文法と表記をチェックし、必要な修正を行ってください：\n\n{content}")
        ])
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content = input_data.get("content", "")
        
        chain = self.prompt | self.llm
        response = await chain.ainvoke({"content": content})
        
        result = {
            "content": response.content,
            "status": "grammar_checked",
            "corrections": self._find_corrections(content, response.content)
        }
        
        self._log_process(input_data, result)
        return result
    
    def _find_corrections(self, original: str, corrected: str) -> list:
        """修正箇所をリストアップ"""
        # TODO: 修正箇所の詳細な分析
        return ["修正箇所のリスト"] 