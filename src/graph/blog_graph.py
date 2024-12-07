from typing import Dict, Any, List, Annotated, Optional
from langgraph.graph import Graph, StateGraph
from langgraph.prebuilt import ToolExecutor
from src.graph.state import BlogState
from src.agents.draft_agent import DraftAgent
from src.agents.style_agent import StyleAgent
from src.agents.tech_agent import TechnicalAgent
from src.agents.seo_agent import SEOAgent
from src.agents.grammar_agent import GrammarAgent
from src.agents.revision_agent import RevisionAgent

class BlogGraph:
    def __init__(self):
        # エージェントのインスタンス化
        self.draft_agent = DraftAgent()
        self.style_agent = StyleAgent()
        self.tech_agent = TechnicalAgent()
        self.seo_agent = SEOAgent()
        self.grammar_agent = GrammarAgent()
        self.revision_agent = RevisionAgent()
        
        # グラフの構築
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """ワークフローグラフを構築"""
        # グラフの初期化
        workflow = StateGraph(BlogState)
        
        # ノードの追加
        workflow.add_node("create_draft", self._draft_step)
        workflow.add_node("improve_style", self._style_step)
        workflow.add_node("review_technical", self._technical_step)
        workflow.add_node("handle_revision", self._revision_step)
        
        # 完了ノードの追加
        def prepare_for_publishing(state: BlogState) -> BlogState:
            """ブログ公開準備ステップ"""
            state.complete = True
            state.status = "ready_to_publish"
            return state
        
        workflow.add_node("prepare_publishing", prepare_for_publishing)
        
        # エッジの定義
        workflow.add_edge("create_draft", "improve_style")
        workflow.add_edge("improve_style", "review_technical")
        workflow.add_edge("review_technical", "prepare_publishing")
        
        # リビジョンループの設定
        workflow.add_conditional_edges(
            "review_technical",
            self._needs_revision,
            {
                True: "handle_revision",
                False: "prepare_publishing"
            }
        )
        workflow.add_edge("handle_revision", "improve_style")
        
        # 終了条件の設定
        workflow.set_entry_point("create_draft")
        workflow.set_finish_point("prepare_publishing")
        
        return workflow.compile()
    
    async def run(self, fragments: List[str], feedback: Optional[str] = None) -> Dict[str, Any]:
        """ワークフローを実行
        
        Args:
            fragments: 記事の断片情報のリスト
            feedback: ユーザーからのフィードバック（オプション）
        
        Returns:
            生成された記事の情報
        """
        initial_state = BlogState(
            fragments=fragments,
            feedback=feedback
        )
        
        # 各ステップを順番に実行
        state = initial_state
        
        # ドラフト生成
        state = await self._draft_step(state)
        
        # スタイル改善
        state = await self._style_step(state)
        
        # 技術レビュー
        state = await self._technical_step(state)
        
        # リビジョンが必要な場合は処理
        if self._needs_revision(state):
            state = await self._revision_step(state)
            state = await self._style_step(state)
            state = await self._technical_step(state)
        
        # 完了処理
        state.complete = True
        state.status = "ready_to_publish"
        
        return {
            "content": state.current_content,
            "metadata": state.metadata,
            "status": state.status,
            "revision_count": state.revision_count
        }
    
    async def _draft_step(self, state: BlogState) -> BlogState:
        """ドラフト生成ステップ"""
        result = await self.draft_agent.process({"fragments": state.fragments})
        state.draft = result["draft"]
        state.current_content = result["draft"]
        state.status = "draft_generated"
        return state
    
    async def _style_step(self, state: BlogState) -> BlogState:
        """スタイル改善ステップ"""
        result = await self.style_agent.process({"content": state.current_content})
        state.current_content = result["content"]
        state.status = "style_improved"
        return state
    
    async def _technical_step(self, state: BlogState) -> BlogState:
        """技術レビューステップ"""
        result = await self.tech_agent.process({"content": state.current_content})
        state.current_content = result["content"]
        state.status = "technically_reviewed"
        return state
    
    async def _revision_step(self, state: BlogState) -> BlogState:
        """リビジョンステップ"""
        result = await self.revision_agent.process({
            "content": state.current_content,
            "feedback": state.feedback
        })
        state.current_content = result["content"]
        state.revision_count += 1
        state.status = "revision_applied"
        return state
    
    def _needs_revision(self, state: BlogState) -> bool:
        """リビジョンが必要かどうかを判断"""
        return bool(state.feedback and not state.complete)
 