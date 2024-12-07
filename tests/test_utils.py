import os
import pytest
from src.utils.text_processing import save_blog_to_markdown, calculate_diff
from src.config.settings import settings

def test_save_blog_to_markdown(test_content, test_metadata):
    title = "テスト記事"
    filepath = save_blog_to_markdown(test_content, title, test_metadata)
    
    assert os.path.exists(filepath)
    assert filepath.endswith(".md")
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        assert title in content
        assert test_content in content

def test_calculate_diff():
    original = "これは元のテキストです。"
    updated = "これは更新されたテキストです。"
    
    diff = calculate_diff(original, updated)
    assert isinstance(diff, str)
    assert len(diff) > 0 