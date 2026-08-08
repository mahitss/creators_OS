from pydantic import BaseModel
from typing import List, Optional

class ActionLink(BaseModel):
    label: str
    href: str

class AttentionItem(BaseModel):
    id: str
    title: str
    context: str
    why_it_matters: str
    primary_action: ActionLink
    secondary_action: Optional[ActionLink] = None
    risk_level: str = "LOW"

class ActivityItem(BaseModel):
    id: str
    title: str
    category: str
    timestamp: str
    status: str

class QuickActionItem(BaseModel):
    id: str
    label: str
    href: str
    icon: str

class RecommendationItem(BaseModel):
    id: str
    title: str
    reason: str
    action_label: str
    action_href: str

class LearnedMemoryItem(BaseModel):
    id: str
    title: str
    content: str
    type: str
    updated_at: str

class ExecutiveBriefResponse(BaseModel):
    user_name: str
    greeting: str
    summary_statement: str
    needs_attention: List[AttentionItem] = []
    primary_recommendation: Optional[RecommendationItem] = None
    learned_memories: List[LearnedMemoryItem] = []
    recent_activity: List[ActivityItem] = []
    quick_actions: List[QuickActionItem] = []
    is_quiet_state: bool = False
    is_empty_state: bool = True
