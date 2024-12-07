from typing import Dict, Any
from langchain.prompts import ChatPromptTemplate
from .base_agent import BaseAgent

class RevisionAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Revision Handler")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "あなたは技術文書の改訂専門家です。"
                      "ユーザーからのフィードバックに基づいて、記事を適切に修正してください。"
                      "修正の際は、元の文章の良い部分を維持しながら、要望に応じた改善を行ってください。"),
            ("user", "以下の技術ブログ記事を、指定された要望に基づいて修正してください：\n\n"
                    "記事：\n{content}\n\n"
                    "要望：\n{feedback}")
        ])
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content = input_data.get("content", "")
        feedback = input_data.get("feedback", "")
        
        chain = self.prompt | self.llm
        response = await chain.ainvoke({
            "content": content,
            "feedback": feedback
        })
        
        result = {
            "content": response.content,
            "status": "revision_applied",
            "feedback_addressed": True
        }
        
        self._log_process(input_data, result)
        return result 