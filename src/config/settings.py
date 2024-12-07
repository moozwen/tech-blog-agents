import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # OpenAI API設定
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME")
    TEMPERATURE = 0.7
    
    # 記事設定
    MAX_TOKENS = 6000  # 記事の最大トークン数
    TARGET_WORD_COUNT = 4000  # 目標文字数
    
    # ログ設定
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 出力設定
    OUTPUT_DIR = "output/blogs"

settings = Settings() 