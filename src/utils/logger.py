import logging
from src.config.settings import settings

def setup_logger(name: str) -> logging.Logger:
    """アプリケーション用のロガーをセットアップする"""
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    
    # ハンドラーの設定
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
    logger.addHandler(handler)
    
    return logger

# アプリケーション全体で使用するロガー
app_logger = setup_logger("blog_generator") 