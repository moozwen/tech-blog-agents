import pytest
from src.graph.blog_graph import BlogGraph
from src.graph.state import BlogState

@pytest.mark.asyncio
async def test_blog_workflow(test_fragments):
    graph = BlogGraph()
    result = await graph.run(fragments=test_fragments)
    
    assert "content" in result
    assert "metadata" in result
    assert "status" in result
    assert result["revision_count"] >= 0

@pytest.mark.asyncio
async def test_blog_state():
    state = BlogState(
        fragments=["テスト用の断片"],
        current_content="テスト用のコンテンツ"
    )
    
    assert state.fragments == ["テスト用の断片"]
    assert state.current_content == "テスト用のコンテンツ"
    assert state.status == "initialized"
    assert state.revision_count == 0
    assert not state.complete

@pytest.mark.asyncio
async def test_workflow_with_revision(test_fragments):
    graph = BlogGraph()
    
    # 初回実行（フィードバックなし）
    initial_result = await graph.run(
        fragments=test_fragments
    )
    assert initial_result["revision_count"] == 0
    
    # フィードバックありで再実行
    final_result = await graph.run(
        fragments=test_fragments,
        feedback="より具体的な例を追加してください"
    )
    
    # 検証
    assert final_result["revision_count"] > 0
    assert final_result["status"] == "ready_to_publish"
    assert len(final_result["content"]) > len(initial_result["content"])