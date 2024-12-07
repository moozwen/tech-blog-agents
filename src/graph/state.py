from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class BlogState(BaseModel):
    """ブログ生成プロセスの状態を管理するクラス"""
    fragments: List[str] = Field(default_factory=list)
    draft: Optional[str] = None
    current_content: Optional[str] = None
    feedback: Optional[str] = None
    metadata: Dict = Field(default_factory=dict)
    status: str = "initialized"
    revision_count: int = 0
    complete: bool = False 