import pytest
from src.agents.draft_agent import DraftAgent
from src.agents.style_agent import StyleAgent
from src.agents.tech_agent import TechnicalAgent
from src.agents.seo_agent import SEOAgent
from src.agents.grammar_agent import GrammarAgent
from src.agents.revision_agent import RevisionAgent

@pytest.mark.asyncio
async def test_draft_agent(test_fragments):
    agent = DraftAgent()
    result = await agent.process({"fragments": test_fragments})
    
    assert "draft" in result
    assert isinstance(result["draft"], str)
    assert len(result["draft"]) > 0
    assert result["status"] == "draft_generated"

@pytest.mark.asyncio
async def test_style_agent(test_content):
    agent = StyleAgent()
    result = await agent.process({"content": test_content})
    
    assert "content" in result
    assert isinstance(result["content"], str)
    assert len(result["content"]) > 0
    assert result["status"] == "style_improved"

@pytest.mark.asyncio
async def test_tech_agent(test_content):
    agent = TechnicalAgent()
    result = await agent.process({"content": test_content})
    
    assert "content" in result
    assert isinstance(result["content"], str)
    assert "changes" in result
    assert result["status"] == "technically_reviewed"

@pytest.mark.asyncio
async def test_seo_agent(test_content):
    agent = SEOAgent()
    result = await agent.process({"content": test_content})
    
    assert "content" in result
    assert "metadata" in result
    assert "keywords" in result["metadata"]
    assert result["status"] == "seo_optimized"

@pytest.mark.asyncio
async def test_grammar_agent(test_content):
    agent = GrammarAgent()
    result = await agent.process({"content": test_content})
    
    assert "content" in result
    assert "corrections" in result
    assert result["status"] == "grammar_checked"

@pytest.mark.asyncio
async def test_revision_agent(test_content):
    agent = RevisionAgent()
    feedback = "もう少し具体的な実装例を追加してください"
    
    result = await agent.process({
        "content": test_content,
        "feedback": feedback
    })
    
    assert "content" in result
    assert result["status"] == "revision_applied"
    assert result["feedback_addressed"] 