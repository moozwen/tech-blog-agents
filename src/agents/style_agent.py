from typing import Dict, Any
from langchain.prompts import ChatPromptTemplate
from .base_agent import BaseAgent

class StyleAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Style Editor")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "あなたは技術文書のスタイル編集の専門家です。"
                      "文章を読みやすく、簡潔で、プロフェッショナルな表現に改善してください。"
                      "ただし、技術的な正確性は維持してください。"),
            ("user", "以下の技術ブログ記事を、読みやすく洗練された文章に改善してください：\n\n{content}")
        ])
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content = input_data.get("content", "")
        
        chain = self.prompt | self.llm
        response = await chain.ainvoke({"content": content})
        
        result = {
            "content": response.content,
            "status": "style_improved"
        }
        
        self._log_process(input_data, result)
        return result 