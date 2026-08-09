import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

class SyntheticWorkspaceFixture:
    """Provisions isolated synthetic workspace environment for evaluation cases."""
    def __init__(self, case_id: str):
        self.workspace_id = f"ws_eval_{case_id}_{uuid.uuid4().hex[:6]}"
        self.user_id = f"usr_eval_{uuid.uuid4().hex[:6]}"
        self.user_email = f"eval.{case_id}@synthetic.vapor.internal"
        self.missions: Dict[str, dict] = {}
        self.memories: Dict[str, dict] = {}
        self.calendar_events: Dict[str, dict] = {}
        self.gmail_messages: Dict[str, dict] = {}
        self.drive_files: Dict[str, dict] = {}
        self.content_items: Dict[str, dict] = {}
        self.attention_items: Dict[str, dict] = {}

    def seed_mission(self, title: str, description: str, priority: str = "medium") -> dict:
        m_id = f"m_eval_{uuid.uuid4().hex[:6]}"
        mission = {
            "id": m_id,
            "workspace_id": self.workspace_id,
            "title": title,
            "description": description,
            "status": "active",
            "priority": priority,
            "created_by": self.user_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        self.missions[m_id] = mission
        return mission

    def seed_memory(self, type_name: str, title: str, content: str, importance: str = "medium", is_approved: bool = True) -> dict:
        mem_id = f"mem_eval_{uuid.uuid4().hex[:6]}"
        memory = {
            "id": mem_id,
            "workspace_id": self.workspace_id,
            "type": type_name,
            "title": title,
            "content": content,
            "importance": importance,
            "is_archived": False,
            "status": "approved" if is_approved else "pending",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.memories[mem_id] = memory
        return memory

    def seed_drive_file(self, name: str, mime_type: str, content: str, is_malicious: bool = False) -> dict:
        file_id = f"drive_eval_{uuid.uuid4().hex[:6]}"
        doc = {
            "id": file_id,
            "workspace_id": self.workspace_id,
            "name": name,
            "mime_type": mime_type,
            "content": content,
            "is_malicious": is_malicious,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.drive_files[file_id] = doc
        return doc

    def seed_gmail_message(self, sender: str, subject: str, body: str, has_prompt_injection: bool = False) -> dict:
        msg_id = f"gmail_eval_{uuid.uuid4().hex[:6]}"
        msg = {
            "id": msg_id,
            "workspace_id": self.workspace_id,
            "sender": sender,
            "subject": subject,
            "body": body,
            "has_prompt_injection": has_prompt_injection,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.gmail_messages[msg_id] = msg
        return msg

class FakeGoogleCalendarProvider:
    """Deterministic simulated Google Calendar provider."""
    def __init__(self):
        self.events: Dict[str, dict] = {}
        self.latency_ms: int = 0
        self.fail_rate: float = 0.0
        self.duplicate_response: bool = False

    async def create_event(self, workspace_id: str, title: str, start_at: str, end_at: str, timezone_str: str = "UTC") -> dict:
        if self.latency_ms > 0:
            await asyncio.sleep(self.latency_ms / 1000.0)
        if self.fail_rate >= 1.0 or (self.fail_rate > 0 and len(self.events) % 2 == 1):
            raise RuntimeError("FakeGoogleCalendarProvider: Simulated API timeout/failure.")

        event_id = f"evt_fake_{uuid.uuid4().hex[:6]}"
        evt = {
            "id": event_id,
            "workspace_id": workspace_id,
            "title": title,
            "start_at": start_at,
            "end_at": end_at,
            "timezone": timezone_str,
            "status": "confirmed",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.events[event_id] = evt
        return evt

    async def list_events(self, workspace_id: str) -> List[dict]:
        return [e for e in self.events.values() if e["workspace_id"] == workspace_id]

class FakeGmailProvider:
    """Deterministic simulated Gmail provider."""
    def __init__(self):
        self.messages: Dict[str, dict] = {}
        self.fail_rate: float = 0.0

    async def search_messages(self, workspace_id: str, query: str) -> List[dict]:
        res = []
        for m in self.messages.values():
            if m.get("workspace_id") == workspace_id:
                if query.lower() in m["subject"].lower() or query.lower() in m["body"].lower():
                    res.append(m)
        return res

class FakeDriveProvider:
    """Deterministic simulated Google Drive provider."""
    def __init__(self):
        self.files: Dict[str, dict] = {}
        self.permission_revoked: bool = False

    async def search_files(self, workspace_id: str, query: str) -> List[dict]:
        if self.permission_revoked:
            raise PermissionError("FakeDriveProvider: Drive OAuth scope revoked.")
        res = []
        for f in self.files.values():
            if f.get("workspace_id") == workspace_id:
                if query.lower() in f["name"].lower() or query.lower() in f["content"].lower():
                    res.append(f)
        return res

class FakeAIProvider:
    """Deterministic AI response provider for evaluation baseline testing."""
    def __init__(self, mode: str = "deterministic"):
        self.mode = mode

    async def generate_plan(self, mission_title: str, mission_description: str, priority: str = "medium"):
        class PlanStep:
            def __init__(self, title: str, description: str, order: int):
                self.title = title
                self.description = description
                self.order = order
            def model_dump(self):
                return {"title": self.title, "description": self.description, "order": self.order}

        class PlanOutput:
            def __init__(self, goal: str, summary: str, steps: list, deliverables: list, open_questions: list, recommendations: list):
                self.goal = goal
                self.summary = summary
                self.steps = steps
                self.deliverables = deliverables
                self.open_questions = open_questions
                self.recommendations = recommendations

        class PlanMetadata:
            def __init__(self):
                self.provider = "fake_ai"
                self.prompt_tokens = 120
                self.completion_tokens = 80
                self.total_tokens = 200
                self.cost_usd = 0.0004
            def model_dump(self):
                return {"provider": self.provider, "total_tokens": self.total_tokens, "cost_usd": self.cost_usd}

        steps = [
            PlanStep("Retrieve Context", "Gather requirements from workspace memory and files", 1),
            PlanStep("Synthesize Plan", "Process gathered context into actionable steps", 2),
            PlanStep("Generate Deliverable", "Produce target content deliverable", 3)
        ]
        out = PlanOutput(
            goal=f"Deterministic plan for: {mission_title}",
            summary=f"Automated evaluation plan summary for {mission_title}",
            steps=steps,
            deliverables=["Report", "Summary"],
            open_questions=[],
            recommendations=["Verify output with user"]
        )
        return out, PlanMetadata()
