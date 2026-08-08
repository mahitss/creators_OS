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

class ExecutiveBriefResponse(BaseModel):
    user_name: str
    greeting: str
    summary_statement: str
    needs_attention: List[AttentionItem] = []
    recent_activity: List[ActivityItem] = []
    quick_actions: List[QuickActionItem] = []
    is_empty_state: bool = True
