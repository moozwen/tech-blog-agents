import os
import sys
from pathlib import Path

# プロジェクトルートディレクトリをPythonパスに追加
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

import pytest
from src.config.settings import settings

@pytest.fixture
def test_fragments():
    return [
        "Python と LangGraph によるAIエージェント開発",
        "複数のAIエージェントの連携",
        "非同期処理とワークフロー制御"
    ]

@pytest.fixture
def test_content():
    return """
# Python と LangGraph によるAIエージェント開発

この記事では、Python と LangGraph を使用したAIエージェントの開発方法について説明します。
    """

@pytest.fixture
def test_metadata():
    return {
        "keywords": ["Python", "LangGraph", "AI", "エージェント開発"],
        "meta_description": "PythonとLangGraphを使用したAIエージェント開発の入門ガイド"
    } 