from typing import Dict, Any
from langchain.prompts import ChatPromptTemplate
from .base_agent import BaseAgent

class SEOAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="SEO Optimizer")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "あなたはSEO最適化の専門家です。"
                      "技術ブログ記事のSEOスコアを向上させ、検索エンジンでの表示順位を改善してください。"
                      "ただし、コンテンツの質と自然な読み心地を損なわないように注意してください。"),
            ("user", "以下の技術ブログ記事をSEO観点で最適化してください：\n\n{content}")
        ])
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content = input_data.get("content", "")
        
        chain = self.prompt | self.llm
        response = await chain.ainvoke({"content": content})
        
        result = {
            "content": response.content,
            "status": "seo_optimized",
            "metadata": {
                "keywords": self._extract_keywords(response.content),
                "meta_description": self._generate_meta_description(response.content)
            }
        }
        
        self._log_process(input_data, result)
        return result
    
    def _extract_keywords(self, content: str) -> list:
        """主要なキーワードを抽出"""
        # TODO: キーワード抽出ロジックの実装
        return ["keyword1", "keyword2"]
    
    def _generate_meta_description(self, content: str) -> str:
        """メタディスクリプションを生成"""
        # TODO: メタディスクリプション生成ロジックの実装
        return "Meta description for the blog post" 