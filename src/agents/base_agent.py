from typing import Any, Dict
from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from src.config.settings import settings
from src.utils.logger import app_logger

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = app_logger
        self.llm = ChatOpenAI(
            model_name=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE
        )
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        エージェントの基本的な処理メソッド
        Args:
            input_data: 入力データ
        Returns:
            処理結果
        """
        pass
    
    def _log_process(self, input_data: Dict[str, Any], output_data: Dict[str, Any]):
        """処理のログを記録"""
        self.logger.info(f"{self.name} - Processing started")
        self.logger.debug(f"{self.name} - Input: {input_data}")
        self.logger.debug(f"{self.name} - Output: {output_data}")
        self.logger.info(f"{self.name} - Processing completed") 