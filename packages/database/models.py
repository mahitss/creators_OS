import uuid
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, ForeignKey, JSON, Index, Integer, Boolean, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Workspace(Base):
    __tablename__ = "workspaces"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    root_path: Mapped[str] = mapped_column(Text, nullable=False)
    settings: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    token: Mapped[str] = mapped_column(String(512), unique=True, nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("idx_missions_workspace_status", "workspace_id", "status"),
        Index("idx_missions_workspace_created", "workspace_id", "created_at"),
    )

class MissionActivity(Base):
    __tablename__ = "mission_activities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("missions.id", ondelete="CASCADE"), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class MissionPlan(Base):
    __tablename__ = "mission_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("missions.id", ondelete="CASCADE"), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="validated", index=True)
    goal: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    steps: Mapped[list] = mapped_column(JSON, default=list)
    deliverables: Mapped[list] = mapped_column(JSON, default=list)
    open_questions: Mapped[list] = mapped_column(JSON, default=list)
    recommendations: Mapped[list] = mapped_column(JSON, default=list)
    usage_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    replan_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_mission_plans_version", "mission_id", "version"),
    )

class PlanNode(Base):
    __tablename__ = "plan_nodes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("mission_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    node_key: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    type: Mapped[str] = mapped_column(String(50), nullable=False, default="tool_call", index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, ready, running, waiting_for_approval, completed, failed, blocked, cancelled, skipped
    dependencies: Mapped[list] = mapped_column(JSON, default=list)
    tool_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    input_schema: Mapped[dict] = mapped_column(JSON, default=dict)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="read")
    approval_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    estimated_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_plan_nodes_key", "plan_id", "node_key", unique=True),
    )

class MissionStep(Base):
    __tablename__ = "mission_steps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("missions.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_version_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("mission_plans.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("idx_mission_steps_order", "mission_id", "order"),
    )

class MissionExecution(Base):
    __tablename__ = "mission_executions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("missions.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="idle", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class MissionStepResult(Base):
    __tablename__ = "mission_step_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    step_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("mission_steps.id", ondelete="CASCADE"), nullable=False, index=True)
    execution_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("mission_executions.id", ondelete="CASCADE"), nullable=False, index=True)
    output: Mapped[dict] = mapped_column(JSON, default=dict)
    step_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Memory(Base):
    __tablename__ = "memories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False, default="manual")
    source_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    importance: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    last_accessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_dict: Mapped[dict] = mapped_column(JSON, default=dict)

    __table_args__ = (
        Index("idx_memories_workspace_type", "workspace_id", "type"),
        Index("idx_memories_workspace_archived", "workspace_id", "is_archived"),
    )

class MemoryCandidate(Base):
    __tablename__ = "memory_candidates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False, default="ai_extraction")
    source_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, default="preference")
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Content(Base):
    __tablename__ = "content_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    mission_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("missions.id", ondelete="SET NULL"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False, default="article", index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    archived_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("idx_content_workspace_type", "workspace_id", "type"),
        Index("idx_content_workspace_status", "workspace_id", "status"),
    )

class DeliverableSuggestion(Base):
    __tablename__ = "deliverable_suggestions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    mission_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("missions.id", ondelete="CASCADE"), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, default="report", index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    source_data: Mapped[dict] = mapped_column(JSON, default=dict)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_deliv_sugg_mission_status", "mission_id", "status"),
        Index("idx_deliv_sugg_workspace_status", "workspace_id", "status"),
    )

class AttentionItem(Base):
    __tablename__ = "attention_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    source_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    snoozed_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_dict: Mapped[dict] = mapped_column(JSON, default=dict)

    __table_args__ = (
        Index("idx_attention_workspace_status", "workspace_id", "status"),
        Index("idx_attention_source", "source_type", "source_id"),
    )

class IntegrationConnection(Base):
    __tablename__ = "integration_connections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="disconnected", index=True)
    scopes: Mapped[list] = mapped_column(JSON, default=list)
    external_account_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    external_account_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    encrypted_access_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    encrypted_refresh_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    token_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    connected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_sync_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_dict: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_integration_workspace_provider", "workspace_id", "provider", unique=True),
        Index("idx_integration_workspace_status", "workspace_id", "status"),
    )

class IntegrationSyncJob(Base):
    __tablename__ = "integration_sync_jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    integration_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("integration_connections.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="queued", index=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    attempt: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Calendar(Base):
    __tablename__ = "calendars"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    integration_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("integration_connections.id", ondelete="CASCADE"), nullable=False, index=True)
    external_calendar_id: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    timezone: Mapped[str] = mapped_column(String(100), nullable=False, default="UTC")
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    sync_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_calendars_workspace_ext", "workspace_id", "external_calendar_id", unique=True),
    )

class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    integration_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("integration_connections.id", ondelete="CASCADE"), nullable=False, index=True)
    calendar_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("calendars.id", ondelete="CASCADE"), nullable=False, index=True)
    external_event_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    location: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    timezone: Mapped[str] = mapped_column(String(100), nullable=False, default="UTC")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="confirmed", index=True)
    organizer: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    attendee_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_all_day: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    external_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_events_workspace_start", "workspace_id", "start_at"),
        Index("idx_events_cal_ext", "calendar_id", "external_event_id", unique=True),
    )

class GmailThread(Base):
    __tablename__ = "gmail_threads"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    integration_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("integration_connections.id", ondelete="CASCADE"), nullable=False, index=True)
    external_thread_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    last_message_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    message_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    snippet: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_threads_workspace_ext", "workspace_id", "external_thread_id", unique=True),
    )

class GmailMessage(Base):
    __tablename__ = "gmail_messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    integration_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("integration_connections.id", ondelete="CASCADE"), nullable=False, index=True)
    thread_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gmail_threads.id", ondelete="CASCADE"), nullable=False, index=True)
    external_message_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    sender_name: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    sender_email: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    snippet: Mapped[str] = mapped_column(Text, nullable=False, default="")
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    is_unread: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    label_ids: Mapped[list] = mapped_column(JSON, default=list)
    full_body: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_classification: Mapped[str] = mapped_column(String(50), nullable=False, default="informational", index=True)
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    external_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_messages_workspace_received", "workspace_id", "received_at"),
        Index("idx_messages_thread_ext", "thread_id", "external_message_id", unique=True),
    )

class DriveFile(Base):
    __tablename__ = "drive_files"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    integration_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("integration_connections.id", ondelete="CASCADE"), nullable=False, index=True)
    external_file_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False, default="application/octet-stream", index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    web_url: Mapped[str] = mapped_column(Text, nullable=False, default="")
    owner_name: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    modified_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    trashed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    parent_external_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    external_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_drive_files_workspace_modified", "workspace_id", "modified_time"),
        Index("idx_drive_files_integ_ext", "integration_id", "external_file_id", unique=True),
    )

class MissionDocumentReference(Base):
    __tablename__ = "mission_document_references"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    mission_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("missions.id", ondelete="CASCADE"), nullable=False, index=True)
    drive_file_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("drive_files.id", ondelete="CASCADE"), nullable=False, index=True)
    added_by: Mapped[str] = mapped_column(String(255), nullable=False, default="usr_alex")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_mission_doc_ref_unique", "mission_id", "drive_file_id", unique=True),
    )

class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    mission_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("missions.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="queued", index=True)
    goal: Mapped[str] = mapped_column(Text, nullable=False)
    current_step_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    iteration_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_iterations: Mapped[int] = mapped_column(Integer, nullable=False, default=20)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    lease_worker_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    lease_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    budget_state: Mapped[dict] = mapped_column(JSON, default=dict)
    resume_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_agent_runs_workspace_status", "workspace_id", "status"),
    )

class AgentStep(Base):
    __tablename__ = "agent_steps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    type: Mapped[str] = mapped_column(String(50), nullable=False, default="reasoning", index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="completed", index=True)
    tool_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    input: Mapped[dict] = mapped_column(JSON, default=dict)
    result: Mapped[dict] = mapped_column(JSON, default=dict)
    error_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_agent_steps_run_seq", "agent_run_id", "sequence"),
    )

class AgentApprovalRequest(Base):
    __tablename__ = "agent_approval_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    tool_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="write", index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True)
    input_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class AgentCheckpoint(Base):
    __tablename__ = "agent_checkpoints"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    state: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_checkpoints_run_seq", "agent_run_id", "sequence"),
    )

class ToolExecution(Base):
    __tablename__ = "tool_executions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_step_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_steps.id", ondelete="CASCADE"), nullable=False, index=True)
    tool_name: Mapped[str] = mapped_column(String(100), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True)
    input_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    result_reference: Mapped[dict] = mapped_column(JSON, default=dict)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_tool_exec_run_step", "agent_run_id", "agent_step_id"),
    )

class EvaluationSuite(Base):
    __tablename__ = "evaluation_suites"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class EvaluationCase(Base):
    __tablename__ = "evaluation_cases"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    suite_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("evaluation_suites.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    input: Mapped[dict] = mapped_column(JSON, default=dict)
    expected: Mapped[dict] = mapped_column(JSON, default=dict)
    constraints: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_eval_cases_suite_cat", "suite_id", "category"),
    )

class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    suite_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("evaluation_suites.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="queued", index=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    total_cases: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    passed_cases: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    failed_cases: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_eval_runs_suite_status", "suite_id", "status"),
    )

class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("evaluation_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("evaluation_cases.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="passed", index=True)
    score: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    metrics: Mapped[dict] = mapped_column(JSON, default=dict)
    actual: Mapped[dict] = mapped_column(JSON, default=dict)
    expected: Mapped[dict] = mapped_column(JSON, default=dict)
    failure_category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    token_usage: Mapped[dict] = mapped_column(JSON, default=dict)
    estimated_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_eval_results_run_case", "run_id", "case_id"),
    )

class OperatorAuditLog(Base):
    __tablename__ = "operator_audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operator_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    target_agent_run_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    policy_result: Mapped[str] = mapped_column(String(50), nullable=False, default="allowed")
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    __table_args__ = (
        Index("idx_operator_audit_ts", "timestamp"),
    )

class AgentPolicyRule(Base):
    __tablename__ = "agent_policy_rules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    rule_type: Mapped[str] = mapped_column(String(100), nullable=False, default="tool_restriction")
    action: Mapped[str] = mapped_column(String(50), nullable=False, default="ALLOW") # ALLOW, DENY, APPROVAL_REQUIRED
    conditions: Mapped[dict] = mapped_column(JSON, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    priority: Mapped[int] = mapped_column(Integer, default=10, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class WorkspaceMember(Base):
    __tablename__ = "workspace_members"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="member") # owner, admin, member, viewer
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # invited, active, suspended, removed
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("uq_ws_member", "workspace_id", "user_id", unique=True),
    )

class WorkspaceInvitation(Base):
    __tablename__ = "workspace_invitations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="member")
    invited_by: Mapped[str] = mapped_column(String(255), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, accepted, expired, revoked
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class MissionMember(Base):
    __tablename__ = "mission_members"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="contributor") # owner, editor, contributor, viewer
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("uq_mission_member", "mission_id", "user_id", unique=True),
    )

class AgentDefinition(Base):
    __tablename__ = "agent_definitions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_by: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    visibility: Mapped[str] = mapped_column(String(50), nullable=False, default="workspace", index=True) # private, workspace, mission
    default_purpose: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class AgentDelegation(Base):
    __tablename__ = "agent_delegations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    delegated_by: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    agent_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    mission_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    scope: Mapped[str] = mapped_column(String(50), nullable=False, default="mission", index=True) # mission, workspace, resource, tool
    permissions: Mapped[dict] = mapped_column(JSON, default=dict)
    allowed_tools: Mapped[dict] = mapped_column(JSON, default=dict)
    allowed_resources: Mapped[dict] = mapped_column(JSON, default=dict)
    autonomy_level: Mapped[str] = mapped_column(String(50), nullable=False, default="FULL_AUTONOMY")
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, paused, expired, revoked, completed
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class AgentHandoff(Base):
    __tablename__ = "agent_handoffs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_agent_run_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_agent_definition_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    scope: Mapped[str] = mapped_column(String(50), nullable=False, default="mission")
    input_reference: Mapped[dict] = mapped_column(JSON, default=dict)
    depth: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, running, completed, failed
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class KnowledgeObject(Base):
    __tablename__ = "knowledge_objects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    scope: Mapped[str] = mapped_column(String(50), nullable=False, default="workspace", index=True) # personal, workspace, mission, agent, temporary
    owner_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    mission_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    source_type: Mapped[str] = mapped_column(String(100), nullable=False, default="project_context", index=True) # fact, preference, decision, requirement, project_context, reference, summary, instruction
    source_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content_reference: Mapped[dict] = mapped_column(JSON, default=dict)
    content_hash: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="fresh", index=True) # fresh, aging, stale, expired
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    freshness: Mapped[str] = mapped_column(String(50), nullable=False, default="fresh")
    visibility: Mapped[str] = mapped_column(String(50), nullable=False, default="workspace")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class MemoryConflict(Base):
    __tablename__ = "memory_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    memory_a_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    memory_b_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, resolved, dismissed, superseded
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class KnowledgeRelation(Base):
    __tablename__ = "knowledge_relations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_knowledge_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    relation_type: Mapped[str] = mapped_column(String(50), nullable=False, default="supports", index=True) # supports, contradicts, derived_from, belongs_to, references, supersedes
    to_knowledge_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SystemEvent(Base):
    __tablename__ = "system_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # gmail, calendar, drive, mission, agent, approval, workspace, policy, integration, system
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    resource_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    actor_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    dedupe_key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    metadata_dict: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    sensitivity: Mapped[str] = mapped_column(String(50), nullable=False, default="internal")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="received", index=True) # received, processing, processed, ignored, failed, dead_lettered
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AgentTrigger(Base):
    __tablename__ = "agent_triggers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    conditions: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    action_type: Mapped[str] = mapped_column(String(100), nullable=False, default="create_attention")
    agent_definition_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    mission_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, paused, disabled, deleted
    scope: Mapped[str] = mapped_column(String(50), nullable=False, default="workspace", index=True) # personal, workspace, mission
    cooldown_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=7200) # 2 hours default
    last_triggered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Signal(Base):
    __tablename__ = "signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # deadline_change, important_message, document_change, mission_risk, approval_risk, agent_failure, schedule_conflict, project_update
    importance: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True) # low, medium, high, critical
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    reason_code: Mapped[str] = mapped_column(String(100), nullable=False)
    details: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Insight(Base):
    __tablename__ = "insights"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    scope: Mapped[str] = mapped_column(String(50), nullable=False, default="workspace", index=True)
    source_events: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    importance: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    source_references: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="new", index=True) # new, seen, dismissed, acted_on, expired
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class AutomationExecution(Base):
    __tablename__ = "automation_executions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trigger_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    event_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    decision: Mapped[str] = mapped_column(String(50), nullable=False, default="allowed", index=True) # allowed, approval_required, denied, ignored
    action_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="completed", index=True) # completed, failed, retrying, loop_blocked, cooldown_blocked
    agent_run_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    insight_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    chain_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    chain_depth: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class DeadLetterEvent(Base):
    __tablename__ = "dead_letter_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    error_message: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class EventDeduplication(Base):
    __tablename__ = "event_deduplication"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dedupe_key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    event_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    processed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", index=True) # draft, active, paused, archived, deleted
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    visibility: Mapped[str] = mapped_column(String(50), nullable=False, default="workspace", index=True) # private, workspace, mission
    trigger_config: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class WorkflowVersion(Base):
    __tablename__ = "workflow_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    definition: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    compiled_graph: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    capabilities: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", index=True) # draft, published, archived
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workflow_version_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger_event_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="queued", index=True) # queued, running, waiting, paused, completed, failed, cancelled, expired
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    current_node: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class WorkflowNodeRun(Base):
    __tablename__ = "workflow_node_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_run_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    node_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    node_key: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    node_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, running, waiting_approval, completed, failed, skipped
    attempt: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    result_reference: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    error_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class WorkflowAIRequest(Base):
    __tablename__ = "workflow_ai_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workflow_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    request_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # create, modify, explain, debug, optimize, simulate, validate, summarize
    request_text: Mapped[str] = mapped_column(Text, nullable=False)
    context: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="completed", index=True) # pending, completed, failed
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class WorkflowProposal(Base):
    __tablename__ = "workflow_proposals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    request_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    base_version_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    proposed_definition: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    change_summary: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    risk_summary: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    capability_summary: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    validation_result: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", index=True) # draft, validated, needs_review, approved, rejected, applied, expired
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class WorkflowTestCase(Base):
    __tablename__ = "workflow_test_cases"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_version_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    input: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    expected_path: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    expected_outcome: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class WorkflowTestRun(Base):
    __tablename__ = "workflow_test_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_version_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    test_case_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # passed, failed, skipped
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    node_path: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class WorkflowOptimizationProposal(Base):
    __tablename__ = "workflow_optimization_proposals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    current_graph: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    proposed_graph: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    estimated_improvement: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    capability_changes: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class UsageRecord(Base):
    __tablename__ = "usage_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    span_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    parent_span_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    user_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    mission_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    agent_run_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    workflow_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    workflow_run_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    node_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    provider: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False, default="model") # model, tool, embedding, retrieval
    input_units: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    output_units: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cached_units: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    reasoning_units: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    pricing_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="success", index=True)
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class PricingVersion(Base):
    __tablename__ = "pricing_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    input_price_per_1k: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    output_price_per_1k: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    cached_input_price_per_1k: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    reasoning_price_per_1k: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1, index=True)

class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    scope_type: Mapped[str] = mapped_column(String(50), nullable=False, default="workspace", index=True) # workspace, user, mission, workflow, agent
    scope_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    period: Mapped[str] = mapped_column(String(50), nullable=False, default="monthly") # daily, monthly, total
    limit_amount: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    used_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    reserved_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    warning_threshold_pct: Mapped[float] = mapped_column(Float, nullable=False, default=90.0)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, warning, exhausted
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class BudgetReservation(Base):
    __tablename__ = "budget_reservations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    budget_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    amount_reserved: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="reserved", index=True) # reserved, released, consumed
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class UsageAnomaly(Base):
    __tablename__ = "usage_anomalies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # cost_spike, latency_spike, failure_spike, token_spike, retry_spike
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(255), nullable=False)
    observed_value: Mapped[float] = mapped_column(Float, nullable=False)
    baseline_value: Mapped[float] = mapped_column(Float, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.9)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, acknowledged, muted, resolved
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class OperationalIncident(Base):
    __tablename__ = "operational_incidents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    service: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True) # low, medium, high, critical
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="detected", index=True) # detected, investigating, mitigated, resolved, acknowledged
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    source_references: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class HealthSignal(Base):
    __tablename__ = "health_signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    service: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="warning", index=True) # info, warning, high, critical
    signal_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # latency_degradation, error_rate_increase, queue_backlog, worker_failure, provider_failure, workflow_failure, agent_failure, integration_failure, budget_exhaustion
    observed_value: Mapped[float] = mapped_column(Float, nullable=False)
    baseline_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="telemetry")
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class IncidentDiagnosis(Base):
    __tablename__ = "incident_diagnoses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    observed: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    correlated: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    suspected: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class RecoveryPlan(Base):
    __tablename__ = "recovery_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    steps: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low") # low, medium, high
    estimated_impact: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    policy_requirements: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="proposed", index=True) # proposed, approved, executing, completed, failed, rejected
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class RecoveryExecution(Base):
    __tablename__ = "recovery_executions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recovery_plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    incident_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    recovery_key: Mapped[str] = mapped_column(String(255), nullable=False, index=True) # Idempotency Key
    step_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    action_type: Mapped[str] = mapped_column(String(100), nullable=False) # retry_transient_job, restart_worker, pause_workflow, resume_workflow, requeue_dead_letter, switch_configured_fallback_model, clear_stale_lease
    target: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="executing", index=True) # executing, verified, failed, rolled_back
    verification_result: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class Runbook(Base):
    __tablename__ = "runbooks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    trigger_condition: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    steps: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    verification: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    rollback: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    owner: Mapped[str] = mapped_column(String(255), nullable=False, default="sre")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class RunbookVersion(Base):
    __tablename__ = "runbook_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    runbook_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    definition: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Problem(Base):
    __tablename__ = "problems"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    service: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    signature: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    frequency: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    incidents: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, investigating, mitigated, resolved, accepted
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class CircuitBreakerState(Base):
    __tablename__ = "circuit_breaker_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="closed", index=True) # closed, open, half_open
    failure_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_failure_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cooldown_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=60)
    opened_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    half_opened_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class OrganizationMembership(Base):
    __tablename__ = "organization_memberships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="member", index=True) # owner, admin, security_admin, billing_admin, member, viewer
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, suspended, invited
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    actor_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    actor_type: Mapped[str] = mapped_column(String(50), nullable=False, default="user") # user, agent, system
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(255), nullable=False)
    result: Mapped[str] = mapped_column(String(50), nullable=False, default="SUCCESS") # SUCCESS, DENIED, FAILED
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    ip_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    user_agent_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    metadata_info: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class RetentionPolicy(Base):
    __tablename__ = "retention_policies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # audit, workflow_runs, agent_runs, usage_records, events, insights, logs, traces
    retention_days: Mapped[int] = mapped_column(Integer, nullable=False, default=90)
    legal_hold: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class LegalHold(Base):
    __tablename__ = "legal_holds"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AccessReview(Base):
    __tablename__ = "access_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="all_members")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, in_review, completed, expired
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class AccessReviewItem(Base):
    __tablename__ = "access_review_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    resource: Mapped[str] = mapped_column(String(255), nullable=False)
    principal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    permission: Mapped[str] = mapped_column(String(100), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    decision: Mapped[str] = mapped_column(String(50), nullable=False, default="retain") # retain, remove, modify, unknown
    reviewer_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ComplianceControl(Base):
    __tablename__ = "compliance_controls"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    framework: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # SOC_2, ISO_27001, GDPR
    control_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="supported", index=True) # not_assessed, in_progress, partially_supported, supported, not_applicable
    owner: Mapped[str] = mapped_column(String(255), nullable=False, default="secops")
    last_reviewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ComplianceEvidence(Base):
    __tablename__ = "compliance_evidence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    control_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    evidence_type: Mapped[str] = mapped_column(String(100), nullable=False) # audit_event, configuration, access_review, policy, security_test, retention_policy
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    source_reference: Mapped[str] = mapped_column(String(255), nullable=False)
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="valid", index=True)

class SecurityFinding(Base):
    __tablename__ = "security_findings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True) # low, medium, high, critical
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # excessive_permission, stale_access, missing_approval, unsafe_workflow, unrestricted_agent, sensitive_data_exposure, integration_risk, policy_conflict
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="governance_scanner")
    resource: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, acknowledged, remediating, resolved, accepted_risk
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class PolicySimulation(Base):
    __tablename__ = "policy_simulations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    policy_definition: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    affected_workflows: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    affected_agents: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    simulated_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class IdentityProvider(Base):
    __tablename__ = "identity_providers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # oidc, saml, google, local, azure_ad, okta, auth0
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", index=True) # draft, active, disabled, error, deleted
    configuration: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict) # Secure reference / configuration settings
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class VerifiedDomain(Base):
    __tablename__ = "verified_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    domain: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, verified, failed
    verification_token: Mapped[str] = mapped_column(String(255), nullable=False)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ExternalIdentity(Base):
    __tablename__ = "external_identities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    provider_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    external_subject: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    attributes: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_external_identities_sub", "provider_id", "external_subject", unique=True),
    )

class IdentityGroup(Base):
    __tablename__ = "identity_groups"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    external_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class GroupMapping(Base):
    __tablename__ = "group_mappings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    external_group: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="member") # member, viewer, security_admin, admin
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="organization")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ServiceAccount(Base):
    __tablename__ = "service_accounts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, disabled, review_required
    owner_id: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class ServiceAccountToken(Base):
    __tablename__ = "service_account_tokens"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_account_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    scopes: Mapped[dict] = mapped_column(JSON, nullable=False, default=list) # e.g. ["organization.read", "workflow.run"]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class SCIMEvent(Base):
    __tablename__ = "scim_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    provider_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # create_user, update_user, disable_user, delete_user, manage_group
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="SUCCESS")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class AuthenticationEvent(Base):
    __tablename__ = "authentication_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    auth_method: Mapped[str] = mapped_column(String(50), nullable=False) # oidc, saml, google, password, service_account
    provider_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="SUCCESS")
    ip_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    user_agent_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class IdentitySecuritySignal(Base):
    __tablename__ = "identity_security_signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    user_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    signal_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # impossible_travel, brute_force, unmapped_claim, orphaned_service_account
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    details: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class DataAsset(Base):
    __tablename__ = "data_assets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # gmail, drive, calendar, workflow, agent, memory, document, user_input, tool_output, generated_output
    source_id: Mapped[str] = mapped_column(String(255), nullable=False)
    classification: Mapped[str] = mapped_column(String(50), nullable=False, default="internal", index=True) # public, internal, confidential, restricted, secret
    owner_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class DataClassificationRecord(Base):
    __tablename__ = "data_classification_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    classification: Mapped[str] = mapped_column(String(50), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="deterministic") # user_label, source_metadata, deterministic, ai_suggestion, policy_rule
    model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SensitiveDataFinding(Base):
    __tablename__ = "sensitive_data_findings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    detector: Mapped[str] = mapped_column(String(100), nullable=False) # email, phone, credit_card, api_key, jwt_token, private_key, password
    classification: Mapped[str] = mapped_column(String(50), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False, default="redact") # allow, redact, block, quarantine
    resource: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, acknowledged, resolved
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class DLPPolicy(Base):
    __tablename__ = "dlp_policies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    classification: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    source_scope: Mapped[str] = mapped_column(String(100), nullable=False, default="all")
    destination_scope: Mapped[str] = mapped_column(String(100), nullable=False, default="external")
    allowed_action: Mapped[str] = mapped_column(String(50), nullable=False, default="redact") # allow, redact, block, require_approval, quarantine
    approval_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DLPDecision(Base):
    __tablename__ = "dlp_decisions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # allow, redact, block, require_approval, quarantine
    reason_code: Mapped[str] = mapped_column(String(100), nullable=False)
    classification: Mapped[str] = mapped_column(String(50), nullable=False)
    detectors: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    policy_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    redactions_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class DataAccessEvent(Base):
    __tablename__ = "data_access_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    resource: Mapped[str] = mapped_column(String(255), nullable=False)
    classification: Mapped[str] = mapped_column(String(50), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    destination: Mapped[str | None] = mapped_column(String(255), nullable=True)
    result: Mapped[str] = mapped_column(String(50), nullable=False, default="SUCCESS")
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class DataLineageNode(Base):
    __tablename__ = "data_lineage_nodes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False) # source, agent, model, output, destination
    classification: Mapped[str] = mapped_column(String(50), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DataLineageEdge(Base):
    __tablename__ = "data_lineage_edges"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    destination_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    transformation: Mapped[str] = mapped_column(String(100), nullable=False)
    policy_decision_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class QuarantineRecord(Base):
    __tablename__ = "quarantine_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(255), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    quarantined_by: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="quarantined", index=True) # quarantined, released, rejected
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ModelDataPolicy(Base):
    __tablename__ = "model_data_policies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # openai, anthropic, google, local
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    classification: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    allowed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    requires_approval: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class DataProcessingRecord(Base):
    __tablename__ = "data_processing_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    classification: Mapped[str] = mapped_column(String(50), nullable=False)
    decision: Mapped[str] = mapped_column(String(50), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class KnowledgeSource(Base):
    __tablename__ = "knowledge_sources"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # drive, gmail, calendar, document, memory, workflow, agent, mission, manual
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="connected", index=True) # connected, syncing, healthy, degraded, paused, error, disconnected
    configuration: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class KnowledgeCollection(Base):
    __tablename__ = "knowledge_collections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    owner_id: Mapped[str] = mapped_column(String(255), nullable=False)
    classification: Mapped[str] = mapped_column(String(50), nullable=False, default="internal", index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    external_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False, default="text/plain")
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    classification: Mapped[str] = mapped_column(String(50), nullable=False, default="internal", index=True)
    owner_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    content_hash: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    indexed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="indexed", index=True) # pending, processing, indexed, updated, failed, deleted, quarantined
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class KnowledgeDocumentVersion(Base):
    __tablename__ = "knowledge_document_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    source_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    indexed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    parser_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")
    chunking_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")
    embedding_version: Mapped[str] = mapped_column(String(50), nullable=False, default="text-embedding-3-small")

class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    section: Mapped[str | None] = mapped_column(String(255), nullable=True)
    text_content: Mapped[str] = mapped_column(Text, nullable=False)
    token_estimate: Mapped[int] = mapped_column(Integer, nullable=False, default=128)
    classification: Mapped[str] = mapped_column(String(50), nullable=False, default="internal", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class KnowledgeEntity(Base):
    __tablename__ = "knowledge_entities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # person, team, project, document, mission, workflow, agent, company, product
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    canonical_key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class KnowledgeRelationship(Base):
    __tablename__ = "knowledge_relationships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_entity_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    relationship: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # owns, created_by, belongs_to, mentions, related_to, depends_on, member_of, assigned_to, part_of
    target_entity_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_reference: Mapped[str] = mapped_column(String(255), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class KnowledgeQuery(Base):
    __tablename__ = "knowledge_queries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_text: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    agent_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    workflow_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    classification_ceiling: Mapped[str] = mapped_column(String(50), nullable=False, default="restricted")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class KnowledgeRetrieval(Base):
    __tablename__ = "knowledge_retrievals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    candidates_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    authorized_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    filtered_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rerank_latency_ms: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    context_size_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class KnowledgeSyncJob(Base):
    __tablename__ = "knowledge_sync_jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="running", index=True)
    items_processed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    items_failed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class KnowledgeSyncCheckpoint(Base):
    __tablename__ = "knowledge_sync_checkpoints"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    cursor: Mapped[str] = mapped_column(String(512), nullable=False)
    last_sync: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_successful_sync: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class KnowledgeEvaluationCase(Base):
    __tablename__ = "knowledge_evaluation_cases"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    expected_sources: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    expected_facts: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    permissions: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    classification: Mapped[str] = mapped_column(String(50), nullable=False, default="internal")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class KnowledgeEvaluationRun(Base):
    __tablename__ = "knowledge_evaluation_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    precision: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    recall: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    citation_correctness: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    grounding_score: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="passed", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AgentCapability(Base):
    __tablename__ = "agent_capabilities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # research, analysis, retrieval, coding, planning, writing, data_processing, validation, communication, scheduling
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    input_schema: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    output_schema: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="low", index=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AgentRegistry(Base):
    __tablename__ = "agent_registry"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    agent_name: Mapped[str] = mapped_column(String(255), nullable=False)
    specialization: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # Researcher, Data Analyst, Engineering Agent, Finance Analyst, Writer, Reviewer, Planner, Security Analyst
    capabilities: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="available", index=True) # available, busy, paused, disabled, degraded
    availability: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    max_delegation_depth: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    max_concurrent_tasks: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    budget_limit: Mapped[float] = mapped_column(Float, nullable=False, default=10.0)
    data_classification_ceiling: Mapped[str] = mapped_column(String(50), nullable=False, default="restricted")
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class DelegationRequest(Base):
    __tablename__ = "delegation_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_agent_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    child_agent_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    task_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    scope: Mapped[str] = mapped_column(String(255), nullable=False, default="read_only")
    input_references: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    required_output: Mapped[str] = mapped_column(Text, nullable=False, default="")
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="requested", index=True) # requested, approved, queued, running, completed, failed, cancelled, rejected, timed_out
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DelegationContextToken(Base):
    __tablename__ = "delegation_context_tokens"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    delegation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    parent_agent_id: Mapped[str] = mapped_column(String(255), nullable=False)
    child_agent_id: Mapped[str] = mapped_column(String(255), nullable=False)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False)
    task_id: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(255), nullable=False)
    expiration: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    capabilities: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    policy_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AgentGraphNode(Base):
    __tablename__ = "agent_graph_nodes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    task_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    agent_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    node_type: Mapped[str] = mapped_column(String(50), nullable=False, default="parallel", index=True) # sequential, parallel, conditional, review, fallback, synthesis
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="queued", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AgentTaskEdge(Base):
    __tablename__ = "agent_task_edges"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_node_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_node_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dependency_type: Mapped[str] = mapped_column(String(50), nullable=False, default="success_required")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AgentArtifact(Base):
    __tablename__ = "agent_artifacts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    task_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    agent_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # research_report, dataset, analysis, code_patch, document, recommendation, validation_report, decision
    schema_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")
    reference_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    classification: Mapped[str] = mapped_column(String(50), nullable=False, default="internal")
    validation_status: Mapped[str] = mapped_column(String(50), nullable=False, default="valid", index=True) # valid, invalid, needs_revision
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AgentMessage(Base):
    __tablename__ = "agent_messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_agent_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    receiver_agent_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    task_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, default="structured_handoff")
    payload_reference: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class AgentDisagreement(Base):
    __tablename__ = "agent_disagreements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    task_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    agents: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    positions: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    evidence: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    resolution: Mapped[str] = mapped_column(String(50), nullable=False, default="unresolved", index=True) # verified, needs_human, insufficient_evidence, policy_blocked
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AgentReviewTask(Base):
    __tablename__ = "agent_review_tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    task_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    artifact_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, approved, rejected, revision_requested, cancelled
    assigned_to: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class MissionSharedState(Base):
    __tablename__ = "mission_shared_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    task_outputs: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    artifacts: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    decisions: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class DecisionSignal(Base):
    __tablename__ = "decision_signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # workflow_volume, workflow_failure_rate, agent_success_rate, agent_latency, model_latency, model_cost, provider_error_rate, queue_depth, incident_frequency, recovery_frequency, knowledge_freshness, retrieval_quality, security_findings, budget_usage, user_activity
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    window: Mapped[str] = mapped_column(String(50), nullable=False, default="1h")
    quality: Mapped[str] = mapped_column(String(50), nullable=False, default="fresh") # fresh, delayed, partial, stale, invalid
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SignalBaseline(Base):
    __tablename__ = "signal_baselines"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    scope: Mapped[str] = mapped_column(String(255), nullable=False, default="global")
    window: Mapped[str] = mapped_column(String(50), nullable=False, default="7d")
    baseline_value: Mapped[float] = mapped_column(Float, nullable=False)
    method: Mapped[str] = mapped_column(String(50), nullable=False, default="moving_average") # moving_average, moving_median, rolling_percentile, seasonal_baseline
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AnomalyEvent(Base):
    __tablename__ = "anomaly_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    baseline_value: Mapped[float] = mapped_column(Float, nullable=False)
    actual_value: Mapped[float] = mapped_column(Float, nullable=False)
    deviation: Mapped[float] = mapped_column(Float, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="info", index=True) # info, warning, high, critical
    detector: Mapped[str] = mapped_column(String(100), nullable=False, default="std_dev_threshold")
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class Forecast(Base):
    __tablename__ = "forecasts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="7d")
    predicted_value: Mapped[float] = mapped_column(Float, nullable=False)
    predicted_range: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    method: Mapped[str] = mapped_column(String(50), nullable=False, default="moving_average") # moving_average, exponential_smoothing, trend_extrapolation, seasonal_baseline
    uncertainty: Mapped[float] = mapped_column(Float, nullable=False, default=0.1)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

class ForecastEvaluation(Base):
    __tablename__ = "forecast_evaluations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forecast_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    signal_type: Mapped[str] = mapped_column(String(100), nullable=False)
    predicted: Mapped[float] = mapped_column(Float, nullable=False)
    actual: Mapped[float] = mapped_column(Float, nullable=False)
    error: Mapped[float] = mapped_column(Float, nullable=False)
    mape: Mapped[float | None] = mapped_column(Float, nullable=True)
    mae: Mapped[float] = mapped_column(Float, nullable=False)
    rmse: Mapped[float] = mapped_column(Float, nullable=False)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # capacity_adjustment, provider_routing, workflow_optimization, cost_optimization, reliability_improvement, knowledge_refresh, agent_routing, human_review
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    evidence: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    expected_impact: Mapped[str] = mapped_column(Text, nullable=False)
    risk: Mapped[str] = mapped_column(String(50), nullable=False, default="medium") # low, medium, high, critical
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="new", index=True) # new, reviewing, accepted, rejected, executing, completed, expired
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class DecisionRecord(Base):
    __tablename__ = "decision_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger: Mapped[str] = mapped_column(String(255), nullable=False)
    evidence: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    recommendation_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    decision: Mapped[str] = mapped_column(String(255), nullable=False)
    actor: Mapped[str] = mapped_column(String(255), nullable=False)
    policy_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DecisionScenario(Base):
    __tablename__ = "decision_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    assumptions: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    inputs: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    outputs: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ScenarioResult(Base):
    __tablename__ = "scenario_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    baseline: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    scenario_output: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    delta: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    assumptions: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    uncertainty: Mapped[float] = mapped_column(Float, nullable=False, default=0.1)
    run_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DecisionOutcome(Base):
    __tablename__ = "decision_outcomes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expected_impact: Mapped[str] = mapped_column(Text, nullable=False)
    actual_impact: Mapped[str] = mapped_column(Text, nullable=False)
    error: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    unintended_effects: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DecisionFeedback(Base):
    __tablename__ = "decision_feedbacks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recommendation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    feedback: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # useful, not_useful, incorrect, unsafe, missing_context
    actor: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SignalCorrelation(Base):
    __tablename__ = "signal_correlations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signals: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    time_window: Mapped[str] = mapped_column(String(50), nullable=False, default="24h")
    relationship: Mapped[str] = mapped_column(String(100), nullable=False, default="correlated_with")
    strength: Mapped[float] = mapped_column(Float, nullable=False, default=0.8)
    evidence: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class WorkflowPerformanceProfile(Base):
    __tablename__ = "workflow_performance_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    execution_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    success_rate: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    failure_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    average_latency: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    p50_latency: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    p95_latency: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    p99_latency: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    average_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    retry_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    timeout_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    approval_wait_time: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class WorkflowNodePerformance(Base):
    __tablename__ = "workflow_node_performances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    node_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    execution_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    success_rate: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    latency: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    retry_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    failure_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class WorkflowBottleneck(Base):
    __tablename__ = "workflow_bottlenecks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    bottleneck_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # latency, cost, failure, retry, queue, provider, approval, sequential_dependency, data_transfer
    node_id: Mapped[str] = mapped_column(String(255), nullable=False)
    evidence: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="warning")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AdaptiveOptimizationProposal(Base):
    __tablename__ = "adaptive_optimization_proposals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_version: Mapped[int] = mapped_column(Integer, nullable=False)
    changes: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    evidence: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    expected_impact: Mapped[str] = mapped_column(Text, nullable=False)
    risk: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", index=True) # draft, simulating, needs_review, approved, rejected, published, rolled_back, expired
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class WorkflowOptimizationChange(Base):
    __tablename__ = "workflow_optimization_changes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proposal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    node_id: Mapped[str] = mapped_column(String(255), nullable=False)
    change_type: Mapped[str] = mapped_column(String(50), nullable=False) # parallelize, retry_adjustment, timeout_adjustment, provider_change, model_change, cache, batch, deduplicate, remove_redundant_step, reorder_safe_nodes
    before: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    after: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    reversible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class OptimizationSimulation(Base):
    __tablename__ = "optimization_simulations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proposal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    simulated_latency_diff: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    simulated_cost_diff: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    safety_validation: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    simulated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class OptimizationExperiment(Base):
    __tablename__ = "optimization_experiments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    baseline_version: Mapped[int] = mapped_column(Integer, nullable=False)
    candidate_version: Mapped[int] = mapped_column(Integer, nullable=False)
    traffic_split: Mapped[float] = mapped_column(Float, nullable=False, default=0.10) # 0.10 = 10% candidate, 90% baseline
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="running", index=True) # running, completed, stopped, rolled_back
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    stopped_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class OptimizationOutcome(Base):
    __tablename__ = "optimization_outcomes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proposal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    baseline_metrics: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    optimized_metrics: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    delta: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class WorkflowVersionComparison(Base):
    __tablename__ = "workflow_version_comparisons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version_a: Mapped[int] = mapped_column(Integer, nullable=False)
    version_b: Mapped[int] = mapped_column(Integer, nullable=False)
    diff_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    compared_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Integration(Base):
    __tablename__ = "integrations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # google, github, gmail, calendar, drive, slack, notion
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # communication, productivity, storage, calendar, crm, project_management, analytics, developer_tools, finance, custom
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="available", index=True) # available, connected, degraded, disabled, error
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class FabricConnection(Base):
    __tablename__ = "fabric_connections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    integration_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    owner_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    auth_type: Mapped[str] = mapped_column(String(50), nullable=False, default="oauth2") # oauth2, api_key, service_account, basic_auth
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="connected", index=True) # connected, reauthentication_required, expired, disabled, error
    scopes: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    metadata_info: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class IntegrationCapability(Base):
    __tablename__ = "integration_capabilities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    integration_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    input_schema: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    output_schema: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="medium") # low, medium, high, critical
    required_scopes: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class IntegrationAction(Base):
    __tablename__ = "integration_actions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    connection_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    actor: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    input_data: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, validating, authorizing, dlp_evaluating, approval_required, approved, executing, verifying, completed, failed, simulated, blocked
    result_reference: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    idempotency_key: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class ActionResultModel(Base):
    __tablename__ = "action_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # accepted, pending_verification, verified, failed
    provider_status: Mapped[int] = mapped_column(Integer, nullable=False, default=200)
    resource_reference: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    safe_metadata: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    error_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class IntegrationSubscription(Base):
    __tablename__ = "integration_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    integration_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target: Mapped[str] = mapped_column(String(255), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class IntegrationProviderManifest(Base):
    __tablename__ = "integration_provider_manifests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0.0")
    capabilities: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    auth_config: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    rate_limits: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class IntegrationHealth(Base):
    __tablename__ = "integration_healths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    connection_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="healthy", index=True) # healthy, degraded, rate_limited, provider_error, invalid_configuration
    latency_ms: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    error_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    circuit_breaker_state: Mapped[str] = mapped_column(String(50), nullable=False, default="closed") # closed, open, half_open
    last_successful_call: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)

class IntegrationUsage(Base):
    __tablename__ = "integration_usages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    integration_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    connection_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    action_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    estimated_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class EventEnvelope(Base):
    __tablename__ = "event_envelopes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    event_version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0.0")
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    correlation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    causation_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    producer: Mapped[str] = mapped_column(String(100), nullable=False)
    payload_reference: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    schema_version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0.0")
    classification: Mapped[str] = mapped_column(String(50), nullable=False, default="internal", index=True)
    metadata_info: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class EventSchema(Base):
    __tablename__ = "event_schemas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0.0")
    schema_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    producer: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class EventSubscription(Base):
    __tablename__ = "event_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    consumer: Mapped[str] = mapped_column(String(100), nullable=False)
    filter_config: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class EventDelivery(Base):
    __tablename__ = "event_deliveries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    subscription_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="queued", index=True) # queued, delivered, processing, completed, failed, dead_lettered
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    next_retry_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class EventConsumerState(Base):
    __tablename__ = "event_consumer_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    consumer_group: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    last_processed_offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    consumer_lag: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class EventDeadLetter(Base):
    __tablename__ = "event_dead_letters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    producer: Mapped[str] = mapped_column(String(100), nullable=False)
    error: Mapped[str] = mapped_column(Text, nullable=False)
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    payload_ref: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class EventReplay(Base):
    __tablename__ = "event_replays"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    authorized_by: Mapped[str] = mapped_column(String(255), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="replayed", index=True)
    replayed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class EventOutbox(Base):
    __tablename__ = "event_outboxes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    payload_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, published, failed
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class EventHealth(Base):
    __tablename__ = "event_healths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    throughput_eps: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    latency_p95: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    error_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    consumer_lag: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    dead_letter_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class EventCatalogEntry(Base):
    __tablename__ = "event_catalog_entries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0.0")
    producer: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    classification: Mapped[str] = mapped_column(String(50), nullable=False, default="internal")
    retention_days: Mapped[int] = mapped_column(Integer, nullable=False, default=30)

class OperationalHealth(Base):
    __tablename__ = "operational_healths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scope: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # system, service, agent, workflow, integration, security, cost, event
    scope_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="healthy", index=True) # healthy, degraded, warning, critical
    signals: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ControlAction(Base):
    __tablename__ = "control_actions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # pause_service, resume_service, disable_agent, cancel_workflow, replay_event, disable_integration, revoke_session, retry_ingestion
    target_resource: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    requested_by: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True) # low, medium, high, critical
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="requested", index=True) # requested, pending_approval, approved, executing, completed, failed, cancelled, rejected, verification_failed
    idempotency_key: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True, index=True)
    metadata_info: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class ControlActionApproval(Base):
    __tablename__ = "control_action_approvals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    approver_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    decision: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # approved, rejected
    comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ControlPlaneSnapshot(Base):
    __tablename__ = "control_plane_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    metrics: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class SemanticEntity(Base):
    __tablename__ = "semantic_entities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # user, team, workspace, project, mission, task, workflow, agent, document, event, integration, decision, incident, artifact
    entity_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True) # Authoritative domain ID
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, archived, deleted, unknown
    source: Mapped[str] = mapped_column(String(50), nullable=False, default="native", index=True) # native, integration, derived, ai_suggested
    provider: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    external_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    resource_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    metadata_info: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SemanticRelationship(Base):
    __tablename__ = "semantic_relationships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    from_entity_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    relationship_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # belongs_to, member_of, owns, manages, contains, depends_on, uses, created_by, assigned_to, related_to, references, produces, consumes, triggered_by, supports, implements
    to_entity_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False, default="native", index=True) # native, integration, derived, ai_suggested
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # proposed, verified, rejected, active, invalidated, conflicting
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high") # high, medium, low
    evidence_references: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    valid_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class RelationshipEvidence(Base):
    __tablename__ = "relationship_evidences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    relationship_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evidence_type: Mapped[str] = mapped_column(String(100), nullable=False) # document, event, database_record, workflow, user_action
    reference_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    snippet: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class RelationshipConflict(Base):
    __tablename__ = "relationship_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    relationship_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evidence_a: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    evidence_b: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, resolved
    resolution_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ContextPack(Base):
    __tablename__ = "context_packs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    entity_ids: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    relationship_ids: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    evidence: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    scope: Mapped[str] = mapped_column(String(100), nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

class GraphSyncState(Base):
    __tablename__ = "graph_sync_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_type: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    last_synced_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    sync_status: Mapped[str] = mapped_column(String(50), nullable=False, default="synced", index=True) # synced, syncing, failed
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    items_processed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

class GraphHealthSnapshot(Base):
    __tablename__ = "graph_health_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    entity_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    relationship_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    orphan_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    invalid_relationship_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    sync_lag_seconds: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

class KnowledgeProvenance(Base):
    __tablename__ = "knowledge_provenances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # user, document, email, calendar, integration, database, workflow, agent, system, external_source, generated
    source_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    external_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    origin: Mapped[str] = mapped_column(String(255), nullable=False, default="native")

class SourceAuthority(Base):
    __tablename__ = "source_authorities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    authority_level: Mapped[str] = mapped_column(String(50), nullable=False, default="trusted", index=True) # authoritative, trusted, normal, unverified, generated
    context_scope: Mapped[str] = mapped_column(String(100), nullable=False, default="global")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class KnowledgeClaim(Base):
    __tablename__ = "knowledge_claims"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    predicate: Mapped[str] = mapped_column(String(255), nullable=False)
    object_val: Mapped[str] = mapped_column(Text, nullable=False)
    source_references: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="unverified", index=True) # verified, trusted, unverified, stale, conflicting, deprecated, generated, rejected
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="medium") # high, medium, low
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class KnowledgeConflict(Base):
    __tablename__ = "knowledge_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    claim_a: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    claim_b: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    sources: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, investigating, resolved, accepted_a, accepted_b, superseded
    resolution_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class KnowledgeQualityScore(Base):
    __tablename__ = "knowledge_quality_scores"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_quality: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    freshness_score: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    evidence_coverage: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    consistency_score: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    verification_status: Mapped[str] = mapped_column(String(50), nullable=False, default="unverified")
    composite_score: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class KnowledgeVerification(Base):
    __tablename__ = "knowledge_verifications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    verified_by: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    decision: Mapped[str] = mapped_column(String(50), nullable=False, default="verified") # verified, rejected, deprecated
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

class AIOutputProvenance(Base):
    __tablename__ = "ai_output_provenances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    output_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    model_version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0")
    prompt_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")
    context_references: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    evaluation_status: Mapped[str] = mapped_column(String(50), nullable=False, default="grounded", index=True) # evaluated, not_evaluated, grounded, partially_grounded, unsupported, failed

class KnowledgeFeedback(Base):
    __tablename__ = "knowledge_feedbacks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    output_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    feedback_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # correct, incorrect, outdated, missing_source, conflicting
    comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class KnowledgeGovernanceEvent(Base):
    __tablename__ = "knowledge_governance_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    actor_id: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class EnterpriseEvaluationRun(Base):
    __tablename__ = "ent_eval_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evaluation_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # offline, online, regression, benchmark, human_review, simulation, production_sample
    target_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # response, agent, mission, workflow, retrieval, decision, recommendation, tool_call, memory
    target_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    model_version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0")
    prompt_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")
    context_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="completed", index=True) # running, completed, failed
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class EvaluationDataset(Base):
    __tablename__ = "evaluation_datasets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="workspace")
    is_golden: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class EvaluationDatasetVersion(Base):
    __tablename__ = "evaluation_dataset_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    changes_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class EnterpriseEvaluationCase(Base):
    __tablename__ = "ent_eval_cases"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    input_data: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    expected_output_reference: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    expected_evidence_references: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    metadata_info: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    classification: Mapped[str] = mapped_column(String(50), nullable=False, default="internal")

class EnterpriseEvaluationResult(Base):
    __tablename__ = "ent_eval_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evaluation_run_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    metric: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # correctness, relevance, groundedness, citation_accuracy, completeness, instruction_following, tool_correctness, policy_compliance, safety, latency, cost
    score: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pass") # pass, fail, warning
    evidence: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class EvaluationMetric(Base):
    __tablename__ = "evaluation_metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    dimension: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    metric_type: Mapped[str] = mapped_column(String(50), nullable=False, default="continuous") # binary, continuous
    min_value: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    max_value: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)

class HumanEvaluation(Base):
    __tablename__ = "human_evaluations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evaluator_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evaluation_run_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    criteria: Mapped[str] = mapped_column(String(100), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False, default=5.0)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class EvaluationExperiment(Base):
    __tablename__ = "evaluation_experiments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    baseline_config: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    candidate_config: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="running", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class EvaluationRegression(Base):
    __tablename__ = "evaluation_regressions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    baseline_run_id: Mapped[str] = mapped_column(String(255), nullable=False)
    candidate_run_id: Mapped[str] = mapped_column(String(255), nullable=False)
    metric: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    delta: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="detected", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class EvaluationReport(Base):
    __tablename__ = "evaluation_reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evaluation_run_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    summary: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    metrics_breakdown: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    regressions: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    recommendation: Mapped[str] = mapped_column(String(50), nullable=False, default="promote") # promote, hold, rollback, investigate
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AIQualityAlert(Base):
    __tablename__ = "ai_quality_alerts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    target_type: Mapped[str] = mapped_column(String(100), nullable=False)
    target_id: Mapped[str] = mapped_column(String(255), nullable=False)
    metric: Mapped[str] = mapped_column(String(100), nullable=False)
    current_value: Mapped[float] = mapped_column(Float, nullable=False)
    threshold_value: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class ModelRegistry(Base):
    __tablename__ = "model_registries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    model_key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0")
    capabilities: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    context_window: Mapped[int] = mapped_column(Integer, nullable=False, default=128000)
    supported_inputs: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    supported_outputs: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="available", index=True) # available, degraded, unavailable, disabled, deprecated
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ModelProvider(Base):
    __tablename__ = "model_providers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    provider_key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="healthy", index=True) # healthy, degraded, outage
    region: Mapped[str | None] = mapped_column(String(100), nullable=True)
    capabilities: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ModelVersion(Base):
    __tablename__ = "model_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_key: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    model_key: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    release_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ModelCapability(Base):
    __tablename__ = "model_capabilities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capability_key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True) # text_generation, reasoning, tool_calling, structured_output, vision, long_context, code_generation, embedding, reranking
    description: Mapped[str] = mapped_column(Text, nullable=False)

class ModelRequirements(Base):
    __tablename__ = "model_requirements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    capability: Mapped[str] = mapped_column(String(100), nullable=False)
    minimum_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.8)
    maximum_latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    maximum_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    data_policy: Mapped[str] = mapped_column(String(100), nullable=False, default="internal")
    required_context_window: Mapped[int] = mapped_column(Integer, nullable=False, default=4096)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="normal")

class ModelRoutingRule(Base):
    __tablename__ = "model_routing_rules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="global", index=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    conditions: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    requirements: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    preferred_models: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    fallback_models: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ModelRoutingDecision(Base):
    __tablename__ = "model_routing_decisions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    selected_provider: Mapped[str] = mapped_column(String(100), nullable=False)
    selected_model: Mapped[str] = mapped_column(String(255), nullable=False)
    candidates: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    rejected_candidates: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    reason_codes: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    policy_result: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    routing_policy_version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class ModelHealth(Base):
    __tablename__ = "model_healths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_key: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    provider_key: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    latency_p95_ms: Mapped[float] = mapped_column(Float, nullable=False, default=150.0)
    error_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    availability: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ModelExperiment(Base):
    __tablename__ = "model_experiments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    candidate_model: Mapped[str] = mapped_column(String(255), nullable=False)
    traffic_percentage: Mapped[float] = mapped_column(Float, nullable=False, default=5.0)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="running", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ModelUsage(Base):
    __tablename__ = "model_usages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    provider_key: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    model_key: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    input_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    estimated_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class ModelBudget(Base):
    __tablename__ = "model_budgets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    monthly_limit: Mapped[float] = mapped_column(Float, nullable=False, default=500.0)
    current_spend: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, warning, exceeded
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AgentExecution(Base):
    __tablename__ = "agent_executions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    agent_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    mission_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    workflow_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="created", index=True) # created, queued, running, waiting, paused, awaiting_approval, recovering, completed, failed, cancelled, expired
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    current_step: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class AgentExecutionState(Base):
    __tablename__ = "agent_execution_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    variables: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    completed_steps: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    pending_steps: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    active_steps: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    blocked_steps: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    context_references: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    memory_references: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    last_checkpoint_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AgentExecutionStep(Base):
    __tablename__ = "agent_execution_steps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    step_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # model_call, tool_call, knowledge_retrieval, memory_read, memory_write, agent_delegate, human_approval, condition, parallel_group, checkpoint
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, running, waiting, completed, failed, blocked, cancelled, unknown_outcome
    attempt: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    input_reference: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    output_reference: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_reference: Mapped[dict | None] = mapped_column(JSON, nullable=True)

class ExecutionCheckpoint(Base):
    __tablename__ = "execution_checkpoints"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    execution_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    step_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    state_reference: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    reason: Mapped[str] = mapped_column(String(100), nullable=False, default="step_completed") # step_completed, approval_requested, pause, periodic, before_external_action, recovery, compaction
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class ExecutionStepAttempt(Base):
    __tablename__ = "execution_step_attempts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    step_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="running")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

class ExecutionContextSnapshot(Base):
    __tablename__ = "execution_context_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    goals: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    completed_work: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    evidence_references: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    pending_work: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    decisions: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ExecutionFailure(Base):
    __tablename__ = "execution_failures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    step_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False, default="unknown") # model, tool, policy, authorization, data, dependency, timeout, provider, runtime, unknown
    error_message: Mapped[str] = mapped_column(Text, nullable=False)
    root_cause_summary: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ExecutionUnknownOutcome(Base):
    __tablename__ = "execution_unknown_outcomes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    step_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    idempotency_key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    action_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="unresolved", index=True) # unresolved, resolved_success, resolved_failure
    resolution_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    resolved_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ExecutionBudget(Base):
    __tablename__ = "execution_budgets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    max_duration_sec: Mapped[int] = mapped_column(Integer, nullable=False, default=3600)
    max_steps: Mapped[int] = mapped_column(Integer, nullable=False, default=50)
    max_model_calls: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    max_tool_calls: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    max_cost: Mapped[float] = mapped_column(Float, nullable=False, default=10.0)
    current_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AgentMemory(Base):
    __tablename__ = "agent_memories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    owner_type: Mapped[str] = mapped_column(String(50), nullable=False, default="agent", index=True) # agent, user, workspace, organization, mission, team
    owner_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    memory_type: Mapped[str] = mapped_column(String(50), nullable=False, default="semantic", index=True) # episodic, semantic, procedural, working, preference, execution
    scope: Mapped[str] = mapped_column(String(50), nullable=False, default="workspace", index=True) # private, shared, workspace, organization
    content_reference: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # candidate, active, stale, conflicting, deprecated, rejected, expired
    importance: Mapped[str] = mapped_column(String(50), nullable=False, default="medium") # high, medium, low
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)

class MemoryVersion(Base):
    __tablename__ = "memory_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    memory_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    content_reference: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="human_review")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class MemoryProvenance(Base):
    __tablename__ = "memory_provenances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    memory_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(100), nullable=False, default="conversation") # conversation, execution, workflow, event, document, user_input, integration, agent, human_review, derived
    source_id: Mapped[str] = mapped_column(String(255), nullable=False)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    origin: Mapped[str | None] = mapped_column(String(255), nullable=True)

class AgentMemoryCandidate(Base):
    __tablename__ = "agent_memory_candidates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    proposed_by_agent_id: Mapped[str] = mapped_column(String(255), nullable=False)
    memory_type: Mapped[str] = mapped_column(String(50), nullable=False)
    suggested_content: Mapped[dict] = mapped_column(JSON, nullable=False)
    evidence_reference: Mapped[dict] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending_review", index=True) # pending_review, approved, rejected
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AgentMemoryConflict(Base):
    __tablename__ = "agent_memory_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    memory_id_a: Mapped[str] = mapped_column(String(255), nullable=False)
    memory_id_b: Mapped[str] = mapped_column(String(255), nullable=False)
    conflict_reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="unresolved", index=True) # unresolved, resolved_a, resolved_b, resolved_both
    resolution_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    resolved_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class MemoryVerification(Base):
    __tablename__ = "memory_verifications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    memory_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    verifier_id: Mapped[str] = mapped_column(String(255), nullable=False)
    verification_status: Mapped[str] = mapped_column(String(50), nullable=False, default="verified")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class MemoryFeedback(Base):
    __tablename__ = "memory_feedbacks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    memory_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    feedback_type: Mapped[str] = mapped_column(String(50), nullable=False) # correct, incorrect, outdated, irrelevant
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class MemoryRetentionPolicy(Base):
    __tablename__ = "memory_retention_policies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    memory_type: Mapped[str] = mapped_column(String(50), nullable=False)
    ttl_days: Mapped[int] = mapped_column(Integer, nullable=False, default=90)
    auto_expire: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    indefinite_allowed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class MemoryConsolidationJob(Base):
    __tablename__ = "memory_consolidation_jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    memories_scanned: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    duplicates_merged: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    conflicts_flagged: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    candidates_promoted: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AgentSkill(Base):
    __tablename__ = "agent_skills"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    owner_type: Mapped[str] = mapped_column(String(50), nullable=False, default="workspace", index=True) # agent, team, workspace, organization
    owner_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    skill_type: Mapped[str] = mapped_column(String(50), nullable=False, default="workflow_execution", index=True) # reasoning, research, analysis, coding, communication, data_processing, workflow_execution, decision_support, tool_usage, domain_specific
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # candidate, sandbox, evaluating, approved, canary, active, paused, deprecated, rejected, failed_evaluation
    current_version_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class AgentSkillVersion(Base):
    __tablename__ = "agent_skill_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1, index=True)
    definition_reference: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    input_schema: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    output_schema: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    side_effect_contract: Mapped[str] = mapped_column(String(50), nullable=False, default="read-only") # read-only, external_mutation, communication, data_modification, destructive
    required_capabilities: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    required_tools: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    required_knowledge: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SkillProvenance(Base):
    __tablename__ = "skill_provenances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_executions: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    source_memories: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    source_workflows: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SkillCandidate(Base):
    __tablename__ = "skill_candidates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    proposed_by_agent_id: Mapped[str] = mapped_column(String(255), nullable=False)
    skill_type: Mapped[str] = mapped_column(String(50), nullable=False)
    suggested_definition: Mapped[dict] = mapped_column(JSON, nullable=False)
    evidence_summary: Mapped[dict] = mapped_column(JSON, nullable=False)
    success_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, evaluating, approved, rejected
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SkillEvaluationRecord(Base):
    __tablename__ = "skill_evaluations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_version_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evaluation_run_id: Mapped[str] = mapped_column(String(255), nullable=False)
    correctness_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    grounding_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    safety_score: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    cost_usd: Mapped[float] = mapped_column(Float, nullable=False, default=0.01)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=240)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SkillApproval(Base):
    __tablename__ = "skill_approvals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_version_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    approver_id: Mapped[str] = mapped_column(String(255), nullable=False)
    approval_status: Mapped[str] = mapped_column(String(50), nullable=False, default="approved")
    policy_used: Mapped[str] = mapped_column(String(100), nullable=False, default="policy_standard_read_only")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    approved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SkillDeployment(Base):
    __tablename__ = "skill_deployments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_version_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    mode: Mapped[str] = mapped_column(String(50), nullable=False, default="active") # sandbox, canary, active
    traffic_percentage: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active") # deploying, active, rolled_back, paused
    deployed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class SkillHealth(Base):
    __tablename__ = "skill_healths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_version_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    quality_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    reliability_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.99)
    cost_per_1k: Mapped[float] = mapped_column(Float, nullable=False, default=0.02)
    latency_p95_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=280)
    safety_score: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    freshness_status: Mapped[str] = mapped_column(String(50), nullable=False, default="fresh") # fresh, needs_revalidation, stale
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SkillFeedback(Base):
    __tablename__ = "skill_feedbacks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    feedback_type: Mapped[str] = mapped_column(String(50), nullable=False) # useful, incorrect, outdated, unsafe, too_expensive, too_slow
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SkillDependency(Base):
    __tablename__ = "skill_dependencies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dependency_type: Mapped[str] = mapped_column(String(50), nullable=False) # tool, model, knowledge, skill, workflow
    dependency_target_id: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SkillPolicy(Base):
    __tablename__ = "skill_policies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    skill_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    allowed_agents: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    allowed_tools: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="low") # low, medium, high, critical
    auto_approval_allowed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SkillPackage(Base):
    __tablename__ = "skill_packages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0.0")
    contained_skill_ids: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SkillCompatibility(Base):
    __tablename__ = "skill_compatibilities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_version_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    min_runtime_version: Mapped[str] = mapped_column(String(50), nullable=False, default="2.0.0")
    required_tool_schemas: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Capability(Base):
    __tablename__ = "capabilities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    workspace_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    owner_type: Mapped[str] = mapped_column(String(50), nullable=False, default="workspace", index=True) # agent, user, workspace, organization
    owner_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False, default="productivity", index=True) # research, communication, coding, analytics, productivity, data, knowledge, automation, operations, security, finance, engineering
    type: Mapped[str] = mapped_column(String(50), nullable=False, default="skill", index=True) # skill, tool, workflow, agent, connector, model, knowledge_source, automation
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # draft, published, active, paused, deprecated, revoked
    current_version_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class CapabilityVersion(Base):
    __tablename__ = "capability_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1, index=True)
    definition_reference: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    input_schema: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    output_schema: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    requirements: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    dependencies: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CapabilityProvenance(Base):
    __tablename__ = "capability_provenances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    creator: Mapped[str] = mapped_column(String(255), nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="manual")
    skill_candidate_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    workflow_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    agent_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    organization_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

class CapabilityCompatibility(Base):
    __tablename__ = "capability_compatibilities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capability_version_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    min_runtime_version: Mapped[str] = mapped_column(String(50), nullable=False, default="2.0.0")
    required_tools: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    required_models: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class CapabilityInstallation(Base):
    __tablename__ = "capability_installations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    installed_by: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="installed", index=True) # available, requested, approved, installed, disabled, removed
    installed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CapabilityHealth(Base):
    __tablename__ = "capability_healths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    availability_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.999)
    latency_p95_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=210)
    error_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.001)
    security_state: Mapped[str] = mapped_column(String(50), nullable=False, default="passed")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="healthy", index=True) # healthy, degraded, unavailable, blocked, deprecated
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CapabilityPolicy(Base):
    __tablename__ = "capability_policies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    allowed_agents: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    allowed_workflows: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="low") # low, medium, high, critical
    requires_approval: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CapabilityRequest(Base):
    __tablename__ = "capability_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    requested_by: Mapped[str] = mapped_column(String(255), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, approved, rejected
    reviewed_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CapabilityDependency(Base):
    __tablename__ = "capability_dependencies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dependency_type: Mapped[str] = mapped_column(String(50), nullable=False) # tool, model, knowledge, skill, workflow, connector
    dependency_target_id: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CapabilityPackage(Base):
    __tablename__ = "capability_packages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0.0")
    contained_capability_ids: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CapabilityPackageVersion(Base):
    __tablename__ = "capability_package_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    package_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    capability_versions: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CapabilityFeedback(Base):
    __tablename__ = "capability_feedbacks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    feedback_type: Mapped[str] = mapped_column(String(50), nullable=False) # useful, broken, unsafe, outdated, too_expensive, too_slow
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CapabilityAudit(Base):
    __tablename__ = "capability_audits"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    actor_id: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class MissionObjective(Base):
    __tablename__ = "mission_objectives"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    goal: Mapped[str] = mapped_column(Text, nullable=False)
    clarity: Mapped[str] = mapped_column(String(50), nullable=False, default="clear", index=True) # clear, ambiguous, underspecified, conflicting
    constraints: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    success_criteria: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="normal", index=True) # critical, high, normal, low
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    budget_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="low") # low, medium, high, critical
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class MissionOrchestrationPlan(Base):
    __tablename__ = "mission_orchestration_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1, index=True)
    objective_summary: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="executing", index=True) # draft, proposed, approved, executing, paused, superseded, completed, failed
    max_replans: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    replan_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class MissionPlanVersion(Base):
    __tablename__ = "mission_plan_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1, index=True)
    steps_snapshot: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    dependencies_snapshot: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    assignments_snapshot: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class MissionOrchestrationStep(Base):
    __tablename__ = "mission_orchestration_steps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    plan_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    step_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    step_type: Mapped[str] = mapped_column(String(50), nullable=False, default="agent_task", index=True) # agent_task, skill_task, tool_task, workflow_task, knowledge_task, human_task, approval_task, validation_task, decision_task
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    assigned_executor_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    assigned_executor_type: Mapped[str] = mapped_column(String(50), nullable=False, default="agent") # agent, skill, tool, workflow, human
    required_capability_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, ready, executing, completed, failed, blocked
    input_payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    output_payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class MissionAssignment(Base):
    __tablename__ = "mission_assignments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    step_id: Mapped[str] = mapped_column(String(255), nullable=False)
    agent_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    skill_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    capacity_used: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class MissionDependency(Base):
    __tablename__ = "mission_dependencies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    step_id: Mapped[str] = mapped_column(String(255), nullable=False)
    depends_on_step_id: Mapped[str] = mapped_column(String(255), nullable=False)
    dependency_type: Mapped[str] = mapped_column(String(50), nullable=False, default="execution_dependency") # data_dependency, execution_dependency, approval_dependency, resource_dependency

class MissionDelegation(Base):
    __tablename__ = "mission_delegations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    parent_step_id: Mapped[str] = mapped_column(String(255), nullable=False)
    child_agent_id: Mapped[str] = mapped_column(String(255), nullable=False)
    delegation_depth: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    subtask_contract: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")

class MissionRisk(Base):
    __tablename__ = "mission_risks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    data_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    action_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    financial_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    security_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    execution_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    active_warnings: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class MissionValidation(Base):
    __tablename__ = "mission_validations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    step_id: Mapped[str] = mapped_column(String(255), nullable=False)
    verifier_type: Mapped[str] = mapped_column(String(50), nullable=False, default="action_gateway") # artifact, action_gateway, human, validator_agent
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    evidence_summary: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    validated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class MissionReplan(Base):
    __tablename__ = "mission_replans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    from_version: Mapped[int] = mapped_column(Integer, nullable=False)
    to_version: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_reason: Mapped[str] = mapped_column(Text, nullable=False)
    diff_summary: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class MissionCost(Base):
    __tablename__ = "mission_costs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    estimated_cost_usd: Mapped[float] = mapped_column(Float, nullable=False, default=0.50)
    actual_cost_usd: Mapped[float] = mapped_column(Float, nullable=False, default=0.12)
    model_cost_usd: Mapped[float] = mapped_column(Float, nullable=False, default=0.10)
    tool_cost_usd: Mapped[float] = mapped_column(Float, nullable=False, default=0.02)
    remaining_budget_usd: Mapped[float] = mapped_column(Float, nullable=False, default=10.0)

class MissionApproval(Base):
    __tablename__ = "mission_approvals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    step_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    approver_id: Mapped[str] = mapped_column(String(255), nullable=False)
    approval_status: Mapped[str] = mapped_column(String(50), nullable=False, default="approved")
    policy_used: Mapped[str] = mapped_column(String(100), nullable=False, default="policy_standard_read_only")
    approved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Decision(Base):
    __tablename__ = "decisions_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    mission_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    agent_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    decision_type: Mapped[str] = mapped_column(String(100), nullable=False, default="operational") # operational, strategic, architectural, security, financial
    question: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="analyzing", index=True) # draft, analyzing, options_ready, awaiting_approval, approved, rejected, executing, completed, superseded, expired, cancelled
    current_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    superseded_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DecisionVersion(Base):
    __tablename__ = "decision_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    options_snapshot: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    evidence_snapshot: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    claims_snapshot: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DecisionContextRef(Base):
    __tablename__ = "decision_context_refs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    context_type: Mapped[str] = mapped_column(String(50), nullable=False) # mission, knowledge, memory, graph, event, constraint
    reference_id: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DecisionClaim(Base):
    __tablename__ = "decision_claims"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    claim_type: Mapped[str] = mapped_column(String(50), nullable=False, default="fact", index=True) # fact, inference, assumption, constraint, prediction, recommendation
    content: Mapped[str] = mapped_column(Text, nullable=False)
    uncertainty: Mapped[str] = mapped_column(String(50), nullable=False, default="known") # known, likely, uncertain, unknown
    time_horizon: Mapped[str | None] = mapped_column(String(50), nullable=True)
    source_evidence_ids: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class DecisionEvidence(Base):
    __tablename__ = "decision_evidences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False) # document, database, integration, event, execution, human_input, memory, knowledge_object, semantic_graph, external_source
    source_id: Mapped[str] = mapped_column(String(255), nullable=False)
    claim_summary: Mapped[str] = mapped_column(Text, nullable=False)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    valid_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    authority: Mapped[str] = mapped_column(String(50), nullable=False, default="medium") # high, medium, low
    freshness: Mapped[str] = mapped_column(String(50), nullable=False, default="fresh") # fresh, aging, stale
    relevance: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="verified", index=True) # unverified, verified, stale, contradicted, rejected

class EvidenceConflict(Base):
    __tablename__ = "evidence_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    claim_a: Mapped[str] = mapped_column(Text, nullable=False)
    claim_b: Mapped[str] = mapped_column(Text, nullable=False)
    source_a_id: Mapped[str] = mapped_column(String(255), nullable=False)
    source_b_id: Mapped[str] = mapped_column(String(255), nullable=False)
    authority_a: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    authority_b: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    resolution_status: Mapped[str] = mapped_column(String(50), nullable=False, default="unresolved") # unresolved, resolved_newer_evidence, resolved_authoritative_source, resolved_human_review

class DecisionOption(Base):
    __tablename__ = "decision_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    generated_by: Mapped[str] = mapped_column(String(50), nullable=False, default="agent") # agent, skill, historical, workflow, human
    is_generated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    constraints: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    requirements: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    risks: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class DecisionCriterion(Base):
    __tablename__ = "decision_criteria"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False) # cost, latency, reliability, security, quality, time, compliance
    weight: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    min_threshold: Mapped[float | None] = mapped_column(Float, nullable=True)

class DecisionTradeoff(Base):
    __tablename__ = "decision_tradeoffs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    option_a_id: Mapped[str] = mapped_column(String(255), nullable=False)
    option_b_id: Mapped[str] = mapped_column(String(255), nullable=False)
    advantage_a: Mapped[str] = mapped_column(Text, nullable=False)
    advantage_b: Mapped[str] = mapped_column(Text, nullable=False)
    tradeoff_summary: Mapped[str] = mapped_column(Text, nullable=False)

class DecisionRisk(Base):
    __tablename__ = "decision_risks_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    option_id: Mapped[str] = mapped_column(String(255), nullable=False)
    financial_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    security_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    operational_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    data_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    compliance_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    execution_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    reputational_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")

class DecisionScenarioV2(Base):
    __tablename__ = "decision_scenarios_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    assumptions: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    variables: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    result_summary: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DecisionApproval(Base):
    __tablename__ = "decision_approvals_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    recommended_option_id: Mapped[str] = mapped_column(String(255), nullable=False)
    approver_id: Mapped[str] = mapped_column(String(255), nullable=False)
    approval_status: Mapped[str] = mapped_column(String(50), nullable=False, default="approved") # approved, rejected, override
    override_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    policy_used: Mapped[str] = mapped_column(String(100), nullable=False, default="policy_standard_read_only")
    approved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DecisionOutcomeV2(Base):
    __tablename__ = "decision_outcomes_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    expected_outcome: Mapped[str] = mapped_column(Text, nullable=False)
    actual_outcome: Mapped[str | None] = mapped_column(Text, nullable=True)
    observed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, successful, partial, failed, unknown

class DecisionEvaluation(Base):
    __tablename__ = "decision_evaluations_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evidence_quality_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    option_coverage_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    constraint_compliance_score: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    risk_coverage_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    outcome_quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    calibration_error: Mapped[float | None] = mapped_column(Float, nullable=True)

class DecisionOverride(Base):
    __tablename__ = "decision_overrides"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    actor_id: Mapped[str] = mapped_column(String(255), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    original_option_id: Mapped[str] = mapped_column(String(255), nullable=False)
    selected_option_id: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Policy(Base):
    __tablename__ = "policies_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    policy_type: Mapped[str] = mapped_column(String(50), nullable=False, default="access") # access, data, agent, tool, model, execution, approval, risk, compliance, retention, network, integration
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # draft, active, paused, deprecated, superseded
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=100, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    hierarchy_level: Mapped[str] = mapped_column(String(50), nullable=False, default="workspace") # organization, workspace, team, agent, mission, capability
    conditions: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    actions: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class PolicyVersion(Base):
    __tablename__ = "policy_versions_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    policy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    conditions: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    actions: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class PolicyEvaluation(Base):
    __tablename__ = "policy_evaluations_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    policy_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    decision: Mapped[str] = mapped_column(String(50), nullable=False, default="deny") # allow, deny, approval_required, review_required, restricted, escalated, simulation_required, dry_run_required
    matched_conditions: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    applied_controls: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    latency_ms: Mapped[float] = mapped_column(Float, nullable=False, default=1.5)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class PolicyRequest(Base):
    __tablename__ = "policy_requests_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    actor_id: Mapped[str] = mapped_column(String(255), nullable=False)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # read, write, delete, send, execute, approve, deploy, publish, export, share
    resource_id: Mapped[str] = mapped_column(String(255), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False) # document, email, calendar, database, API, tool, workflow, agent, skill, capability, model, knowledge_object
    context: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class PolicyControl(Base):
    __tablename__ = "policy_controls"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evaluation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    control_type: Mapped[str] = mapped_column(String(50), nullable=False) # approval, data_redaction, sandbox, rate_limit, scope_limit, time_limit, human_review, dual_approval, simulation
    parameters: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="enforced")

class RiskAssessment(Base):
    __tablename__ = "risk_assessments_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    overall_risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="low") # low, medium, high, critical
    data_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    financial_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    security_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    privacy_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    operational_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    compliance_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    reputational_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    score: Mapped[float] = mapped_column(Float, nullable=False, default=0.1)

class PolicyConflict(Base):
    __tablename__ = "policy_conflicts_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    policy_a_id: Mapped[str] = mapped_column(String(255), nullable=False)
    policy_b_id: Mapped[str] = mapped_column(String(255), nullable=False)
    conflict_description: Mapped[str] = mapped_column(Text, nullable=False)
    precedence_applied: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="unresolved", index=True) # unresolved, resolved_hierarchy, resolved_deny_wins, resolved_admin

class PolicyGap(Base):
    __tablename__ = "policy_gaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    frequency: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    recommended_control: Mapped[str] = mapped_column(String(100), nullable=False, default="approval_required")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, drafted, resolved, ignored

class PolicySimulationV2(Base):
    __tablename__ = "policy_simulations_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_policy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    test_type: Mapped[str] = mapped_column(String(50), nullable=False, default="shadow") # historical, synthetic, shadow
    comparison_results: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class PolicyOverride(Base):
    __tablename__ = "policy_overrides_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    policy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    actor_id: Mapped[str] = mapped_column(String(255), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    scope: Mapped[str] = mapped_column(String(255), nullable=False, default="single_request")
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TemporaryAccessGrant(Base):
    __tablename__ = "temporary_access_grants"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(255), nullable=False)
    capability: Mapped[str] = mapped_column(String(100), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    granted_by: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")

class BreakGlassGrant(Base):
    __tablename__ = "break_glass_grants"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    authorized_by: Mapped[str] = mapped_column(String(255), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    audit_trail_id: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")

class SecurityEvent(Base):
    __tablename__ = "security_events_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # authentication_anomaly, authorization_violation, prompt_injection, tool_abuse, data_exfiltration, credential_exposure, privilege_escalation, memory_poisoning, knowledge_poisoning, capability_anomaly, delegation_anomaly, policy_bypass, cross_tenant_attempt, supply_chain_risk, behavioral_anomaly
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True) # info, low, medium, high, critical
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    actor: Mapped[str] = mapped_column(String(255), nullable=False)
    resource: Mapped[str] = mapped_column(String(255), nullable=False)
    mission_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    agent_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="new", index=True)

class SecuritySignal(Base):
    __tablename__ = "security_signals_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    signal_type: Mapped[str] = mapped_column(String(50), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    evidence: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ThreatFinding(Base):
    __tablename__ = "threat_findings_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    security_event_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    threat_type: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="new", index=True) # new, investigating, confirmed, false_positive, contained, resolved, accepted_risk
    evidence: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    recommended_action: Mapped[str] = mapped_column(String(100), nullable=False, default="monitor")

class SecurityIncident(Base):
    __tablename__ = "security_incidents_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, investigating, contained, resolved, closed
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class SecurityInvestigation(Base):
    __tablename__ = "security_investigations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    investigator_id: Mapped[str] = mapped_column(String(255), nullable=False)
    timeline: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    evidence: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SecurityQuarantine(Base):
    __tablename__ = "security_quarantines"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_type: Mapped[str] = mapped_column(String(50), nullable=False) # agent, skill, capability, workflow, integration
    target_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    scope: Mapped[str] = mapped_column(String(255), nullable=False, default="full_isolation")
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    release_policy: Mapped[str] = mapped_column(String(100), nullable=False, default="security_admin_approval")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, released, expired

class ThreatChain(Base):
    __tablename__ = "threat_chains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    event_ids: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    attack_path: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ThreatIntelligenceSignal(Base):
    __tablename__ = "threat_intelligence_signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    freshness: Mapped[str] = mapped_column(String(50), nullable=False, default="fresh")
    indicator_type: Mapped[str] = mapped_column(String(50), nullable=False) # domain, IP, URL, hash, package, capability, model, tool
    indicator_value: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    context: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AgentBehaviorBaseline(Base):
    __tablename__ = "agent_behavior_baselines"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    agent_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    tool_frequency_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    avg_latency_ms: Mapped[float] = mapped_column(Float, nullable=False, default=150.0)
    avg_data_volume_bytes: Mapped[int] = mapped_column(Integer, nullable=False, default=2048)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class BehaviorAnomaly(Base):
    __tablename__ = "behavior_anomalies_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    anomaly_type: Mapped[str] = mapped_column(String(50), nullable=False) # frequency, sequence, volume, target, timing, capability
    deviation_score: Mapped[float] = mapped_column(Float, nullable=False, default=3.5)
    evidence: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class SecurityEvidence(Base):
    __tablename__ = "security_evidences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    evidence_data: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    integrity_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SecurityResponse(Base):
    __tablename__ = "security_responses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    finding_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    action_taken: Mapped[str] = mapped_column(String(50), nullable=False) # monitor, approval, restrict, quarantine, block
    policy_reference: Mapped[str] = mapped_column(String(255), nullable=False)
    enforced_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SecurityResponsePlan(Base):
    __tablename__ = "security_response_plans_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", index=True) # draft, simulated, approved, executing, completed, failed
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    approval_requirements: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SecurityResponsePlanVersion(Base):
    __tablename__ = "security_response_plan_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    actions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SecurityResponseAction(Base):
    __tablename__ = "security_response_actions_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False) # monitor, notify, restrict, rate_limit, quarantine, pause_agent, disable_capability, block_tool, revoke_session, require_approval, revalidate_decision, pause_mission, cancel_mission
    target_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_id: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(255), nullable=False, default="resource")
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    authorization: Mapped[str] = mapped_column(String(255), nullable=False, default="security_policy")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, approved, executing, completed, failed, blocked, expired
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class SecurityPostIncidentReview(Base):
    __tablename__ = "security_post_incident_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    root_cause_type: Mapped[str] = mapped_column(String(50), nullable=False, default="confirmed") # confirmed, likely, unknown
    root_cause_summary: Mapped[str] = mapped_column(Text, nullable=False)
    detection_quality_score: Mapped[float] = mapped_column(Float, nullable=False, default=4.5)
    response_quality_score: Mapped[float] = mapped_column(Float, nullable=False, default=4.8)
    lessons_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SecurityDetectionRule(Base):
    __tablename__ = "security_detection_rules_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    conditions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    scope: Mapped[str] = mapped_column(String(255), nullable=False, default="global")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="shadow", index=True) # draft, simulation, shadow, active, paused, deprecated
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SecurityDetectionRuleVersion(Base):
    __tablename__ = "security_detection_rule_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    conditions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SecurityAutomationRule(Base):
    __tablename__ = "security_automation_rules_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    trigger_event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    condition_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    response_action_type: Mapped[str] = mapped_column(String(50), nullable=False)
    scope: Mapped[str] = mapped_column(String(255), nullable=False, default="workspace")
    max_actions: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    cooldown_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=300)
    approval_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SecurityRunbook(Base):
    __tablename__ = "security_runbooks_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    trigger_condition: Mapped[str] = mapped_column(String(255), nullable=False)
    investigation_steps_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    approved_responses_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    verification_steps_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SecurityRunbookVersion(Base):
    __tablename__ = "security_runbook_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    runbook_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    content_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SecurityInvestigationNote(Base):
    __tablename__ = "security_investigation_notes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    author_id: Mapped[str] = mapped_column(String(255), nullable=False)
    author_type: Mapped[str] = mapped_column(String(50), nullable=False, default="human-authored") # human-authored, AI-generated
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SecuritySLA(Base):
    __tablename__ = "security_slas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    time_to_detect_seconds: Mapped[float] = mapped_column(Float, nullable=False, default=45.0)
    time_to_triage_seconds: Mapped[float] = mapped_column(Float, nullable=False, default=120.0)
    time_to_contain_seconds: Mapped[float] = mapped_column(Float, nullable=False, default=300.0)
    time_to_recover_seconds: Mapped[float] = mapped_column(Float, nullable=False, default=1800.0)
    sla_breached: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SecurityResponseExecution(Base):
    __tablename__ = "security_response_executions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    execution_status: Mapped[str] = mapped_column(String(50), nullable=False, default="completed") # completed, failed, blocked
    result_details_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ComponentHealth(Base):
    __tablename__ = "component_healths_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    component_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    component_type: Mapped[str] = mapped_column(String(50), nullable=False) # agent, model, tool, integration, database, queue, event_stream, knowledge, memory, workflow, service
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="healthy", index=True) # healthy, degraded, unavailable, recovering, unknown
    latency_ms: Mapped[float] = mapped_column(Float, nullable=False, default=45.0)
    error_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.001)
    availability_pct: Mapped[float] = mapped_column(Float, nullable=False, default=99.95)
    last_healthy_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class FailureEvent(Base):
    __tablename__ = "failure_events_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    component_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    failure_type: Mapped[str] = mapped_column(String(50), nullable=False) # timeout, provider_outage, dependency_failure, capacity_exhaustion, data_corruption, network_failure, authentication_failure, authorization_failure, schema_failure, queue_failure, unknown_failure
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class DegradationMode(Base):
    __tablename__ = "degradation_modes_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scope: Mapped[str] = mapped_column(String(255), nullable=False, default="global")
    mode: Mapped[str] = mapped_column(String(50), nullable=False) # read_only, limited_execution, no_external_actions, approval_required, model_fallback, queue_only, manual_operation
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, resolved
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CircuitBreakerState(Base):
    __tablename__ = "circuit_breaker_states_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    state: Mapped[str] = mapped_column(String(50), nullable=False, default="closed") # closed, open, half_open
    failure_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_state_change_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DeadLetterEntry(Base):
    __tablename__ = "dead_letter_entries_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_ref: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    queue_name: Mapped[str] = mapped_column(String(100), nullable=False)
    failure_reason: Mapped[str] = mapped_column(Text, nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, replayed, discarded
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class RecoveryPlan(Base):
    __tablename__ = "recovery_plans_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    components_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    rto_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=300)
    rpo_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=60)
    recovery_order_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # draft, simulated, active, completed
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class RecoveryPlanVersion(Base):
    __tablename__ = "recovery_plan_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    plan_content_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class RecoveryStep(Base):
    __tablename__ = "recovery_steps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    step_number: Mapped[int] = mapped_column(Integer, nullable=False)
    action_description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending") # pending, executing, completed, failed

class IntegrityCheck(Base):
    __tablename__ = "integrity_checks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_resource: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    schema_valid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    checksum_valid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    relationships_valid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="passed") # passed, corrupted
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class RecoveryExecution(Base):
    __tablename__ = "recovery_executions_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="executing", index=True) # executing, completed, failed
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class ResilienceExperiment(Base):
    __tablename__ = "resilience_experiments_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    experiment_type: Mapped[str] = mapped_column(String(50), nullable=False) # latency_injection, error_injection, dependency_disablement, queue_saturation, model_outage_simulation, tool_outage_simulation
    target_scope: Mapped[str] = mapped_column(String(255), nullable=False, default="sandbox")
    blast_radius_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    abort_conditions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", index=True) # draft, running, completed, aborted
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ExperimentResult(Base):
    __tablename__ = "experiment_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    experiment_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    findings_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    aborted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    abort_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ReliabilityBudget(Base):
    __tablename__ = "reliability_budgets_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    allowed_error_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.1) # 99.9% SLO -> 0.1% budget
    current_burn_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.02)
    budget_remaining_pct: Mapped[float] = mapped_column(Float, nullable=False, default=80.0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ResilienceSLO(Base):
    __tablename__ = "resilience_slos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slo_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    target_availability_pct: Mapped[float] = mapped_column(Float, nullable=False, default=99.9)
    current_availability_pct: Mapped[float] = mapped_column(Float, nullable=False, default=99.95)
    target_latency_ms: Mapped[float] = mapped_column(Float, nullable=False, default=200.0)
    current_latency_ms: Mapped[float] = mapped_column(Float, nullable=False, default=45.0)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="compliant") # compliant, warning, breached
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CapacitySnapshot(Base):
    __tablename__ = "capacity_snapshots_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cpu_pct: Mapped[float] = mapped_column(Float, nullable=False, default=35.0)
    memory_pct: Mapped[float] = mapped_column(Float, nullable=False, default=42.0)
    queue_depth: Mapped[int] = mapped_column(Integer, nullable=False, default=12)
    concurrency_level: Mapped[int] = mapped_column(Integer, nullable=False, default=8)
    load_shedding_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class StateLease(Base):
    __tablename__ = "state_leases"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    owner_worker_id: Mapped[str] = mapped_column(String(255), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active") # active, expired

class AIUsageEvent(Base):
    __tablename__ = "ai_usage_events_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    agent_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    mission_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    decision_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    workflow_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    model_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    provider_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    capability_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    usage_type: Mapped[str] = mapped_column(String(50), nullable=False) # model_input, model_output, embedding, retrieval, tool_call, workflow_execution, agent_execution, storage, compute, network, integration
    units_used: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    tokens_input: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tokens_output: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tokens_cached: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tokens_reasoning: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    latency_ms: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class AIPriceCatalog(Base):
    __tablename__ = "ai_price_catalogs_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    unit: Mapped[str] = mapped_column(String(50), nullable=False) # 1k_tokens, 1k_cached, 1k_embeddings, request
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.002)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="provider_api")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CostCalculation(Base):
    __tablename__ = "cost_calculations_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usage_event_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    price_version_id: Mapped[str] = mapped_column(String(255), nullable=False)
    units: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    estimated_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    actual_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    cost_status: Mapped[str] = mapped_column(String(50), nullable=False, default="estimated", index=True) # estimated, reported, reconciled, unknown
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    agent_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    mission_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class AIBudget(Base):
    __tablename__ = "ai_budgets_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    team_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    agent_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    mission_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    scope: Mapped[str] = mapped_column(String(50), nullable=False, default="organization", index=True) # organization, workspace, team, agent, mission
    period: Mapped[str] = mapped_column(String(50), nullable=False, default="monthly") # daily, weekly, monthly, custom
    limit_amount: Mapped[float] = mapped_column(Float, nullable=False, default=1000.0)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    spent_amount: Mapped[float] = mapped_column(Float, nullable=False, default=120.0)
    committed_amount: Mapped[float] = mapped_column(Float, nullable=False, default=50.0)
    forecast_amount: Mapped[float] = mapped_column(Float, nullable=False, default=450.0)
    remaining_amount: Mapped[float] = mapped_column(Float, nullable=False, default=830.0)
    soft_threshold_pct: Mapped[float] = mapped_column(Float, nullable=False, default=75.0)
    hard_limit_action: Mapped[str] = mapped_column(String(50), nullable=False, default="require_approval") # block, pause, require_approval, degrade
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="healthy", index=True) # healthy, warning, exceeded

class CostForecast(Base):
    __tablename__ = "cost_forecasts_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    scope: Mapped[str] = mapped_column(String(50), nullable=False, default="organization")
    current_period_expected: Mapped[float] = mapped_column(Float, nullable=False, default=450.0)
    lower_bound: Mapped[float] = mapped_column(Float, nullable=False, default=380.0)
    upper_bound: Mapped[float] = mapped_column(Float, nullable=False, default=520.0)
    confidence_pct: Mapped[float] = mapped_column(Float, nullable=False, default=92.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CostDriver(Base):
    __tablename__ = "cost_drivers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    driver_type: Mapped[str] = mapped_column(String(50), nullable=False) # high_token_mission, repeated_retries, inefficient_workflow, expensive_model, excessive_retrieval, tool_loop
    resource_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    cost_impact: Mapped[float] = mapped_column(Float, nullable=False, default=75.0)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AIValueMetric(Base):
    __tablename__ = "ai_value_metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    quality_score: Mapped[float] = mapped_column(Float, nullable=False, default=4.8)
    success_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.98)
    latency_p95_ms: Mapped[float] = mapped_column(Float, nullable=False, default=180.0)
    cost_amount: Mapped[float] = mapped_column(Float, nullable=False, default=1.25)
    value_index: Mapped[float] = mapped_column(Float, nullable=False, default=3.84)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class OptimizationRecommendation(Base):
    __tablename__ = "optimization_recommendations_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False) # model_switch, prompt_reduction, retrieval_reduction, retry_reduction, workflow_optimization, cache_usage, batching, scheduling
    estimated_savings: Mapped[float] = mapped_column(Float, nullable=False, default=120.0)
    quality_impact: Mapped[str] = mapped_column(String(50), nullable=False, default="neutral")
    latency_impact: Mapped[str] = mapped_column(String(50), nullable=False, default="improved")
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    confidence_pct: Mapped[float] = mapped_column(Float, nullable=False, default=95.0)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    approval_status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # draft, pending, approved, applied, reverted
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CostOptimizationExperiment(Base):
    __tablename__ = "cost_optimization_experiments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recommendation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    baseline_config_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    optimized_config_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    baseline_cost: Mapped[float] = mapped_column(Float, nullable=False, default=15.0)
    optimized_cost: Mapped[float] = mapped_column(Float, nullable=False, default=8.5)
    baseline_quality: Mapped[float] = mapped_column(Float, nullable=False, default=4.8)
    optimized_quality: Mapped[float] = mapped_column(Float, nullable=False, default=4.78)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="running", index=True) # running, completed, reverted
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AICapacitySnapshot(Base):
    __tablename__ = "ai_capacity_snapshots_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    concurrency_used: Mapped[int] = mapped_column(Integer, nullable=False, default=12)
    concurrency_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=50)
    queue_depth: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    provider_limits_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    load_shedding_recommended: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class ProviderCapacityLimit(Base):
    __tablename__ = "provider_capacity_limits"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    rpm_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=10000)
    tpm_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=2000000)
    concurrency_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    quota_used_pct: Mapped[float] = mapped_column(Float, nullable=False, default=24.5)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CostReconciliation(Base):
    __tablename__ = "cost_reconciliations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    period: Mapped[str] = mapped_column(String(50), nullable=False, default="2026-08")
    estimated_total: Mapped[float] = mapped_column(Float, nullable=False, default=120.0)
    provider_reported_total: Mapped[float] = mapped_column(Float, nullable=False, default=121.5)
    variance_amount: Mapped[float] = mapped_column(Float, nullable=False, default=1.5)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="matched", index=True) # matched, variance, unavailable
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CostAdjustment(Base):
    __tablename__ = "cost_adjustments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cost_calculation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    original_amount: Mapped[float] = mapped_column(Float, nullable=False)
    adjusted_amount: Mapped[float] = mapped_column(Float, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    adjusted_by_user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SpendAnomaly(Base):
    __tablename__ = "spend_anomalies_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    spike_magnitude_pct: Mapped[float] = mapped_column(Float, nullable=False, default=145.0)
    anomaly_classification: Mapped[str] = mapped_column(String(50), nullable=False, default="unexpected") # normal, unexpected, investigate
    driver_summary: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class WorkItem(Base):
    __tablename__ = "work_items_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    team_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    mission_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    parent_work_item_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="medium") # low, medium, high, urgent
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="backlog", index=True) # backlog, ready, assigned, in_progress, blocked, awaiting_review, awaiting_approval, completed, cancelled
    assignee_type: Mapped[str] = mapped_column(String(50), nullable=False, default="agent", index=True) # human, agent, team, hybrid
    assignee_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    work_classification: Mapped[str] = mapped_column(String(50), nullable=False, default="agent_suitable") # automatable, agent_suitable, human_required, hybrid, restricted
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class WorkHandoff(Base):
    __tablename__ = "work_handoffs_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_item_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    from_id: Mapped[str] = mapped_column(String(255), nullable=False)
    from_type: Mapped[str] = mapped_column(String(50), nullable=False) # human, agent
    to_id: Mapped[str] = mapped_column(String(255), nullable=False)
    to_type: Mapped[str] = mapped_column(String(50), nullable=False) # human, agent
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    context_references_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    expected_output: Mapped[str] = mapped_column(Text, nullable=False)
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, accepted, rejected

class CollaborationSession(Base):
    __tablename__ = "collaboration_sessions_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_item_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    mission_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="contributor") # owner, contributor, reviewer, approver, observer
    user_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    agent_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CollaborationEscalation(Base):
    __tablename__ = "collaboration_escalations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_item_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    escalation_type: Mapped[str] = mapped_column(String(50), nullable=False) # risk, deadline, uncertainty, approval, dependency, capacity, conflict
    target_role_or_user: Mapped[str] = mapped_column(String(255), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, resolved, timed_out

class ExpertiseProfile(Base):
    __tablename__ = "expertise_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    skills_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    capabilities_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    domains_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    verified_experience_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    confidence_pct: Mapped[float] = mapped_column(Float, nullable=False, default=90.0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class WorkBlocker(Base):
    __tablename__ = "work_blockers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_item_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    blocker_type: Mapped[str] = mapped_column(String(50), nullable=False) # dependency, approval, capacity, data, policy, agent, human
    description: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_action: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, resolved

class WorkRoutingRecommendation(Base):
    __tablename__ = "work_routing_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_item_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    recommended_executor_type: Mapped[str] = mapped_column(String(50), nullable=False) # human, agent, hybrid
    recommended_executor_id: Mapped[str] = mapped_column(String(255), nullable=False)
    reason_summary: Mapped[str] = mapped_column(Text, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    cost_estimate: Mapped[float] = mapped_column(Float, nullable=False, default=1.5)
    deadline_impact: Mapped[str] = mapped_column(String(50), nullable=False, default="minimal")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CollaborationFeedback(Base):
    __tablename__ = "collaboration_feedback_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_item_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    feedback_type: Mapped[str] = mapped_column(String(50), nullable=False) # correction, approval, rejection, suggestion, rating
    rating_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    author_user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CollaborationReview(Base):
    __tablename__ = "collaboration_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_item_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    review_type: Mapped[str] = mapped_column(String(50), nullable=False) # fact_check, quality_review, security_review, business_review, final_acceptance
    artifact_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    reviewer_id: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, approved, rejected
    comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TeamWorkloadSnapshot(Base):
    __tablename__ = "team_workload_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    assigned_count: Mapped[int] = mapped_column(Integer, nullable=False, default=14)
    active_count: Mapped[int] = mapped_column(Integer, nullable=False, default=6)
    blocked_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    pending_review_count: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    workload_fairness_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Outcome(Base):
    __tablename__ = "outcomes_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # planned, active, at_risk, blocked, achieved, cancelled
    target: Mapped[str] = mapped_column(String(255), nullable=False)
    current_state: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class OperatingChangeEvent(Base):
    __tablename__ = "operating_change_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    change_type: Mapped[str] = mapped_column(String(50), nullable=False) # ownership_change, capability_change, workflow_change, dependency_change, mission_change, policy_change
    target_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    impact_summary: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high") # high, medium, low
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class OperatingScenario(Base):
    __tablename__ = "operating_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    assumptions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    affected_nodes_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    expected_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    confidence_pct: Mapped[float] = mapped_column(Float, nullable=False, default=92.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class OperatingRisk(Base):
    __tablename__ = "operating_risks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dimension: Mapped[str] = mapped_column(String(50), nullable=False) # dependency, capacity, knowledge, workflow, integration, decision, security
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    source_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="identified", index=True) # identified, monitoring, mitigating, resolved, accepted
    mitigation_recommendations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class CapabilityGap(Base):
    __tablename__ = "capability_gaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    required_by_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    gap_classification: Mapped[str] = mapped_column(String(50), nullable=False, default="missing") # missing, under_capacity, restricted, unavailable, unknown
    impact_summary: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, addressed
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class OperatingBottleneck(Base):
    __tablename__ = "operating_bottlenecks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    blocker_type: Mapped[str] = mapped_column(String(50), nullable=False) # approval, capacity, dependency, knowledge, integration
    root_dependency_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    affected_work_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    duration_hours: Mapped[float] = mapped_column(Float, nullable=False, default=4.5)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, resolved
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class OperatingDependency(Base):
    __tablename__ = "operating_dependencies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_type: Mapped[str] = mapped_column(String(50), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(50), nullable=False) # OWNS, MEMBER_OF, ASSIGNED_TO, EXECUTES, DEPENDS_ON, BLOCKS, REQUIRES, PRODUCES, CONSUMES, REVIEWS, APPROVES, ESCALATES_TO, SUPPORTED_BY, USES, RELATED_TO, INFORMS, RESULTS_IN
    health: Mapped[str] = mapped_column(String(50), nullable=False, default="healthy") # healthy, degraded, blocked, unknown
    is_critical_path: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    freshness_policy_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=24)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class GraphValidationIssue(Base):
    __tablename__ = "graph_validation_issues"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    issue_type: Mapped[str] = mapped_column(String(50), nullable=False) # orphan_node, invalid_edge, conflicting_ownership, missing_dependency, stale_relationship
    node_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    suggested_repair: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, resolved
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class GraphRelationshipSnapshot(Base):
    __tablename__ = "graph_relationship_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    node_count: Mapped[int] = mapped_column(Integer, nullable=False, default=450)
    edge_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1250)
    health_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class StrategicPlan(Base):
    __tablename__ = "strategic_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", index=True) # draft, active, paused, completed, archived
    start_date: Mapped[str] = mapped_column(String(50), nullable=False)
    end_date: Mapped[str] = mapped_column(String(50), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class StrategicPlanVersion(Base):
    __tablename__ = "strategic_plan_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class StrategicObjective(Base):
    __tablename__ = "strategic_objectives"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="high") # critical, high, medium, low
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # planned, active, at_risk, blocked, achieved, cancelled
    target: Mapped[str] = mapped_column(String(255), nullable=False)
    current_state: Mapped[str] = mapped_column(String(255), nullable=False)
    deadline: Mapped[str] = mapped_column(String(50), nullable=False)

class StrategicInitiative(Base):
    __tablename__ = "strategic_initiatives"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    objective_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # proposed, approved, active, paused, at_risk, completed, cancelled
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    expected_outcome: Mapped[str] = mapped_column(Text, nullable=False)
    estimated_cost: Mapped[float] = mapped_column(Float, nullable=False, default=100000.0)
    estimated_duration: Mapped[str] = mapped_column(String(50), nullable=False, default="6 months")

class StrategicAssumption(Base):
    __tablename__ = "strategic_assumptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    statement: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high") # high, medium, low
    assumption_type: Mapped[str] = mapped_column(String(50), nullable=False) # market, customer, financial, operational, technical, regulatory, capacity, competitive
    validity: Mapped[str] = mapped_column(String(50), nullable=False, default="valid", index=True) # valid, uncertain, invalid, expired
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)

class StrategicPrioritization(Base):
    __tablename__ = "strategic_prioritizations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    alignment_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.9)
    outcome_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    cost_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.8)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.2)
    dependency_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.3)
    time_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    explanation_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class StrategicRecommendation(Base):
    __tablename__ = "strategic_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    recommendation: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    alternatives_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list) # Option A, Option B, Option C
    tradeoffs_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    risks_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    assumptions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    confidence_pct: Mapped[float] = mapped_column(Float, nullable=False, default=90.0)

class StrategicReview(Base):
    __tablename__ = "strategic_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    review_cadence: Mapped[str] = mapped_column(String(50), nullable=False, default="quarterly") # weekly, monthly, quarterly, custom
    progress_summary: Mapped[str] = mapped_column(Text, nullable=False)
    assumptions_evaluated_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    risks_evaluated_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    drift_summary: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class StrategicDrift(Base):
    __tablename__ = "strategic_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    drift_type: Mapped[str] = mapped_column(String(50), nullable=False) # execution, resource, assumption, outcome, dependency
    signal_summary: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, resolved
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class StrategicAlert(Base):
    __tablename__ = "strategic_alerts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    alert_type: Mapped[str] = mapped_column(String(50), nullable=False) # objective_at_risk, assumption_invalidated, critical_dependency_failure, budget_pressure, capacity_pressure, deadline_risk
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, acknowledged, resolved
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class StrategicDecisionLink(Base):
    __tablename__ = "strategic_decision_links"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False)
    reversibility: Mapped[str] = mapped_column(String(50), nullable=False, default="reversible") # reversible, partially_reversible, irreversible
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class StrategicResourceConstraint(Base):
    __tablename__ = "strategic_resource_constraints"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    constraint_type: Mapped[str] = mapped_column(String(50), nullable=False) # budget, capacity, skill, technology, time
    description: Mapped[str] = mapped_column(Text, nullable=False)
    affected_initiatives_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class Portfolio(Base):
    __tablename__ = "portfolios_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # draft, active, under_review, paused, completed, archived
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class PortfolioVersion(Base):
    __tablename__ = "portfolio_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Program(Base):
    __tablename__ = "programs_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # proposed, approved, active, at_risk, paused, completed, cancelled
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    target_outcome: Mapped[str] = mapped_column(String(255), nullable=False)

class PortfolioDependency(Base):
    __tablename__ = "portfolio_dependencies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_type: Mapped[str] = mapped_column(String(50), nullable=False)
    dependency_type: Mapped[str] = mapped_column(String(50), nullable=False) # technical, organizational, financial, capacity, knowledge, security, regulatory
    health: Mapped[str] = mapped_column(String(50), nullable=False, default="healthy") # healthy, watch, at_risk, blocked, unknown

class PortfolioResourceAllocation(Base):
    __tablename__ = "portfolio_resource_allocations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False) # budget, human_capacity, agent_capacity, compute, model_capacity, integration_capacity, workspace_capacity
    allocated_amount: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    used_amount: Mapped[float] = mapped_column(Float, nullable=False, default=65.0)
    requested_amount: Mapped[float] = mapped_column(Float, nullable=False, default=120.0)

class PortfolioResourceConflict(Base):
    __tablename__ = "portfolio_resource_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    competing_initiatives_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    time_window: Mapped[str] = mapped_column(String(100), nullable=False, default="Q3 2026")
    capacity_gap_summary: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, resolved

class PortfolioOverlap(Base):
    __tablename__ = "portfolio_overlaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    initiative_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    overlap_type: Mapped[str] = mapped_column(String(50), nullable=False) # objective, deliverable, capability, workflow
    similarity_summary: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, dismissed

class PortfolioOutcomeVariance(Base):
    __tablename__ = "portfolio_outcome_variances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    variance_type: Mapped[str] = mapped_column(String(50), nullable=False, default="on_track", index=True) # ahead, on_track, behind, unknown
    expected_outcome: Mapped[str] = mapped_column(Text, nullable=False)
    measured_outcome: Mapped[str] = mapped_column(Text, nullable=False)
    delta_summary: Mapped[str] = mapped_column(Text, nullable=False)

class InvestmentOption(Base):
    __tablename__ = "investment_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    option_type: Mapped[str] = mapped_column(String(50), nullable=False) # increase, maintain, reduce, pause, accelerate, sequence_change
    description: Mapped[str] = mapped_column(Text, nullable=False)
    benefit_summary: Mapped[str] = mapped_column(Text, nullable=False)
    estimated_cost_delta: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    risk_delta: Mapped[str] = mapped_column(String(50), nullable=False, default="low")

class PortfolioRecommendation(Base):
    __tablename__ = "portfolio_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    recommendation: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    alternatives_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    tradeoffs_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    reversibility: Mapped[str] = mapped_column(String(50), nullable=False, default="reversible") # reversible, partially_reversible, irreversible
    approval_status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, approved, rejected
    confidence_pct: Mapped[float] = mapped_column(Float, nullable=False, default=92.0)

class PortfolioReview(Base):
    __tablename__ = "portfolio_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    review_cadence: Mapped[str] = mapped_column(String(50), nullable=False, default="quarterly") # weekly, monthly, quarterly, custom
    progress_summary: Mapped[str] = mapped_column(Text, nullable=False)
    cost_variance_summary: Mapped[str] = mapped_column(Text, nullable=False)
    schedule_variance_summary: Mapped[str] = mapped_column(Text, nullable=False)
    risk_exposure_summary: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class PortfolioDrift(Base):
    __tablename__ = "portfolio_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    drift_type: Mapped[str] = mapped_column(String(50), nullable=False) # cost, schedule, outcome, risk, strategic, capacity
    signal_summary: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, resolved
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class PortfolioAlert(Base):
    __tablename__ = "portfolio_alerts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    alert_type: Mapped[str] = mapped_column(String(50), nullable=False) # budget_pressure, capacity_pressure, dependency_failure, outcome_deterioration, risk_escalation
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, acknowledged, resolved
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Benefit(Base):
    __tablename__ = "benefits_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    portfolio_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    program_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    initiative_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    outcome_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="planned", index=True) # planned, measuring, on_track, at_risk, achieved, partially_achieved, not_achieved, unknown
    benefit_type: Mapped[str] = mapped_column(String(50), nullable=False) # financial, operational, customer, quality, risk_reduction, capacity, revenue, cost_reduction, time_saved, strategic
    baseline: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    target: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    current_value: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    unit: Mapped[str] = mapped_column(String(50), nullable=False, default="USD")
    measurement_method: Mapped[str] = mapped_column(Text, nullable=False)
    target_date: Mapped[str] = mapped_column(String(50), nullable=False, default="2026-12-31", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class BenefitEvidence(Base):
    __tablename__ = "benefit_evidences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    benefit_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    reference: Mapped[str] = mapped_column(Text, nullable=False)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=90.0)
    verification_status: Mapped[str] = mapped_column(String(50), nullable=False, default="unverified", index=True) # unverified, verified, rejected, stale

class BenefitMeasurement(Base):
    __tablename__ = "benefit_measurements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    benefit_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    baseline: Mapped[float] = mapped_column(Float, nullable=False)
    current: Mapped[float] = mapped_column(Float, nullable=False)
    target: Mapped[float] = mapped_column(Float, nullable=False)
    variance: Mapped[float] = mapped_column(Float, nullable=False)
    measurement_period: Mapped[str] = mapped_column(String(100), nullable=False, default="Q3 2026")
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class BenefitRealizationPlan(Base):
    __tablename__ = "benefit_realization_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    benefit_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    actions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    milestones_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    measurement_method: Mapped[str] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    target_date: Mapped[str] = mapped_column(String(50), nullable=False)

class ExecutionMilestone(Base):
    __tablename__ = "execution_milestones"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    due_date: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="planned", index=True) # planned, in_progress, completed, late, blocked, cancelled
    completion_evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

class ExecutionBaseline(Base):
    __tablename__ = "execution_baselines"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    scope_summary: Mapped[str] = mapped_column(Text, nullable=False)
    timeline_summary: Mapped[str] = mapped_column(Text, nullable=False)
    budget: Mapped[float] = mapped_column(Float, nullable=False)
    expected_outcomes_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class ExecutionVariance(Base):
    __tablename__ = "execution_variances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    variance_type: Mapped[str] = mapped_column(String(50), nullable=False) # scope, schedule, cost, capacity, dependency, quality, benefit
    baseline: Mapped[str] = mapped_column(Text, nullable=False)
    actual: Mapped[str] = mapped_column(Text, nullable=False)
    forecast: Mapped[str] = mapped_column(Text, nullable=False)
    delta: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True) # low, medium, high, critical

class AcceptanceRecord(Base):
    __tablename__ = "acceptance_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deliverable_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    criteria: Mapped[str] = mapped_column(Text, nullable=False)
    evidence: Mapped[str] = mapped_column(Text, nullable=False)
    reviewer: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending") # pending, accepted, rejected, conditional
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ExecutionGate(Base):
    __tablename__ = "execution_gates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    gate_type: Mapped[str] = mapped_column(String(50), nullable=False) # approval, security, quality, budget, compliance, business
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, passed, failed, waived
    waiver_actor: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    waiver_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

class ExecutionGateEvidence(Base):
    __tablename__ = "execution_gate_evidences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gate_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ExecutionChangeRequest(Base):
    __tablename__ = "execution_change_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    change_type: Mapped[str] = mapped_column(String(50), nullable=False) # scope, timeline, budget, resource, dependency, quality
    requested_change: Mapped[str] = mapped_column(Text, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    impact_summary: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, approved, rejected
    requester: Mapped[str] = mapped_column(String(255), nullable=False)

class ExecutionForecast(Base):
    __tablename__ = "execution_forecasts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    forecast_completion_date: Mapped[str] = mapped_column(String(50), nullable=False)
    forecast_cost: Mapped[float] = mapped_column(Float, nullable=False)
    forecast_benefit: Mapped[float] = mapped_column(Float, nullable=False)
    lower_bound: Mapped[float] = mapped_column(Float, nullable=False)
    upper_bound: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_pct: Mapped[float] = mapped_column(Float, nullable=False, default=88.5)

class BenefitRisk(Base):
    __tablename__ = "benefit_risks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    benefit_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_type: Mapped[str] = mapped_column(String(50), nullable=False) # measurement, dependency, adoption, execution, assumption, capacity
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")

class BenefitAttribution(Base):
    __tablename__ = "benefit_attributions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    benefit_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    attribution_type: Mapped[str] = mapped_column(String(50), nullable=False, default="direct") # direct, correlated, inferred
    contribution_pct: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    evidence_summary: Mapped[str] = mapped_column(Text, nullable=False)

class KPI(Base):
    __tablename__ = "kpis_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    definition: Mapped[Text] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # draft, active, paused, retired
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # strategic, financial, operational, customer, quality, risk, capacity, delivery, security, AI, workforce, innovation
    unit: Mapped[str] = mapped_column(String(50), nullable=False, default="USD")
    direction: Mapped[str] = mapped_column(String(50), nullable=False, default="higher_is_better") # higher_is_better, lower_is_better, target_range, binary, informational
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class KPIVersion(Base):
    __tablename__ = "kpi_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kpi_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class KPIDataSource(Base):
    __tablename__ = "kpi_data_sources"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kpi_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False) # database, event_stream, integration, manual_entry, external_source, derived_metric
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    source_version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0")
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class KPITarget(Base):
    __tablename__ = "kpi_targets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kpi_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    effective_from: Mapped[str] = mapped_column(String(50), nullable=False)
    effective_to: Mapped[str] = mapped_column(String(50), nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    approval_reference: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

class KPITargetVersion(Base):
    __tablename__ = "kpi_target_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class KPIMeasurement(Base):
    __tablename__ = "kpi_measurements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kpi_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    period_start: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    period_end: Mapped[str] = mapped_column(String(50), nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    quality: Mapped[str] = mapped_column(String(50), nullable=False, default="verified") # verified, estimated, partial, stale, missing, invalid
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=95.0)

class KPIVariance(Base):
    __tablename__ = "kpi_variances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kpi_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    actual: Mapped[float] = mapped_column(Float, nullable=False)
    target: Mapped[float] = mapped_column(Float, nullable=False)
    baseline: Mapped[float] = mapped_column(Float, nullable=False)
    delta: Mapped[float] = mapped_column(Float, nullable=False)
    percentage_delta: Mapped[float] = mapped_column(Float, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="on_track", index=True) # on_track, watch, at_risk, off_track, unknown

class KPIAlert(Base):
    __tablename__ = "kpi_alerts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kpi_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    alert_type: Mapped[str] = mapped_column(String(50), nullable=False) # threshold, trend, anomaly, forecast, data_quality, target_miss
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, acknowledged, resolved
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class KPIDriver(Base):
    __tablename__ = "kpi_drivers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kpi_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    driver_name: Mapped[str] = mapped_column(String(255), nullable=False)
    driver_type: Mapped[str] = mapped_column(String(50), nullable=False)
    association_type: Mapped[str] = mapped_column(String(50), nullable=False, default="correlated") # correlated, inferred
    confidence_pct: Mapped[float] = mapped_column(Float, nullable=False, default=85.0)
    evidence_summary: Mapped[str] = mapped_column(Text, nullable=False)

class KPIForecast(Base):
    __tablename__ = "kpi_forecasts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kpi_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    forecast_value: Mapped[float] = mapped_column(Float, nullable=False)
    lower_bound: Mapped[float] = mapped_column(Float, nullable=False)
    upper_bound: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_pct: Mapped[float] = mapped_column(Float, nullable=False, default=90.0)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class KPIScorecard(Base):
    __tablename__ = "kpi_scorecards"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scorecard_type: Mapped[str] = mapped_column(String(50), nullable=False) # strategy, portfolio, program, team, workspace
    kpi_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class KPIReview(Base):
    __tablename__ = "kpi_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kpi_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    review_cadence: Mapped[str] = mapped_column(String(50), nullable=False, default="monthly") # monthly, quarterly, annual, custom
    progress_summary: Mapped[str] = mapped_column(Text, nullable=False)
    quality_summary: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="completed")

class KPIDataQualityIssue(Base):
    __tablename__ = "kpi_data_quality_issues"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kpi_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    issue_type: Mapped[str] = mapped_column(String(50), nullable=False) # missing, stale, estimated, invalid
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="warning")

class KPIReconciliation(Base):
    __tablename__ = "kpi_reconciliations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kpi_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_a: Mapped[str] = mapped_column(String(255), nullable=False)
    value_a: Mapped[float] = mapped_column(Float, nullable=False)
    source_b: Mapped[str] = mapped_column(String(255), nullable=False)
    value_b: Mapped[float] = mapped_column(Float, nullable=False)
    conflict_status: Mapped[str] = mapped_column(String(50), nullable=False, default="conflicting")

class KPIReplacement(Base):
    __tablename__ = "kpi_replacements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    old_kpi_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    replaced_by_kpi_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    replaced_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Forecast(Base):
    __tablename__ = "forecasts_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # kpi, benefit, initiative, milestone, portfolio, capacity, cost, risk, outcome, mission
    entity_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    metric_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="medium_term") # short_term, medium_term, long_term, custom
    method: Mapped[str] = mapped_column(String(100), nullable=False, default="ensemble_timeseries")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # draft, active, completed, superseded, invalidated
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ForecastPoint(Base):
    __tablename__ = "forecast_points"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forecast_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    lower_bound: Mapped[float] = mapped_column(Float, nullable=False)
    upper_bound: Mapped[float] = mapped_column(Float, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=90.0)

class ForecastInput(Base):
    __tablename__ = "forecast_inputs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forecast_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    input_type: Mapped[str] = mapped_column(String(50), nullable=False) # historical_series, current_state, external_signal, business_event, dependency, assumption, scenario
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quality: Mapped[str] = mapped_column(String(50), nullable=False, default="verified") # verified, estimated, stale, missing, conflicted

class ForecastDriver(Base):
    __tablename__ = "forecast_drivers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forecast_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    factor_name: Mapped[str] = mapped_column(String(255), nullable=False)
    direction: Mapped[str] = mapped_column(String(50), nullable=False) # positive, negative, neutral
    magnitude: Mapped[float] = mapped_column(Float, nullable=False)
    evidence: Mapped[str] = mapped_column(Text, nullable=False)
    confidence_pct: Mapped[float] = mapped_column(Float, nullable=False, default=85.0)
    association_type: Mapped[str] = mapped_column(String(50), nullable=False, default="correlated") # correlated, inferred

class ForecastVersion(Base):
    __tablename__ = "forecast_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forecast_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    previous_forecast_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    revision_reason: Mapped[str] = mapped_column(Text, nullable=False)
    snapshot_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ForecastAccuracy(Base):
    __tablename__ = "forecast_accuracies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forecast_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    actual_value: Mapped[float] = mapped_column(Float, nullable=False)
    absolute_error: Mapped[float] = mapped_column(Float, nullable=False)
    percentage_error: Mapped[float] = mapped_column(Float, nullable=False)
    interval_coverage: Mapped[float] = mapped_column(Float, nullable=False, default=95.0)
    calibration: Mapped[float] = mapped_column(Float, nullable=False, default=92.0)

class ForecastModelDrift(Base):
    __tablename__ = "forecast_model_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    baseline_accuracy: Mapped[float] = mapped_column(Float, nullable=False)
    current_accuracy: Mapped[float] = mapped_column(Float, nullable=False)
    drift_magnitude: Mapped[float] = mapped_column(Float, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=90.0)

class ForecastBacktest(Base):
    __tablename__ = "forecast_backtests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    mae: Mapped[float] = mapped_column(Float, nullable=False)
    rmse: Mapped[float] = mapped_column(Float, nullable=False)
    mape: Mapped[float] = mapped_column(Float, nullable=False)
    interval_coverage: Mapped[float] = mapped_column(Float, nullable=False)
    bias: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    calibration: Mapped[float] = mapped_column(Float, nullable=False)

class PredictiveAlert(Base):
    __tablename__ = "predictive_alerts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forecast_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    alert_type: Mapped[str] = mapped_column(String(50), nullable=False) # target_miss, deadline_miss, capacity_shortage, cost_overrun, risk_escalation, benefit_shortfall, anomaly, dependency_failure
    predicted_window: Mapped[str] = mapped_column(String(100), nullable=False) # e.g., "Likely within 14-21 days"
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high") # high, medium, low, unknown
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class PredictiveRiskSignal(Base):
    __tablename__ = "predictive_risk_signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forecast_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_id: Mapped[str] = mapped_column(String(255), nullable=False)
    affected_entity_id: Mapped[str] = mapped_column(String(255), nullable=False)
    probability_range: Mapped[str] = mapped_column(String(50), nullable=False) # e.g. "60-75%"
    impact: Mapped[str] = mapped_column(String(50), nullable=False, default="high") # low, medium, high, critical
    evidence: Mapped[str] = mapped_column(Text, nullable=False)

class PredictiveRecommendation(Base):
    __tablename__ = "predictive_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    options_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    expected_effect: Mapped[str] = mapped_column(Text, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    confidence_pct: Mapped[float] = mapped_column(Float, nullable=False, default=88.0)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="advisory")

class CapacityForecast(Base):
    __tablename__ = "capacity_forecasts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capacity_type: Mapped[str] = mapped_column(String(50), nullable=False) # human, agent, compute, model, integration
    demand_value: Mapped[float] = mapped_column(Float, nullable=False)
    capacity_value: Mapped[float] = mapped_column(Float, nullable=False)
    gap: Mapped[float] = mapped_column(Float, nullable=False)
    horizon: Mapped[str] = mapped_column(String(50), nullable=False)

class DemandForecast(Base):
    __tablename__ = "demand_forecasts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    demand_type: Mapped[str] = mapped_column(String(50), nullable=False) # work, mission, agent, compute
    forecast_demand: Mapped[float] = mapped_column(Float, nullable=False)
    horizon: Mapped[str] = mapped_column(String(50), nullable=False)

class ForecastScenario(Base):
    __tablename__ = "forecast_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forecast_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    scenario_name: Mapped[str] = mapped_column(String(50), nullable=False) # baseline, upside, downside, stress
    scenario_params_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    output_distribution_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class ForecastRevision(Base):
    __tablename__ = "forecast_revisions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forecast_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    new_inputs_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class OptimizationProblem(Base):
    __tablename__ = "optimization_problems_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    objective_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # maximize_outcome, minimize_cost, minimize_risk, minimize_delay, maximize_capacity_efficiency, maximize_utility, custom
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="configured", index=True) # draft, configured, simulating, ready_for_review, approved, executing, completed, cancelled
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class OptimizationObjective(Base):
    __tablename__ = "optimization_objectives"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    problem_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    metric: Mapped[str] = mapped_column(String(255), nullable=False)
    direction: Mapped[str] = mapped_column(String(50), nullable=False, default="maximize") # maximize, minimize
    weight: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    source: Mapped[str] = mapped_column(String(255), nullable=False)

class DecisionVariable(Base):
    __tablename__ = "decision_variables_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    problem_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    variable_type: Mapped[str] = mapped_column(String(50), nullable=False) # continuous, integer, boolean, categorical
    minimum: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    maximum: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    allowed_values_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class OptimizationConstraint(Base):
    __tablename__ = "optimization_constraints_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    problem_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    constraint_type: Mapped[str] = mapped_column(String(50), nullable=False) # budget, capacity, policy, deadline, dependency, security, resource, technical, business
    is_hard: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    expression: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    freshness: Mapped[str] = mapped_column(String(50), nullable=False, default="fresh") # fresh, stale

class OptimizationOption(Base):
    __tablename__ = "optimization_options_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    problem_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    variables_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    constraints_satisfied: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    expected_outcome: Mapped[float] = mapped_column(Float, nullable=False)
    expected_cost: Mapped[float] = mapped_column(Float, nullable=False)
    expected_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=90.0)

class OptimizationScenario(Base):
    __tablename__ = "optimization_scenarios_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    option_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    outcome: Mapped[float] = mapped_column(Float, nullable=False)
    cost: Mapped[float] = mapped_column(Float, nullable=False)
    risk: Mapped[str] = mapped_column(String(50), nullable=False)
    capacity: Mapped[float] = mapped_column(Float, nullable=False)
    timeline: Mapped[str] = mapped_column(String(50), nullable=False)
    uncertainty: Mapped[float] = mapped_column(Float, nullable=False, default=10.0)

class RobustnessAnalysis(Base):
    __tablename__ = "robustness_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    option_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    demand_change: Mapped[str] = mapped_column(String(100), nullable=False)
    cost_change: Mapped[str] = mapped_column(String(100), nullable=False)
    capacity_change: Mapped[str] = mapped_column(String(100), nullable=False)
    dependency_failure_impact: Mapped[str] = mapped_column(Text, nullable=False)
    robustness_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)

class SensitivityAnalysis(Base):
    __tablename__ = "sensitivity_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    option_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    variable_name: Mapped[str] = mapped_column(String(255), nullable=False)
    impact_direction: Mapped[str] = mapped_column(String(50), nullable=False) # positive, negative
    estimated_magnitude: Mapped[float] = mapped_column(Float, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=88.0)

class OptimizationTradeoff(Base):
    __tablename__ = "optimization_tradeoffs_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    problem_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    option_a_id: Mapped[str] = mapped_column(String(255), nullable=False)
    option_b_id: Mapped[str] = mapped_column(String(255), nullable=False)
    comparison_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    pareto_frontier_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class PrescriptiveRecommendation(Base):
    __tablename__ = "prescriptive_recommendations_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    problem_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    recommended_option_id: Mapped[str] = mapped_column(String(255), nullable=False)
    alternatives_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    objective_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    constraints_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence: Mapped[Text] = mapped_column(Text, nullable=False)
    expected_impact: Mapped[Text] = mapped_column(Text, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    confidence_pct: Mapped[float] = mapped_column(Float, nullable=False, default=92.0)
    robustness_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="ready_for_review", index=True) # draft, ready_for_review, approved, rejected, superseded, expired

class OptimizationActionPlan(Base):
    __tablename__ = "optimization_action_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recommendation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    actions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    milestones_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    rollback_plan: Mapped[Text] = mapped_column(Text, nullable=False)
    execution_mode: Mapped[str] = mapped_column(String(50), nullable=False, default="approval_gated") # advisory, approval_gated, policy_authorized

class OptimizationAction(Base):
    __tablename__ = "optimization_actions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action_plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String(100), nullable=False)
    target_system: Mapped[str] = mapped_column(String(100), nullable=False)
    payload_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")

class OptimizationPerformance(Base):
    __tablename__ = "optimization_performances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recommendation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expected_outcome: Mapped[float] = mapped_column(Float, nullable=False)
    actual_outcome: Mapped[float] = mapped_column(Float, nullable=False)
    expected_cost: Mapped[float] = mapped_column(Float, nullable=False)
    actual_cost: Mapped[float] = mapped_column(Float, nullable=False)
    benefit_accuracy: Mapped[float] = mapped_column(Float, nullable=False, default=94.0)
    cost_accuracy: Mapped[float] = mapped_column(Float, nullable=False, default=96.0)
    forecast_error: Mapped[float] = mapped_column(Float, nullable=False, default=4.5)

class OptimizationAlert(Base):
    __tablename__ = "optimization_alerts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    problem_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    alert_type: Mapped[str] = mapped_column(String(50), nullable=False) # recommendation_invalidated, constraint_changed, better_option_found, risk_increased, expected_benefit_changed, cost_changed
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True)

class OptimizationVersion(Base):
    __tablename__ = "optimization_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    problem_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ControlLoop(Base):
    __tablename__ = "control_loops_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    target_entity_type: Mapped[str] = mapped_column(String(100), nullable=False) # mission, kpi, capacity, cost, infrastructure, workflow
    target_entity_id: Mapped[str] = mapped_column(String(255), nullable=False)
    mode: Mapped[str] = mapped_column(String(50), nullable=False, default="monitor_only") # monitor_only, recommendation, approval_gated, policy_authorized
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # draft, active, paused, degraded, suspended, completed, retired
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ControlObjective(Base):
    __tablename__ = "control_objectives_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loop_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    metric: Mapped[str] = mapped_column(String(255), nullable=False)
    target: Mapped[float] = mapped_column(Float, nullable=False)
    acceptable_range: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. [90.0, 100.0]
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    source: Mapped[str] = mapped_column(String(255), nullable=False)

class ControlSignal(Base):
    __tablename__ = "control_signals_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loop_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    signal_type: Mapped[str] = mapped_column(String(50), nullable=False) # kpi, forecast, risk, capacity, cost, benefit, dependency, policy, execution
    value: Mapped[float] = mapped_column(Float, nullable=False)
    signal_quality: Mapped[str] = mapped_column(String(50), nullable=False, default="verified") # verified, estimated, stale, missing, conflicted
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high") # high, medium, low, unknown
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    freshness: Mapped[str] = mapped_column(String(50), nullable=False, default="fresh") # fresh, stale

class ControlStateSnapshot(Base):
    __tablename__ = "control_state_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loop_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    current_state_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    target_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    constraints_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    risks_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    active_decisions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    active_actions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class ControlStateChange(Base):
    __tablename__ = "control_state_changes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loop_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    change_type: Mapped[str] = mapped_column(String(50), nullable=False) # target_changed, metric_changed, risk_changed, constraint_changed, dependency_changed, capacity_changed, cost_changed, benefit_changed, execution_changed
    delta_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DecisionValidityAssessment(Base):
    __tablename__ = "decision_validity_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    validity_status: Mapped[str] = mapped_column(String(50), nullable=False, default="valid") # valid, uncertain, degraded, invalid
    validity_factors_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    assessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DecisionReassessment(Base):
    __tablename__ = "decision_reassessments_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger_type: Mapped[str] = mapped_column(String(50), nullable=False) # periodic, threshold, event, forecast_change, risk_change, constraint_change, outcome_change
    evidence: Mapped[Text] = mapped_column(Text, nullable=False)
    affected_decision_id: Mapped[str] = mapped_column(String(255), nullable=False)
    new_conditions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    recommended_next_step: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True) # pending, in_review, resolved

class ControlResponse(Base):
    __tablename__ = "control_responses_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loop_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    response_type: Mapped[str] = mapped_column(String(50), nullable=False) # continue, monitor, reassess, escalate, simulate, recommend, pause, rollback
    payload_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="proposed", index=True) # proposed, approved, executed, rejected, blocked
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")

class ControlGuardrail(Base):
    __tablename__ = "control_guardrails_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loop_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    guardrail_type: Mapped[str] = mapped_column(String(50), nullable=False) # max_cost, max_risk, min_quality, max_delay, max_capacity, data_freshness, confidence, policy
    threshold: Mapped[float] = mapped_column(Float, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="warning") # info, warning, high, critical
    action: Mapped[str] = mapped_column(String(100), nullable=False) # alert, recommend, escalate, pause, require_approval
    approval_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    policy_reference: Mapped[str] = mapped_column(String(255), nullable=False)

class GuardrailBreach(Base):
    __tablename__ = "guardrail_breaches_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guardrail_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    observed_value: Mapped[float] = mapped_column(Float, nullable=False)
    threshold: Mapped[float] = mapped_column(Float, nullable=False)
    evidence: Mapped[Text] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open")

class ActionOutcomeObservation(Base):
    __tablename__ = "action_outcome_observations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expected_val: Mapped[float] = mapped_column(Float, nullable=False)
    actual_val: Mapped[float] = mapped_column(Float, nullable=False)
    variance: Mapped[float] = mapped_column(Float, nullable=False)
    outcome_class: Mapped[str] = mapped_column(String(50), nullable=False, default="success") # success, partial_success, no_effect, negative_effect, unknown
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DecisionRegretAnalysis(Base):
    __tablename__ = "decision_regret_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    selected_option: Mapped[str] = mapped_column(String(255), nullable=False)
    alternative_options_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    actual_outcome: Mapped[float] = mapped_column(Float, nullable=False)
    regret_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.05)
    counterfactual_label: Mapped[str] = mapped_column(String(50), nullable=False, default="simulated") # simulated, estimated, unknown

class ControlPerformance(Base):
    __tablename__ = "control_performances_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loop_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    false_alerts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    missed_alerts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    successful_interventions: Mapped[int] = mapped_column(Integer, nullable=False, default=12)
    unnecessary_interventions: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    reassessment_frequency: Mapped[float] = mapped_column(Float, nullable=False, default=1.2) # reassessments / week
    health_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.97)

class ControlLoopHealth(Base):
    __tablename__ = "control_loop_healths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loop_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    signal_freshness: Mapped[float] = mapped_column(Float, nullable=False, default=0.98)
    decision_validity: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    guardrail_health: Mapped[float] = mapped_column(Float, nullable=False, default=0.99)
    action_success: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    outcome_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.97)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="healthy")

class ControlLoopVersion(Base):
    __tablename__ = "control_loop_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loop_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CriticalCapability(Base):
    __tablename__ = "critical_capabilities_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    criticality: Mapped[str] = mapped_column(String(50), nullable=False, default="critical", index=True) # low, medium, high, critical
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, degraded, suspended, retired
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class BusinessImpactProfile(Base):
    __tablename__ = "business_impact_profiles_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    financial_impact: Mapped[str] = mapped_column(String(100), nullable=False, default="high")
    operational_impact: Mapped[str] = mapped_column(String(100), nullable=False, default="critical")
    customer_impact: Mapped[str] = mapped_column(String(100), nullable=False, default="high")
    regulatory_impact: Mapped[str] = mapped_column(String(100), nullable=False, default="medium")
    reputational_impact: Mapped[str] = mapped_column(String(100), nullable=False, default="high")
    strategic_impact: Mapped[str] = mapped_column(String(100), nullable=False, default="high")
    tolerable_downtime: Mapped[str] = mapped_column(String(100), nullable=False, default="4 hours")
    maximum_tolerable_disruption: Mapped[str] = mapped_column(String(100), nullable=False, default="12 hours")
    recovery_objective: Mapped[str] = mapped_column(String(100), nullable=False, default="1 hour") # RTO
    data_recovery_objective: Mapped[str] = mapped_column(String(100), nullable=False, default="15 minutes") # RPO

class ResilienceDependencyRisk(Base):
    __tablename__ = "resilience_dependency_risks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dependency_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dependency_type: Mapped[str] = mapped_column(String(100), nullable=False) # application, service, integration, data, person, vendor, agent, infrastructure, process
    criticality: Mapped[str] = mapped_column(String(50), nullable=False, default="required") # required, important, optional
    is_single_point_of_failure: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    has_fallback: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    primary_fallback: Mapped[str] = mapped_column(String(255), nullable=True)

class ResilienceVulnerability(Base):
    __tablename__ = "resilience_vulnerabilities_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dependency_id: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high") # low, medium, high, critical
    evidence: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open")

class ResilienceGap(Base):
    __tablename__ = "resilience_gaps_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    gap_type: Mapped[str] = mapped_column(String(50), nullable=False) # coverage, redundancy, capacity, recovery, testing, dependency, data, governance
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True) # low, medium, high, critical
    evidence: Mapped[Text] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open")

class FailureScenario(Base):
    __tablename__ = "failure_scenarios_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    scenario_type: Mapped[str] = mapped_column(String(100), nullable=False) # service_failure, dependency_failure, vendor_outage, data_loss, security_incident, capacity_exhaustion, regional_outage, agent_failure, integration_failure, human_error, process_failure
    trigger: Mapped[str] = mapped_column(String(255), nullable=False)
    probability_range: Mapped[str] = mapped_column(String(100), nullable=False, default="[0.05, 0.15]")
    impact_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    assumptions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    cascade_depth: Mapped[str] = mapped_column(String(50), nullable=False, default="multi-hop") # direct, indirect, multi-hop
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class ResilienceOption(Base):
    __tablename__ = "resilience_options_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    option_type: Mapped[str] = mapped_column(String(100), nullable=False) # redundancy, fallback, capacity_buffer, failover, manual_process, vendor_alternative, data_replication, architecture_change, process_change
    cost_estimate: Mapped[float] = mapped_column(Float, nullable=False)
    recovery_time_reduction: Mapped[str] = mapped_column(String(100), nullable=False)
    risk_reduction_pct: Mapped[float] = mapped_column(Float, nullable=False, default=75.0)
    complexity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    coverage_pct: Mapped[float] = mapped_column(Float, nullable=False, default=90.0)

class ContinuityPlan(Base):
    __tablename__ = "continuity_plans_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    triggers_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    actions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    owners_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    communications_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    recovery_objectives_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    rollback_plan_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # draft, active, stale, testing, validated, retired
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    last_validated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    next_due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class RecoveryProcedure(Base):
    __tablename__ = "recovery_procedures_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    steps_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    preconditions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    expected_duration_min: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    verification_criteria: Mapped[Text] = mapped_column(Text, nullable=False)

class RecoveryOutcome(Base):
    __tablename__ = "recovery_outcomes_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    procedure_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    execution_id: Mapped[str] = mapped_column(String(255), nullable=False)
    outcome_class: Mapped[str] = mapped_column(String(50), nullable=False, default="successful") # successful, partial, failed, unknown
    expected_duration_min: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    actual_duration_min: Mapped[int] = mapped_column(Integer, nullable=False, default=28)
    variance_min: Mapped[int] = mapped_column(Integer, nullable=False, default=-2)
    verification_details: Mapped[Text] = mapped_column(Text, nullable=False)

class ResilienceTest(Base):
    __tablename__ = "resilience_tests_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    test_type: Mapped[str] = mapped_column(String(50), nullable=False) # tabletop, simulation, technical, failover, restore, recovery
    frequency: Mapped[str] = mapped_column(String(50), nullable=False, default="quarterly") # monthly, quarterly, annual, custom
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    result: Mapped[str] = mapped_column(String(50), nullable=False, default="passed") # passed, partial, failed, inconclusive
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    next_due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class RecoveryReadinessAssessment(Base):
    __tablename__ = "recovery_readiness_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    readiness_status: Mapped[str] = mapped_column(String(50), nullable=False, default="ready") # ready, partially_ready, not_ready, unknown
    assessment_factors_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    assessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ResiliencePosture(Base):
    __tablename__ = "resilience_postures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dependency_dimension: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    recovery_dimension: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    testing_dimension: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    capacity_dimension: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    data_dimension: Mapped[float] = mapped_column(Float, nullable=False, default=0.98)
    governance_dimension: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    overall_readiness: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)

class ResilienceLesson(Base):
    __tablename__ = "resilience_lessons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    observation: Mapped[Text] = mapped_column(Text, nullable=False)
    candidate_root_cause: Mapped[Text] = mapped_column(Text, nullable=False)
    impact_observed: Mapped[Text] = mapped_column(Text, nullable=False)
    recommended_improvement: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class ResilienceImprovement(Base):
    __tablename__ = "resilience_improvements_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gap_id: Mapped[str] = mapped_column(String(255), nullable=True)
    lesson_id: Mapped[str] = mapped_column(String(255), nullable=True)
    initiative_name: Mapped[str] = mapped_column(String(255), nullable=False)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=True)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="in_progress", index=True) # planned, in_progress, completed, verified
    verified_risk_reduction_pct: Mapped[float] = mapped_column(Float, nullable=False, default=80.0)

class ResilienceCommunicationPlan(Base):
    __tablename__ = "resilience_communication_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    audience: Mapped[str] = mapped_column(String(100), nullable=False)
    channel: Mapped[str] = mapped_column(String(100), nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    trigger: Mapped[str] = mapped_column(String(255), nullable=False)
    message_template: Mapped[Text] = mapped_column(Text, nullable=False)

class VendorResilienceProfile(Base):
    __tablename__ = "vendor_resilience_profiles_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vendor_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    vendor_name: Mapped[str] = mapped_column(String(255), nullable=False)
    criticality: Mapped[str] = mapped_column(String(50), nullable=False, default="critical")
    concentration_risk_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    fallback_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    recovery_evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class DataResilienceProfile(Base):
    __tablename__ = "data_resilience_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_asset_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    backup_status: Mapped[str] = mapped_column(String(50), nullable=False, default="healthy")
    replication_status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    last_restore_test_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    rpo_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=15)
    rto_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=60)

class AIResilienceProfile(Base):
    __tablename__ = "ai_resilience_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    provider_name: Mapped[str] = mapped_column(String(255), nullable=False)
    fallback_model_id: Mapped[str] = mapped_column(String(255), nullable=True)
    fallback_agent_id: Mapped[str] = mapped_column(String(255), nullable=True)
    human_escalation_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    quality_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.98)

class Crisis(Base):
    __tablename__ = "crises_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="declared", index=True) # detected, assessing, declared, active, stabilizing, recovering, resolved, closed, cancelled
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="SEV1", index=True) # SEV4, SEV3, SEV2, SEV1, CRITICAL
    declared_by: Mapped[str] = mapped_column(String(255), nullable=False)
    declared_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    commander_id: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CrisisDeclaration(Base):
    __tablename__ = "crisis_declarations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger: Mapped[str] = mapped_column(String(255), nullable=False)
    evidence: Mapped[Text] = mapped_column(Text, nullable=False)
    criteria: Mapped[Text] = mapped_column(Text, nullable=False)
    authorized_actor: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CrisisSignal(Base):
    __tablename__ = "crisis_signals_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    signal_type: Mapped[str] = mapped_column(String(100), nullable=False) # service_failure, security_event, vendor_outage, data_issue, capacity_failure, financial_event, operational_failure, dependency_failure, reputational_event, regulatory_event, external_event
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high") # high, medium, low, unknown
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    source_version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0")

class CrisisImpactAssessment(Base):
    __tablename__ = "crisis_impact_assessments_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    capabilities_impact_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    services_impact_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    customers_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    operations_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    financials_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    data_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    security_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    regulatory_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    reputation_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    impact_status: Mapped[str] = mapped_column(String(50), nullable=False, default="confirmed") # unknown, suspected, confirmed, resolved
    evidence: Mapped[Text] = mapped_column(Text, nullable=False)

class CrisisCascade(Base):
    __tablename__ = "crisis_cascades"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_node: Mapped[str] = mapped_column(String(255), nullable=False)
    affected_node: Mapped[str] = mapped_column(String(255), nullable=False)
    relationship: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class CrisisCommand(Base):
    __tablename__ = "crisis_commands_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    incident_commander: Mapped[str] = mapped_column(String(255), nullable=False)
    operations_lead: Mapped[str] = mapped_column(String(255), nullable=False)
    technical_lead: Mapped[str] = mapped_column(String(255), nullable=False)
    security_lead: Mapped[str] = mapped_column(String(255), nullable=False)
    communications_lead: Mapped[str] = mapped_column(String(255), nullable=False)
    business_lead: Mapped[str] = mapped_column(String(255), nullable=False)
    recovery_lead: Mapped[str] = mapped_column(String(255), nullable=False)

class CrisisCommandAssignment(Base):
    __tablename__ = "crisis_command_assignments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    command_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    actor: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False) # incident_commander, operations_lead, technical_lead, security_lead, communications_lead, business_lead, recovery_lead
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    assigned_by: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")

class CrisisResponsePlan(Base):
    __tablename__ = "crisis_response_plans_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    objectives_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    actions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    owners_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    decision_points_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    communications_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    rollback_plan_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class CrisisResponseOption(Base):
    __tablename__ = "crisis_response_options_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    expected_impact: Mapped[Text] = mapped_column(Text, nullable=False)
    cost_estimate: Mapped[float] = mapped_column(Float, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    recovery_time_min: Mapped[int] = mapped_column(Integer, nullable=False, default=45)
    dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class CrisisCommunication(Base):
    __tablename__ = "crisis_communications_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    audience: Mapped[str] = mapped_column(String(100), nullable=False) # internal, customer, vendor, executive, regulatory, public
    message: Mapped[Text] = mapped_column(Text, nullable=False)
    channel: Mapped[str] = mapped_column(String(100), nullable=False)
    sender: Mapped[str] = mapped_column(String(255), nullable=False)
    approval_status: Mapped[str] = mapped_column(String(50), nullable=False, default="approved", index=True) # draft, pending_approval, approved, sent, failed, cancelled
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CrisisTimelineEvent(Base):
    __tablename__ = "crisis_timeline_events_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    actor: Mapped[str] = mapped_column(String(255), nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence: Mapped[Text] = mapped_column(Text, nullable=False)

class StabilizationAssessment(Base):
    __tablename__ = "stabilization_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    is_contained: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    new_damage_occurring: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    capabilities_recovering: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    assessment_details: Mapped[Text] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CrisisResolution(Base):
    __tablename__ = "crisis_resolutions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    resolution_criteria: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence: Mapped[Text] = mapped_column(Text, nullable=False)
    authorized_resolver: Mapped[str] = mapped_column(String(255), nullable=False)
    resolved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AfterActionReview(Base):
    __tablename__ = "after_action_reviews_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    what_happened: Mapped[Text] = mapped_column(Text, nullable=False)
    what_worked: Mapped[Text] = mapped_column(Text, nullable=False)
    what_failed: Mapped[Text] = mapped_column(Text, nullable=False)
    unexpected_behavior: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    lessons_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    improvements_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class CrisisLesson(Base):
    __tablename__ = "crisis_lessons_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    incident_id: Mapped[str] = mapped_column(String(255), nullable=True)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=True)
    action_id: Mapped[str] = mapped_column(String(255), nullable=True)
    outcome: Mapped[str] = mapped_column(String(100), nullable=False)
    resilience_gap_id: Mapped[str] = mapped_column(String(255), nullable=True)
    lesson_text: Mapped[Text] = mapped_column(Text, nullable=False)

class CrisisImprovement(Base):
    __tablename__ = "crisis_improvements_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    initiative_name: Mapped[str] = mapped_column(String(255), nullable=False)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=True)
    control_loop_id: Mapped[str] = mapped_column(String(255), nullable=True)
    resilience_improvement_id: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="in_progress", index=True) # planned, in_progress, completed, verified

class CrisisDrill(Base):
    __tablename__ = "crisis_drills_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scenario_type: Mapped[str] = mapped_column(String(100), nullable=False)
    participants_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    objectives_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    results_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    gaps_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="passed") # passed, partial, failed, inconclusive
    next_due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class CrisisReadinessAssessment(Base):
    __tablename__ = "crisis_readiness_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    command_readiness: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    plans_readiness: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    communications_readiness: Mapped[float] = mapped_column(Float, nullable=False, default=0.98)
    recovery_readiness: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    readiness_status: Mapped[str] = mapped_column(String(50), nullable=False, default="ready") # ready, partially_ready, not_ready, unknown

class CrisisEscalation(Base):
    __tablename__ = "crisis_escalations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    previous_severity: Mapped[str] = mapped_column(String(50), nullable=False)
    new_severity: Mapped[str] = mapped_column(String(50), nullable=False)
    trigger_reason: Mapped[Text] = mapped_column(Text, nullable=False)
    authorized_by: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CrisisRelationship(Base):
    __tablename__ = "crisis_relationships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    primary_crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    related_crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    relationship_type: Mapped[str] = mapped_column(String(50), nullable=False) # duplicate, related, caused_by, escalation_of, dependency_of

class CrisisMetrics(Base):
    __tablename__ = "crisis_metrics_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crisis_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    time_to_detect_min: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    time_to_declare_min: Mapped[int] = mapped_column(Integer, nullable=False, default=12)
    time_to_stabilize_min: Mapped[int] = mapped_column(Integer, nullable=False, default=48)
    time_to_recover_min: Mapped[int] = mapped_column(Integer, nullable=False, default=95)
    time_to_verify_min: Mapped[int] = mapped_column(Integer, nullable=False, default=115)

class ThreatSignal(Base):
    __tablename__ = "threat_signals_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(100), nullable=False)
    source_id: Mapped[str] = mapped_column(String(255), nullable=False)
    signal_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # availability_change, capacity_change, cost_change, risk_change, dependency_change, vendor_change, security_signal, data_quality_change, policy_change, execution_anomaly, behavioral_pattern, external_signal
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    quality: Mapped[str] = mapped_column(String(50), nullable=False, default="verified") # verified, estimated, stale, missing, conflicted, unverified
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ThreatSignalNormalization(Base):
    __tablename__ = "threat_signal_normalizations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    normalized_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    entity_id: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    source_provenance: Mapped[Text] = mapped_column(Text, nullable=False)

class WeakSignal(Base):
    __tablename__ = "weak_signals_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    novelty_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    persistence_status: Mapped[str] = mapped_column(String(50), nullable=False, default="persists") # appears_once, repeats, persists, accelerates
    signal_velocity: Mapped[str] = mapped_column(String(50), nullable=False, default="increasing_frequency") # increasing_frequency, increasing_magnitude, increasing_severity
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class ThreatCorrelation(Base):
    __tablename__ = "threat_correlations_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_signal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_signal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    connection_type: Mapped[str] = mapped_column(String(100), nullable=False) # entity, dependency, time, causal_hypothesis, shared_source, shared_outcome
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class ThreatPattern(Base):
    __tablename__ = "threat_patterns_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pattern_type: Mapped[str] = mapped_column(String(100), nullable=False) # cluster, sequence, trend, cascade, recurrence, co_occurrence
    entities_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    time_window: Mapped[str] = mapped_column(String(100), nullable=False, default="24 hours")
    strength: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class EmergingThreat(Base):
    __tablename__ = "emerging_threats_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    affected_capabilities_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    probability_range: Mapped[str] = mapped_column(String(50), nullable=False, default="40-60%")
    time_horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="days") # hours, days, weeks, months, unknown
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True) # low, medium, high, critical
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="emerging", index=True) # emerging, watch, escalating, contained, materialized, dismissed, expired

class ThreatEvidence(Base):
    __tablename__ = "threat_evidence_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    threat_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evidence_type: Mapped[str] = mapped_column(String(100), nullable=False) # signal, historical_pattern, dependency, forecast, incident, scenario, external_source
    quality: Mapped[str] = mapped_column(String(50), nullable=False, default="verified") # verified, estimated, simulated, unverified
    details: Mapped[Text] = mapped_column(Text, nullable=False)

class ThreatDriver(Base):
    __tablename__ = "threat_drivers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    threat_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    factor_name: Mapped[str] = mapped_column(String(255), nullable=False)
    direction: Mapped[str] = mapped_column(String(50), nullable=False, default="increasing")
    magnitude: Mapped[float] = mapped_column(Float, nullable=False, default=0.75)
    evidence: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class ThreatEscalationPath(Base):
    __tablename__ = "threat_escalation_paths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    threat_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    signal_id: Mapped[str] = mapped_column(String(255), nullable=True)
    risk_id: Mapped[str] = mapped_column(String(255), nullable=True)
    incident_id: Mapped[str] = mapped_column(String(255), nullable=True)
    crisis_id: Mapped[str] = mapped_column(String(255), nullable=True)
    escalation_conditions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class EarlyWarning(Base):
    __tablename__ = "early_warnings_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    threat_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger_reason: Mapped[Text] = mapped_column(Text, nullable=False)
    probability: Mapped[str] = mapped_column(String(50), nullable=False, default="40-60%")
    time_horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="days")
    impact_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True) # low, medium, high, critical
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="new", index=True) # new, acknowledged, investigating, mitigating, resolved, expired, false_positive

class PreventiveRecommendation(Base):
    __tablename__ = "preventive_recommendations_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    threat_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    options_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    expected_impact: Mapped[Text] = mapped_column(Text, nullable=False)
    cost_estimate: Mapped[float] = mapped_column(Float, nullable=False, default=5000.0)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class ThreatMitigation(Base):
    __tablename__ = "threat_mitigations_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    threat_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    action_name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    precondition: Mapped[Text] = mapped_column(Text, nullable=False)
    authorization_status: Mapped[str] = mapped_column(String(50), nullable=False, default="approved")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="executing", index=True) # planned, approved, executing, completed, failed, verified
    expected_risk_reduction_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    actual_risk_reduction_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)

class ThreatFalsePositive(Base):
    __tablename__ = "threat_false_positives"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    warning_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence: Mapped[Text] = mapped_column(Text, nullable=False)
    reviewer: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ThreatMiss(Base):
    __tablename__ = "threat_misses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    available_signals_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    missed_pattern: Mapped[Text] = mapped_column(Text, nullable=False)
    detection_gap: Mapped[Text] = mapped_column(Text, nullable=False)

class ThreatDetectionPerformance(Base):
    __tablename__ = "threat_detection_performances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    precision: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    recall: Mapped[float] = mapped_column(Float, nullable=False, default=0.91)
    false_positive_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.06)
    false_negative_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.09)
    lead_time_hours: Mapped[float] = mapped_column(Float, nullable=False, default=48.5)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class ThreatBlindSpot(Base):
    __tablename__ = "threat_blind_spots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain: Mapped[str] = mapped_column(String(255), nullable=False)
    missing_signals_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    impact_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    recommendation: Mapped[Text] = mapped_column(Text, nullable=False)

class ThreatCoverage(Base):
    __tablename__ = "threat_coverages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    monitoring_coverage_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    has_gap: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

class CompoundThreat(Base):
    __tablename__ = "compound_threats"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    threat_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    interaction_scenario: Mapped[Text] = mapped_column(Text, nullable=False)
    combined_impact: Mapped[Text] = mapped_column(Text, nullable=False)

class ThreatGraphSnapshot(Base):
    __tablename__ = "threat_graph_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nodes_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    edges_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    snapshot_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ThreatSourceProfile(Base):
    __tablename__ = "threat_source_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    license: Mapped[str] = mapped_column(String(100), nullable=False, default="commercial")
    confidence_rating: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    last_validated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ForesightProgram(Base):
    __tablename__ = "foresight_programs_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="5_year") # 1_year, 3_year, 5_year, 10_year, custom
    scope: Mapped[str] = mapped_column(String(255), nullable=False, default="global_enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # draft, active, review, completed, archived
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class FutureDriver(Base):
    __tablename__ = "future_drivers_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # technology, economic, regulatory, social, market, competitive, environmental, operational, organizational, geopolitical
    driver_name: Mapped[str] = mapped_column(String(255), nullable=False)
    strength: Mapped[str] = mapped_column(String(50), nullable=False, default="accelerating") # weak, emerging, established, accelerating, declining
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class StrategicTrend(Base):
    __tablename__ = "strategic_trends_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trend_name: Mapped[str] = mapped_column(String(255), nullable=False)
    direction: Mapped[str] = mapped_column(String(50), nullable=False, default="increasing", index=True) # increasing, stable, decreasing, volatile, uncertain
    velocity: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    persistence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class StructuralShift(Base):
    __tablename__ = "structural_shifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    shift_name: Mapped[str] = mapped_column(String(255), nullable=False)
    affected_domain: Mapped[str] = mapped_column(String(255), nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class StrategicUncertainty(Base):
    __tablename__ = "strategic_uncertainties_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    uncertainty_statement: Mapped[Text] = mapped_column(Text, nullable=False)
    value_range: Mapped[str] = mapped_column(String(100), nullable=False)
    impact_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    is_critical: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class StrategicAssumption(Base):
    __tablename__ = "strategic_assumptions_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    statement: Mapped[Text] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="fragile", index=True) # valid, questioned, fragile, invalidated, unknown

class FutureScenario(Base):
    __tablename__ = "future_scenarios_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="5_year", index=True)
    scenario_type: Mapped[str] = mapped_column(String(100), nullable=False) # baseline, upside, downside, disruption, transformation, custom
    plausibility: Mapped[str] = mapped_column(String(50), nullable=False, default="high") # low, medium, high, unknown
    assumptions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    drivers_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    uncertainties_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class ScenarioTimeline(Base):
    __tablename__ = "scenario_timelines"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    time_window: Mapped[str] = mapped_column(String(100), nullable=False)
    event_description: Mapped[Text] = mapped_column(Text, nullable=False)
    driver_id: Mapped[str] = mapped_column(String(255), nullable=True)
    impact_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class ScenarioIndicator(Base):
    __tablename__ = "scenario_indicators_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    indicator_name: Mapped[str] = mapped_column(String(255), nullable=False)
    baseline_val: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    threshold_val: Mapped[float] = mapped_column(Float, nullable=False, default=150.0)
    current_val: Mapped[float] = mapped_column(Float, nullable=False, default=162.5)
    direction: Mapped[str] = mapped_column(String(50), nullable=False, default="increasing")
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class ScenarioImpact(Base):
    __tablename__ = "scenario_impacts_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    domain: Mapped[str] = mapped_column(String(100), nullable=False) # strategy, portfolio, capability, financial, operational, technology, customer
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    details_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class StrategicOption(Base):
    __tablename__ = "strategic_options_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    option_name: Mapped[str] = mapped_column(String(255), nullable=False)
    option_type: Mapped[str] = mapped_column(String(100), nullable=False) # invest, wait, experiment, hedge, partner, diversify, exit, build, acquire
    reversibility: Mapped[str] = mapped_column(String(100), nullable=False, default="highly_reversible") # highly_reversible, reversible, partially_reversible, irreversible
    robustness_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class StrategicOptionality(Base):
    __tablename__ = "strategic_optionalities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    option_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    supported_scenarios_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    cost_estimate: Mapped[float] = mapped_column(Float, nullable=False, default=25000.0)
    reversibility: Mapped[str] = mapped_column(String(100), nullable=False, default="highly_reversible")
    upside_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    downside_protection: Mapped[Text] = mapped_column(Text, nullable=False)

class StrategicBet(Base):
    __tablename__ = "strategic_bets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    thesis: Mapped[Text] = mapped_column(Text, nullable=False)
    investment_amount: Mapped[float] = mapped_column(Float, nullable=False, default=500000.0)
    expected_outcomes_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    scenarios_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    evidence: Mapped[Text] = mapped_column(Text, nullable=False)
    review_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # proposed, approved, active, under_review, successful, failed, retired

class StrategicExposure(Base):
    __tablename__ = "strategic_exposures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dependency_name: Mapped[str] = mapped_column(String(255), nullable=False)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False)
    scenario_id: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    exposure_type: Mapped[str] = mapped_column(String(100), nullable=False, default="assumption_dependence")

class StrategicBlindSpot(Base):
    __tablename__ = "strategic_blind_spots_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    blind_spot_type: Mapped[str] = mapped_column(String(100), nullable=False) # unmonitored_driver, unquestioned_assumption, missing_scenario, missing_capability
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    impact_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    recommended_action: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class StrategicTrigger(Base):
    __tablename__ = "strategic_triggers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    indicator_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    condition_expression: Mapped[Text] = mapped_column(Text, nullable=False)
    recommended_action: Mapped[str] = mapped_column(String(100), nullable=False, default="review") # review, experiment, re_forecast, re_optimize, re_plan
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class ForesightReview(Base):
    __tablename__ = "foresight_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    review_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    participants_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    scenarios_reviewed_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    assumptions_challenged_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    decisions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    actions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class AdversarialScenario(Base):
    __tablename__ = "adversarial_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    adversarial_thesis: Mapped[Text] = mapped_column(Text, nullable=False)
    is_hypothetical: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")

class ScenarioQualityAssessment(Base):
    __tablename__ = "scenario_quality_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evidence_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    assumption_clarity: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    internal_consistency: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    diversity_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    groupthink_warning_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

class ForesightMemory(Base):
    __tablename__ = "foresight_memories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    scenario_id: Mapped[str] = mapped_column(String(255), nullable=False)
    indicator_id: Mapped[str] = mapped_column(String(255), nullable=True)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=True)
    actual_developments: Mapped[Text] = mapped_column(Text, nullable=False)
    lesson_text: Mapped[Text] = mapped_column(Text, nullable=False)

class AdaptiveStrategy(Base):
    __tablename__ = "adaptive_strategies_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    strategic_intent: Mapped[Text] = mapped_column(Text, nullable=False)
    horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="3_year")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # draft, active, under_review, adaptation_required, superseded, retired
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class StrategicIntent(Base):
    __tablename__ = "strategic_intents_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    objective: Mapped[str] = mapped_column(String(255), nullable=False)
    desired_outcome: Mapped[Text] = mapped_column(Text, nullable=False)
    constraints_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    time_horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="3_year")
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="p1")

class StrategicThesis(Base):
    __tablename__ = "strategic_theses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    belief: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    assumptions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    expected_outcome: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="supported", index=True) # supported, questioned, weakening, invalidated, unknown

class StrategyIndicator(Base):
    __tablename__ = "strategy_indicators_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    metric: Mapped[str] = mapped_column(String(255), nullable=False)
    baseline: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    target: Mapped[float] = mapped_column(Float, nullable=False, default=200.0)
    current: Mapped[float] = mapped_column(Float, nullable=False, default=145.0)
    direction: Mapped[str] = mapped_column(String(50), nullable=False, default="increasing")
    threshold: Mapped[float] = mapped_column(Float, nullable=False, default=120.0)
    source: Mapped[str] = mapped_column(String(255), nullable=False, default="internal_kpi")
    freshness: Mapped[str] = mapped_column(String(50), nullable=False, default="realtime")
    type: Mapped[str] = mapped_column(String(100), nullable=False, default="financial") # market, financial, customer, operational, technology, competitive, regulatory, risk, capability, portfolio

class StrategyDriftSignal(Base):
    __tablename__ = "strategy_drift_signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    drift_type: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True) # low, medium, high, critical
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    affected_strategy: Mapped[Text] = mapped_column(Text, nullable=False)

class PortfolioStrategicExposure(Base):
    __tablename__ = "portfolio_strategic_exposures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    scenario_id: Mapped[str] = mapped_column(String(255), nullable=False)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False)
    dependency_name: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    exposure_type: Mapped[str] = mapped_column(String(100), nullable=False, default="scenario_concentration")

class AdaptiveInitiativeState(Base):
    __tablename__ = "adaptive_initiative_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    performance_val: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    strategic_alignment: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    scenario_support: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    benefits_realized: Mapped[float] = mapped_column(Float, nullable=False, default=250000.0)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    recommendation: Mapped[str] = mapped_column(String(100), nullable=False, default="continue") # accelerate, continue, monitor, reassess, rescope, pause, retire

class PortfolioReconfiguration(Base):
    __tablename__ = "portfolio_reconfigurations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    reconfiguration_type: Mapped[str] = mapped_column(String(100), nullable=False) # rebalance, accelerate, decelerate, pause, rescope, sequence_change, dependency_change, investment_shift, capability_shift
    current_state_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    proposed_state_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    expected_effect: Mapped[Text] = mapped_column(Text, nullable=False)
    risks_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_initiatives_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="proposed", index=True) # proposed, approved, executed, verified, rejected

class StrategicTradeoff(Base):
    __tablename__ = "strategic_tradeoffs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reconfiguration_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    option_a: Mapped[str] = mapped_column(String(255), nullable=False)
    option_b: Mapped[str] = mapped_column(String(255), nullable=False)
    cost_diff: Mapped[float] = mapped_column(Float, nullable=False, default=50000.0)
    benefit_diff: Mapped[Text] = mapped_column(Text, nullable=False)
    risk_diff: Mapped[Text] = mapped_column(Text, nullable=False)
    time_diff: Mapped[str] = mapped_column(String(100), nullable=False, default="2_months")
    reversibility: Mapped[str] = mapped_column(String(100), nullable=False, default="highly_reversible")

class StrategyAdaptationTrigger(Base):
    __tablename__ = "strategy_adaptation_triggers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger_type: Mapped[str] = mapped_column(String(100), nullable=False) # assumption_break, performance_decline, risk_increase, scenario_shift, capability_gap, market_shift, technology_shift, regulatory_shift
    recommended_action: Mapped[str] = mapped_column(String(100), nullable=False, default="review", index=True) # review, simulate, re_optimize, re_scope, reallocate, pause, accelerate
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class AdaptiveStrategyReview(Base):
    __tablename__ = "adaptive_strategy_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    review_cadence: Mapped[str] = mapped_column(String(50), nullable=False, default="quarterly") # monthly, quarterly, semiannual, annual, event_driven
    participants_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    assumptions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    scenarios_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    portfolio_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    decisions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="completed", index=True)

class StrategicOutcomeObservation(Base):
    __tablename__ = "strategic_outcome_observations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expected_outcome: Mapped[Text] = mapped_column(Text, nullable=False)
    actual_outcome: Mapped[Text] = mapped_column(Text, nullable=False)
    variance: Mapped[float] = mapped_column(Float, nullable=False, default=0.05)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class StrategyLearning(Base):
    __tablename__ = "strategy_learnings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=True)
    assumption_statement: Mapped[Text] = mapped_column(Text, nullable=False)
    action_taken: Mapped[Text] = mapped_column(Text, nullable=False)
    actual_outcome: Mapped[Text] = mapped_column(Text, nullable=False)
    lesson_text: Mapped[Text] = mapped_column(Text, nullable=False)

class CapitalFlexibilityAssessment(Base):
    __tablename__ = "capital_flexibility_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    committed_capital: Mapped[float] = mapped_column(Float, nullable=False, default=2500000.0)
    discretionary_capital: Mapped[float] = mapped_column(Float, nullable=False, default=750000.0)
    reallocation_constraints: Mapped[Text] = mapped_column(Text, nullable=False)
    time_to_reallocate_days: Mapped[int] = mapped_column(Integer, nullable=False, default=14)

class CapacityFlexibilityAssessment(Base):
    __tablename__ = "capacity_flexibility_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    available_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    committed_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=78.0)
    reallocation_constraints: Mapped[Text] = mapped_column(Text, nullable=False)

class DependencyFlexibilityAssessment(Base):
    __tablename__ = "dependency_flexibility_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    single_source_dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    switching_cost: Mapped[float] = mapped_column(Float, nullable=False, default=35000.0)
    fallback_readiness: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class StrategicBottleneck(Base):
    __tablename__ = "strategic_bottlenecks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    bottleneck_type: Mapped[str] = mapped_column(String(100), nullable=False) # capital, capacity, technology, talent, vendor, data, dependency, regulatory
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    recommended_mitigation: Mapped[Text] = mapped_column(Text, nullable=False)

class CapabilityInvestmentOption(Base):
    __tablename__ = "capability_investment_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False)
    cost_estimate: Mapped[float] = mapped_column(Float, nullable=False, default=120000.0)
    time_to_build: Mapped[str] = mapped_column(String(100), nullable=False, default="3_months")
    strategic_value: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    scenario_coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    optionality_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)

class StrategicExperiment(Base):
    __tablename__ = "strategic_experiments_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    hypothesis: Mapped[Text] = mapped_column(Text, nullable=False)
    test_design: Mapped[Text] = mapped_column(Text, nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    cost: Mapped[float] = mapped_column(Float, nullable=False, default=15000.0)
    success_criteria: Mapped[Text] = mapped_column(Text, nullable=False)
    decision_threshold: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="running", index=True) # designed, running, completed, cancelled

class StrategicExperimentOutcome(Base):
    __tablename__ = "strategic_experiment_outcomes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    experiment_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    outcome_classification: Mapped[str] = mapped_column(String(50), nullable=False, default="supports") # supports, weakens, invalidates, inconclusive
    evidence_details: Mapped[Text] = mapped_column(Text, nullable=False)
    updated_confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class ExecutionObjective(Base):
    __tablename__ = "execution_objectives_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    target_outcome: Mapped[Text] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="p1")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # planned, active, at_risk, blocked, achieved, deferred, retired
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class StrategicAlignmentAssessment(Base):
    __tablename__ = "strategic_alignment_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    objective_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=True)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=True)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=True)
    alignment_status: Mapped[str] = mapped_column(String(50), nullable=False, default="aligned") # strong, aligned, weak, misaligned, unknown
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class ExecutionCoverage(Base):
    __tablename__ = "execution_coverages_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    objective_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    portfolio_coverage_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    initiative_coverage_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    mission_coverage_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    execution_coverage_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    benefit_coverage_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.82)
    has_gap: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

class StrategicExecutionPath(Base):
    __tablename__ = "strategic_execution_paths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    objective_id: Mapped[str] = mapped_column(String(255), nullable=False)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False)
    action_id: Mapped[str] = mapped_column(String(255), nullable=True)
    deliverable_id: Mapped[str] = mapped_column(String(255), nullable=True)
    outcome_id: Mapped[str] = mapped_column(String(255), nullable=True)
    benefit_id: Mapped[str] = mapped_column(String(255), nullable=True)
    path_integrity_status: Mapped[str] = mapped_column(String(50), nullable=False, default="intact") # intact, broken_link, degraded

class ExecutionDriftSignal(Base):
    __tablename__ = "execution_drift_signals_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    objective_id: Mapped[str] = mapped_column(String(255), nullable=False)
    drift_type: Mapped[str] = mapped_column(String(100), nullable=False) # priority, scope, schedule, dependency, resource, benefit, alignment
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True) # low, medium, high, critical
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class ExecutionDependencyBlocker(Base):
    __tablename__ = "execution_dependency_blockers_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    blocked_initiative_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dependency_id: Mapped[str] = mapped_column(String(255), nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    impact_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, resolving, resolved

class ExecutionCapacityConflict(Base):
    __tablename__ = "execution_capacity_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    competing_initiative_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False) # people, systems, budget, data, vendors, ai_capacity, infrastructure
    conflict_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    recommendation: Mapped[Text] = mapped_column(Text, nullable=False)

class DecisionExecutionGap(Base):
    __tablename__ = "decision_execution_gaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    approval_id: Mapped[str] = mapped_column(String(255), nullable=False)
    decision_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    approval_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    action_start_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    action_completion_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    delay_days: Mapped[int] = mapped_column(Integer, nullable=False, default=12)
    is_stale: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class ExecutionFrictionSignal(Base):
    __tablename__ = "execution_friction_signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    objective_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    friction_type: Mapped[str] = mapped_column(String(100), nullable=False) # approval, dependency, capacity, data, technical, policy, coordination, communication
    impact_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    recurring_count: Mapped[int] = mapped_column(Integer, nullable=False, default=3)

class ExecutionOutcomeGap(Base):
    __tablename__ = "execution_outcome_gaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expected_outcome: Mapped[Text] = mapped_column(Text, nullable=False)
    actual_outcome: Mapped[Text] = mapped_column(Text, nullable=False)
    gap_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    completion_without_success_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class StrategicContributionAssessment(Base):
    __tablename__ = "strategic_contribution_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    objective_id: Mapped[str] = mapped_column(String(255), nullable=False)
    kpi_contribution: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    capability_contribution: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    benefit_contribution: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class ExecutionPriorityAssessment(Base):
    __tablename__ = "execution_priority_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    strategic_importance: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    urgency: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.25)
    dependency_weight: Mapped[float] = mapped_column(Float, nullable=False, default=0.80)
    priority_conflict_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

class ExecutionRecommendation(Base):
    __tablename__ = "execution_recommendations_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    objective_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False)
    recommendation_type: Mapped[str] = mapped_column(String(100), nullable=False) # accelerate, continue, monitor, reassess, resequence, rescope, pause, escalate
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="proposed", index=True) # proposed, approved, executed, rejected

class ExecutionQualityAssessment(Base):
    __tablename__ = "execution_quality_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    rework_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    failure_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rollback_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    defect_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.02)
    verification_failure_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

class ExecutionWasteSignal(Base):
    __tablename__ = "execution_waste_signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    waste_type: Mapped[str] = mapped_column(String(100), nullable=False) # duplicate_work, low_value_work, blocked_work, rework, unused_output, benefit_failure
    impact_amount: Mapped[float] = mapped_column(Float, nullable=False, default=45000.0)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class ExecutionRiskAssessment(Base):
    __tablename__ = "execution_risk_assessments_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    objective_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    delay_risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.15)
    dependency_risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.20)
    capacity_risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.18)
    alignment_risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.10)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)

class ExecutionEarlyWarning(Base):
    __tablename__ = "execution_early_warnings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    objective_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    warning_trigger: Mapped[str] = mapped_column(String(100), nullable=False) # velocity_decline, dependency_growth, benefit_lag, quality_degradation, decision_delay
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class ExecutionStrategyReview(Base):
    __tablename__ = "execution_strategy_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    review_cadence: Mapped[str] = mapped_column(String(50), nullable=False, default="monthly") # weekly, monthly, quarterly, event_driven
    participants_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    objectives_reviewed_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    decisions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="completed", index=True)

class ExecutionLesson(Base):
    __tablename__ = "execution_lessons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    plan_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    decision_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    execution_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    outcome_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    lesson_text: Mapped[Text] = mapped_column(Text, nullable=False)

class OperatingModel(Base):
    __tablename__ = "operating_models_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # draft, active, under_review, superseded, retired
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class OperatingPrinciple(Base):
    __tablename__ = "operating_principles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    principle: Mapped[str] = mapped_column(String(255), nullable=False)
    intent: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")

class OrganizationalUnit(Base):
    __tablename__ = "organizational_units_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    parent_id: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False) # enterprise, division, business_unit, department, team, function, program_office, shared_service, external_partner
    purpose: Mapped[Text] = mapped_column(Text, nullable=False)
    scope: Mapped[Text] = mapped_column(Text, nullable=False)
    responsibilities: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class OperatingResponsibility(Base):
    __tablename__ = "operating_responsibilities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    unit_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=True)
    process_id: Mapped[str] = mapped_column(String(255), nullable=True)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=True)
    scope: Mapped[Text] = mapped_column(Text, nullable=False)
    responsibility_type: Mapped[str] = mapped_column(String(50), nullable=False, default="primary") # primary, supporting, consulted, informed

class AccountabilityMapping(Base):
    __tablename__ = "accountability_mappings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    outcome_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    objective_id: Mapped[str] = mapped_column(String(255), nullable=False)
    initiative_id: Mapped[str] = mapped_column(String(255), nullable=True)
    process_id: Mapped[str] = mapped_column(String(255), nullable=True)
    unit_id: Mapped[str] = mapped_column(String(255), nullable=False)
    has_gap: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_conflict: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

class DecisionRight(Base):
    __tablename__ = "decision_rights_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    decision_type: Mapped[str] = mapped_column(String(100), nullable=False)
    scope: Mapped[Text] = mapped_column(Text, nullable=False, index=True)
    authority_level: Mapped[str] = mapped_column(String(100), nullable=False)
    constraints_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    escalation_path: Mapped[Text] = mapped_column(Text, nullable=False)

class DecisionRightsMatrix(Base):
    __tablename__ = "decision_rights_matrices"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_right_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    unit_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    role_type: Mapped[str] = mapped_column(String(50), nullable=False, default="decides") # decides, approves, recommends, consulted, informed

class OperatingProcess(Base):
    __tablename__ = "operating_processes_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    purpose: Mapped[Text] = mapped_column(Text, nullable=False)
    owner_unit_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    inputs_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    outputs_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    systems_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # active, degraded, under_review, retired

class ProcessStep(Base):
    __tablename__ = "process_steps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    process_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    owner_unit_id: Mapped[str] = mapped_column(String(255), nullable=False)
    input_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    output_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    dependency_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    system_name: Mapped[str] = mapped_column(String(255), nullable=False)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=True)

class ProcessHandoff(Base):
    __tablename__ = "process_handoffs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    process_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    from_unit_id: Mapped[str] = mapped_column(String(255), nullable=False)
    to_unit_id: Mapped[str] = mapped_column(String(255), nullable=False)
    artifact_name: Mapped[str] = mapped_column(String(255), nullable=False)
    wait_time_hours: Mapped[float] = mapped_column(Float, nullable=False, default=4.5)
    failure_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.03)
    friction_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

class ProcessBottleneck(Base):
    __tablename__ = "process_bottlenecks_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    process_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    bottleneck_type: Mapped[str] = mapped_column(String(100), nullable=False) # capacity, decision, dependency, technology, handoff, approval, data
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)

class CrossFunctionalFlow(Base):
    __tablename__ = "cross_functional_flows"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    unit_a_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    unit_b_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    process_id: Mapped[str] = mapped_column(String(255), nullable=False)
    handoff_count: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    friction_level: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")

class OperatingCapacityProfile(Base):
    __tablename__ = "operating_capacity_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    demand_units: Mapped[float] = mapped_column(Float, nullable=False, default=120.0)
    available_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    committed_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=90.0)
    buffer_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=10.0)
    capacity_type: Mapped[str] = mapped_column(String(50), nullable=False, default="fixed") # fixed, flexible, shared, external

class OperatingModelGap(Base):
    __tablename__ = "operating_model_gaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    gap_type: Mapped[str] = mapped_column(String(100), nullable=False) # capability, accountability, decision, process, capacity, dependency, technology, governance
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True) # low, medium, high, critical

class OperatingModelRecommendation(Base):
    __tablename__ = "operating_model_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    recommendation_type: Mapped[str] = mapped_column(String(100), nullable=False) # clarify, standardize, delegate, centralize, decentralize, automate, integrate, remove_dependency, build_capability, increase_capacity
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="proposed", index=True) # proposed, approved, executed, rejected

class OperatingModelScenario(Base):
    __tablename__ = "operating_model_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scenario_type: Mapped[str] = mapped_column(String(100), nullable=False) # centralize_function, delegate_decision, merge_process, split_capability, introduce_shared_service
    proposed_changes_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    simulated_effects_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class OperatingModelTradeoff(Base):
    __tablename__ = "operating_model_tradeoffs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    option_a: Mapped[Text] = mapped_column(Text, nullable=False)
    option_b: Mapped[Text] = mapped_column(Text, nullable=False)
    cost_diff: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    speed_diff: Mapped[float] = mapped_column(Float, nullable=False, default=0.25)
    control_diff: Mapped[float] = mapped_column(Float, nullable=False, default=-0.10)
    resilience_diff: Mapped[float] = mapped_column(Float, nullable=False, default=0.15)
    complexity_diff: Mapped[float] = mapped_column(Float, nullable=False, default=-0.15)

class OperatingModelDriftSignal(Base):
    __tablename__ = "operating_model_drift_signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    documented_behavior: Mapped[Text] = mapped_column(Text, nullable=False)
    observed_behavior: Mapped[Text] = mapped_column(Text, nullable=False)
    difference_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)

class OperatingAssumption(Base):
    __tablename__ = "operating_assumptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    statement: Mapped[Text] = mapped_column(Text, nullable=False)
    validity_status: Mapped[str] = mapped_column(String(50), nullable=False, default="valid") # valid, questioned, fragile, invalidated, unknown

class OperatingIndicator(Base):
    __tablename__ = "operating_indicators"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    metric_name: Mapped[str] = mapped_column(String(255), nullable=False)
    current_value: Mapped[float] = mapped_column(Float, nullable=False, default=4.2)
    target_value: Mapped[float] = mapped_column(Float, nullable=False, default=2.0)
    trend: Mapped[str] = mapped_column(String(50), nullable=False, default="improving")

class OperatingModelEarlyWarning(Base):
    __tablename__ = "operating_model_early_warnings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    warning_trigger: Mapped[str] = mapped_column(String(100), nullable=False) # decision_latency_increase, handoff_degradation, capacity_overload, dependency_concentration, accountability_conflict
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class OperatingModelChangeProposal(Base):
    __tablename__ = "operating_model_change_proposals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    problem_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    options_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    tradeoffs_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    expected_effect: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="proposed", index=True) # proposed, approved, executed, rejected

class OperatingModelChangeOutcome(Base):
    __tablename__ = "operating_model_change_outcomes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proposal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expected_effect: Mapped[Text] = mapped_column(Text, nullable=False)
    actual_effect: Mapped[Text] = mapped_column(Text, nullable=False)
    variance: Mapped[float] = mapped_column(Float, nullable=False, default=0.05)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class OperatingModelLesson(Base):
    __tablename__ = "operating_model_lessons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proposal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    change_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    outcome_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    lesson_text: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationProgram(Base):
    __tablename__ = "transformation_programs_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    strategic_drivers_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    scope: Mapped[Text] = mapped_column(Text, nullable=False)
    horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="3_year")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # draft, active, under_review, approved, executing, completed, paused, retired
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationDriver(Base):
    __tablename__ = "transformation_drivers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    driver_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # strategy, growth, cost, risk, technology, customer, regulation, resilience, capacity, innovation, operational_performance
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    freshness: Mapped[str] = mapped_column(String(50), nullable=False, default="realtime")

class OperatingModelCurrentState(Base):
    __tablename__ = "operating_model_current_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    units_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    capabilities_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    processes_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    decision_rights_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    systems_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    capacity_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")

class OperatingModelTargetState(Base):
    __tablename__ = "operating_model_target_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    structure_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    target_capabilities_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    target_processes_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    target_decision_rights_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    target_dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    technology_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    capacity_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")

class OperatingModelDelta(Base):
    __tablename__ = "operating_model_deltas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    current_state_id: Mapped[str] = mapped_column(String(255), nullable=False)
    target_state_id: Mapped[str] = mapped_column(String(255), nullable=False)
    gap_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True) # low, medium, high, critical
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class TransformationDesignPrinciple(Base):
    __tablename__ = "transformation_design_principles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    principle_name: Mapped[str] = mapped_column(String(100), nullable=False) # customer_first, simplify, decentralize, standardize, automate, resilience_first, platform_first, control_by_design
    statement: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationConstraint(Base):
    __tablename__ = "transformation_constraints"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    constraint_type: Mapped[str] = mapped_column(String(100), nullable=False) # budget, regulatory, technology, capacity, dependency, risk, timeline, governance
    description: Mapped[Text] = mapped_column(Text, nullable=False)

class FutureOperatingModel(Base):
    __tablename__ = "future_operating_models"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    design_principles_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    constraints_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    assumptions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    target_capabilities_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    target_processes_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    target_decision_rights_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    target_dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class OperatingModelDesignOption(Base):
    __tablename__ = "operating_model_design_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    future_model_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    option_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # centralize, decentralize, federate, platformize, standardize, automate, outsource, insource, integrate, simplify, reconfigure
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    assumptions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    expected_effect: Mapped[Text] = mapped_column(Text, nullable=False)
    risks_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class OperatingModelComparison(Base):
    __tablename__ = "operating_model_comparisons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    option_a_id: Mapped[str] = mapped_column(String(255), nullable=False)
    option_b_id: Mapped[str] = mapped_column(String(255), nullable=False)
    cost_tradeoff: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    speed_tradeoff: Mapped[float] = mapped_column(Float, nullable=False, default=0.30)
    control_tradeoff: Mapped[float] = mapped_column(Float, nullable=False, default=-0.05)
    resilience_tradeoff: Mapped[float] = mapped_column(Float, nullable=False, default=0.20)
    complexity_tradeoff: Mapped[float] = mapped_column(Float, nullable=False, default=-0.15)
    classification: Mapped[str] = mapped_column(String(50), nullable=False, default="competitive") # dominated, competitive, high_upside, high_risk

class TransformationScenario(Base):
    __tablename__ = "transformation_scenarios_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    scenario_name: Mapped[str] = mapped_column(String(255), nullable=False)
    scenario_type: Mapped[str] = mapped_column(String(100), nullable=False) # growth, downturn, crisis, technology_shift, regulatory_change, capacity_loss, demand_surge
    simulated_performance: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    simulated_risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.18)
    simulated_resilience: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="simulated", index=True)

class TransformationRisk(Base):
    __tablename__ = "transformation_risks_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_type: Mapped[str] = mapped_column(String(100), nullable=False) # execution, adoption, technology, dependency, regulatory, capacity, operational, strategic
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)

class TransformationRiskMitigation(Base):
    __tablename__ = "transformation_risk_mitigations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    recommended_action: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="proposed")

class TransformationDependency(Base):
    __tablename__ = "transformation_dependencies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    prerequisite_change: Mapped[Text] = mapped_column(Text, nullable=False)
    dependent_change: Mapped[Text] = mapped_column(Text, nullable=False)
    criticality: Mapped[str] = mapped_column(String(50), nullable=False, default="critical_path", index=True) # low, medium, high, critical_path
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")

class TransformationWorkstream(Base):
    __tablename__ = "transformation_workstreams"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False) # organization, process, technology, data, governance, capability, decision_rights, change_management
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_unit_id: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class TransformationMilestone(Base):
    __tablename__ = "transformation_milestones"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workstream_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    target_date: Mapped[str] = mapped_column(String(50), nullable=False)
    dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="planned", index=True)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class TransformationRoadmap(Base):
    __tablename__ = "transformation_roadmaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phases_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    workstreams_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    milestones_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    decision_gates_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class TransformationDecisionGate(Base):
    __tablename__ = "transformation_decision_gates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    roadmap_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    gate_name: Mapped[str] = mapped_column(String(255), nullable=False)
    required_criteria_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    gate_outcome: Mapped[str] = mapped_column(String(50), nullable=False, default="proceed") # proceed, revise, pause, stop, pilot_more
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class TransformationPilot(Base):
    __tablename__ = "transformation_pilots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    hypothesis: Mapped[Text] = mapped_column(Text, nullable=False)
    expected_effect: Mapped[Text] = mapped_column(Text, nullable=False)
    measurement_criteria: Mapped[Text] = mapped_column(Text, nullable=False)
    success_threshold: Mapped[Text] = mapped_column(Text, nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False, default=45)
    outcome_status: Mapped[str] = mapped_column(String(50), nullable=False, default="validated", index=True) # validated, partially_validated, invalidated, inconclusive

class TransformationAdoptionAssessment(Base):
    __tablename__ = "transformation_adoption_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    process_adoption_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    system_adoption_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    decision_right_adoption_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    capability_adoption_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    aggregate_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.91)

class TransformationReadinessAssessment(Base):
    __tablename__ = "transformation_readiness_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dimension: Mapped[str] = mapped_column(String(100), nullable=False) # capability, technology, process, governance, capacity, dependency, adoption
    current_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    required_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    has_gap: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

class TransformationTransitionPlan(Base):
    __tablename__ = "transformation_transition_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    old_state_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    new_state_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    steps_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    fallback_plan: Mapped[Text] = mapped_column(Text, nullable=False)
    rollback_conditions: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationOutcome(Base):
    __tablename__ = "transformation_outcomes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    outcome_category: Mapped[str] = mapped_column(String(100), nullable=False) # strategic, operational, financial, risk, resilience, customer, capability
    expected_value: Mapped[Text] = mapped_column(Text, nullable=False)
    actual_value: Mapped[Text] = mapped_column(Text, nullable=False)
    variance: Mapped[float] = mapped_column(Float, nullable=False, default=0.03)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class TransformationDriftSignal(Base):
    __tablename__ = "transformation_drift_signals_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    approved_target_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    implemented_state_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    observed_state_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    difference_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)

class TransformationLesson(Base):
    __tablename__ = "transformation_lessons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    hypothesis_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    decision_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    change_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    actual_outcome: Mapped[Text] = mapped_column(Text, nullable=False)
    lesson_text: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationChangeProposal(Base):
    __tablename__ = "transformation_change_proposals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    proposal_title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    options_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    expected_effect: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="proposed", index=True) # proposed, approved, executed, rejected

class TransformationPortfolio(Base):
    __tablename__ = "transformation_portfolios_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    strategy_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="3_year")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="approved", index=True) # draft, proposed, under_review, approved, executing, stable, rebalancing, completed, retired
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationCandidate(Base):
    __tablename__ = "transformation_candidates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    transformation_program_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    strategic_value_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    urgency: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.15, index=True)
    cost_estimate: Mapped[float] = mapped_column(Float, nullable=False, default=150000.0)
    capacity_demand_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    optional_value: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class TransformationDependencyGraph(Base):
    __tablename__ = "transformation_dependency_graphs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dependency_matrix_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    critical_path_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    parallel_groups_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    cycles_detected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    blocked_candidates_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class TransformationSequence(Base):
    __tablename__ = "transformation_sequences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sequence_type: Mapped[str] = mapped_column(String(100), nullable=False) # fast, risk_first, capability_first, cost_first, resilience_first, balanced, custom
    phases_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    order_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    parallel_groups_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    decision_gates_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class TransformationSequenceComparison(Base):
    __tablename__ = "transformation_sequence_comparisons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    sequence_a_id: Mapped[str] = mapped_column(String(255), nullable=False)
    sequence_b_id: Mapped[str] = mapped_column(String(255), nullable=False)
    time_diff: Mapped[float] = mapped_column(Float, nullable=False, default=-0.35)
    cost_diff: Mapped[float] = mapped_column(Float, nullable=False, default=-0.10)
    risk_diff: Mapped[float] = mapped_column(Float, nullable=False, default=-0.40)
    capacity_diff: Mapped[float] = mapped_column(Float, nullable=False, default=0.15)
    benefit_diff: Mapped[float] = mapped_column(Float, nullable=False, default=0.25)
    optionality_diff: Mapped[float] = mapped_column(Float, nullable=False, default=0.30)
    robustness_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)

class TransformationPortfolioBottleneck(Base):
    __tablename__ = "transformation_portfolio_bottlenecks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    bottleneck_type: Mapped[str] = mapped_column(String(100), nullable=False) # capacity, dependency, decision, technology, capability, vendor, regulatory
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)

class TransformationCapacityPlan(Base):
    __tablename__ = "transformation_capacity_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    time_window: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    required_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=85.0)
    available_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    committed_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=70.0)
    buffer_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=15.0)

class TransformationCapitalConstraint(Base):
    __tablename__ = "transformation_capital_constraints"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    budget_envelope: Mapped[float] = mapped_column(Float, nullable=False, default=1000000.0)
    committed_amount: Mapped[float] = mapped_column(Float, nullable=False, default=450000.0)
    remaining_flexibility: Mapped[float] = mapped_column(Float, nullable=False, default=550000.0)
    timing_constraints: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationCapacityConstraint(Base):
    __tablename__ = "transformation_capacity_constraints"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    fixed_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=50.0)
    flexible_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=30.0)
    shared_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=15.0)
    external_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=5.0)

class TransformationLockInRisk(Base):
    __tablename__ = "transformation_lock_in_risks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_type: Mapped[str] = mapped_column(String(100), nullable=False) # technology, vendor, architecture, process, organizational, financial
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    reversibility: Mapped[str] = mapped_column(String(50), nullable=False, default="high") # high, medium, low, irreversible

class TransformationPortfolioOutcome(Base):
    __tablename__ = "transformation_portfolio_outcomes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expected_benefits_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    actual_benefits_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    variance: Mapped[float] = mapped_column(Float, nullable=False, default=0.04)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class TransformationBenefitOverlap(Base):
    __tablename__ = "transformation_benefit_overlaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    candidate_a_id: Mapped[str] = mapped_column(String(255), nullable=False)
    candidate_b_id: Mapped[str] = mapped_column(String(255), nullable=False)
    claimed_benefit: Mapped[Text] = mapped_column(Text, nullable=False)
    overlap_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.35)

class TransformationConflict(Base):
    __tablename__ = "transformation_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    conflict_type: Mapped[str] = mapped_column(String(100), nullable=False) # strategic, technical, capacity, organizational, dependency, timing
    affected_candidates_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    recommendation: Mapped[Text] = mapped_column(Text, nullable=False)

class MinimumTransformationSet(Base):
    __tablename__ = "minimum_transformation_sets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_objective: Mapped[Text] = mapped_column(Text, nullable=False)
    required_candidate_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    total_cost: Mapped[float] = mapped_column(Float, nullable=False, default=250000.0)
    total_time: Mapped[str] = mapped_column(String(50), nullable=False, default="6_months")

class TransformationWave(Base):
    __tablename__ = "transformation_waves"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    wave_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    wave_type: Mapped[str] = mapped_column(String(100), nullable=False) # foundation, pilot, scale, optimization, stabilization
    candidate_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    exit_criteria_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="executing", index=True)

class TransformationContingencyPlan(Base):
    __tablename__ = "transformation_contingency_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger_condition: Mapped[Text] = mapped_column(Text, nullable=False)
    fallback_action: Mapped[Text] = mapped_column(Text, nullable=False)
    impact_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    owner_unit_id: Mapped[str] = mapped_column(String(255), nullable=False)
    approval_status: Mapped[str] = mapped_column(String(50), nullable=False, default="approved")

class TransformationPortfolioRebalance(Base):
    __tablename__ = "transformation_portfolio_rebalances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    rebalance_reason: Mapped[str] = mapped_column(String(100), nullable=False) # capacity_change, risk_change, scenario_shift, benefit_change, dependency_failure, strategy_change
    proposed_sequence_id: Mapped[str] = mapped_column(String(255), nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="proposed", index=True) # proposed, approved, executed, rejected

class TransformationSequenceDrift(Base):
    __tablename__ = "transformation_sequence_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    approved_sequence_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    actual_execution_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    drift_reasons_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)

class TransformationControlTower(Base):
    __tablename__ = "transformation_control_towers_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="healthy", index=True) # initializing, healthy, watch, at_risk, critical, degraded, paused
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    last_evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationLiveState(Base):
    __tablename__ = "transformation_live_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_tower_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    planned_state_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    actual_state_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    forecast_state_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    last_change: Mapped[Text] = mapped_column(Text, nullable=False)
    last_evaluation: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationControlSignal(Base):
    __tablename__ = "transformation_control_signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_tower_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    signal_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # schedule, capacity, dependency, risk, benefit, readiness, adoption, quality, alignment, sequence
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True) # info, low, medium, high, critical
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="detected", index=True) # detected, acknowledged, investigating, mitigated, resolved, dismissed
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class TransformationSituation(Base):
    __tablename__ = "transformation_situations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_tower_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    signals_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_transformations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_waves_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_objectives_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)

class TransformationRootCauseAssessment(Base):
    __tablename__ = "transformation_root_cause_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    situation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False) # capacity, dependency, decision, technology, process, governance, scope, risk, external_change
    evidence_label: Mapped[str] = mapped_column(String(50), nullable=False, default="supported") # observed, supported, inferred
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class TransformationEarlyWarning(Base):
    __tablename__ = "transformation_early_warnings_v2"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_tower_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    warning_trigger: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")

class TransformationWaveReadiness(Base):
    __tablename__ = "transformation_wave_readinesses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wave_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    capability_readiness: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    technology_readiness: Mapped[float] = mapped_column(Float, nullable=False, default=0.98)
    process_readiness: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    capacity_readiness: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    dependency_readiness: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    risk_readiness: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    adoption_readiness: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="ready", index=True)

class TransformationChangeRequest(Base):
    __tablename__ = "transformation_change_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_tower_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    request_type: Mapped[str] = mapped_column(String(100), nullable=False) # scope, sequence, timing, capacity, dependency, design, risk_mitigation, wave_transition
    proposed_change_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    impact_analysis_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="proposed", index=True) # proposed, approved, executed, rejected

class TransformationChangeDrift(Base):
    __tablename__ = "transformation_change_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_tower_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    approved_change_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    implemented_change_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    difference_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)

class TransformationIncident(Base):
    __tablename__ = "transformation_incidents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_tower_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="major", index=True) # minor, major, critical
    impact_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    response_recommendation: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class TransformationEscalation(Base):
    __tablename__ = "transformation_escalations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_tower_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger_reason: Mapped[Text] = mapped_column(Text, nullable=False)
    urgency: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    decision_owner_unit_id: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class TransformationWeeklyReview(Base):
    __tablename__ = "transformation_weekly_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_tower_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    portfolio_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    waves_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    signals_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    risks_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    benefits_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    decisions_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationMonthlyReview(Base):
    __tablename__ = "transformation_monthly_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_tower_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    alignment_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    performance_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    benefits_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    capacity_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    sequence_validity_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    lessons_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationControlLearning(Base):
    __tablename__ = "transformation_control_learnings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_tower_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    signal_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    decision_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    action_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    outcome_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    lesson_text: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationGraphNode(Base):
    __tablename__ = "transformation_graph_nodes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # strategy, objective, capability, unit, process, transformation, portfolio, program, workstream, milestone, dependency, decision, risk, assumption, scenario, benefit, outcome, lesson
    entity_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    freshness: Mapped[str] = mapped_column(String(50), nullable=False, default="realtime")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationGraphEdge(Base):
    __tablename__ = "transformation_graph_edges"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    from_node_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    to_node_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    relationship_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # supports, depends_on, blocks, enables, conflicts_with, duplicates, overlaps, shares_capability, shares_dependency, shares_assumption, shares_scenario, shares_benefit, influences, supersedes, precedes, follows, constrains, mitigates, exposes
    strength: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, index=True)

class TransformationGraphProvenance(Base):
    __tablename__ = "transformation_graph_provenances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    edge_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_system: Mapped[str] = mapped_column(String(255), nullable=False)
    method: Mapped[str] = mapped_column(String(100), nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    classified_as: Mapped[str] = mapped_column(String(50), nullable=False, default="observed", index=True) # observed, declared, derived, inferred

class TransformationImpactMap(Base):
    __tablename__ = "transformation_impact_maps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transformation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    strategy_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    capability_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    process_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    unit_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    system_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    downstream_transformation_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class CrossTransformationImpact(Base):
    __tablename__ = "cross_transformation_impacts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_transformation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_transformation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    impact_type: Mapped[str] = mapped_column(String(50), nullable=False, default="positive", index=True) # positive, negative, blocking, enabling, conditional, uncertain
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class TransformationCapabilityOverlap(Base):
    __tablename__ = "transformation_capability_overlaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capability_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    transformation_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    capacity_demand_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.15)
    conflict_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

class TransformationAssumptionCluster(Base):
    __tablename__ = "transformation_assumption_clusters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shared_assumption: Mapped[Text] = mapped_column(Text, nullable=False)
    transformation_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    exposure_level: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)

class TransformationScenarioExposure(Base):
    __tablename__ = "transformation_scenario_exposures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    transformation_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    vulnerability_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.12)
    impact_desc: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationBenefitGraph(Base):
    __tablename__ = "transformation_benefit_graphs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transformation_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    claimed_benefit: Mapped[Text] = mapped_column(Text, nullable=False)
    overlap_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    outcome_connection: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationConflictGraph(Base):
    __tablename__ = "transformation_conflict_graphs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transformation_a_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    transformation_b_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    conflict_domain: Mapped[str] = mapped_column(String(100), nullable=False) # target_operating_model, technology, process, decision_rights, capacity, timeline
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True) # low, medium, high, critical
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class TransformationDecisionPropagation(Base):
    __tablename__ = "transformation_decision_propagations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    affected_transformation_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    impact_mode: Mapped[str] = mapped_column(String(50), nullable=False, default="direct") # direct, indirect, conditional, downstream
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class TransformationRiskPropagation(Base):
    __tablename__ = "transformation_risk_propagations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_risk_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    affected_transformation_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    downstream_effect: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)

class TransformationLessonPropagation(Base):
    __tablename__ = "transformation_lesson_propagations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    relevant_transformation_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    relevance_level: Mapped[str] = mapped_column(String(50), nullable=False, default="high") # high, medium, low, unknown

class TransformationPattern(Base):
    __tablename__ = "transformation_patterns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pattern_name: Mapped[str] = mapped_column(String(255), nullable=False)
    pattern_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # dependency_failure, capacity_bottleneck, benefit_lag, decision_delay, adoption_friction, scope_drift
    supporting_evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)

class TransformationAnalogy(Base):
    __tablename__ = "transformation_analogies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    current_transformation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    historical_transformation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    similarity_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.86)
    key_differences_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)

class TransformationComplexityProfile(Base):
    __tablename__ = "transformation_complexity_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transformation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dependency_density: Mapped[float] = mapped_column(Float, nullable=False, default=0.35)
    cross_unit_coupling: Mapped[float] = mapped_column(Float, nullable=False, default=0.40)
    decision_density: Mapped[float] = mapped_column(Float, nullable=False, default=0.25)
    shared_capability_count: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    shared_dependency_count: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    benefit_overlap_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    scenario_exposure_count: Mapped[int] = mapped_column(Integer, nullable=False, default=2)

class TransformationComplexityHotspot(Base):
    __tablename__ = "transformation_complexity_hotspots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hotspot_name: Mapped[str] = mapped_column(String(255), nullable=False)
    converging_transformation_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    hotspot_domain: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)

class TransformationKnowledgeConflict(Base):
    __tablename__ = "transformation_knowledge_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_a_id: Mapped[str] = mapped_column(String(255), nullable=False)
    source_b_id: Mapped[str] = mapped_column(String(255), nullable=False)
    conflicting_claim: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="surfaced", index=True) # surfaced, investigating, resolved

class TransformationGraphSnapshot(Base):
    __tablename__ = "transformation_graph_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    snapshot_label: Mapped[str] = mapped_column(String(255), nullable=False)
    nodes_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    edges_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationGraphDiff(Base):
    __tablename__ = "transformation_graph_diffs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    snapshot_a_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    snapshot_b_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    added_edges_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    removed_edges_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    new_conflicts_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    resolved_conflicts_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class TransformationBottleneckCluster(Base):
    __tablename__ = "transformation_bottleneck_clusters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shared_bottleneck_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    transformation_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    downstream_exposure_range: Mapped[str] = mapped_column(String(100), nullable=False, default="14-30 days delay")

class TransformationForesightDomain(Base):
    __tablename__ = "transformation_foresight_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="medium_term", index=True) # near_term, medium_term, long_term, extended
    scope: Mapped[str] = mapped_column(String(255), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationFutureDriver(Base):
    __tablename__ = "transformation_future_drivers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    driver_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # technology, market, customer, regulation, competition, capacity, talent, vendor, geopolitical, economic, operational, strategic
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)

class TransformationDriverTrend(Base):
    __tablename__ = "transformation_driver_trends"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    driver_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    direction: Mapped[str] = mapped_column(String(50), nullable=False, default="increasing", index=True) # increasing, decreasing, stable, fluctuating
    velocity: Mapped[float] = mapped_column(Float, nullable=False, default=0.75)
    acceleration: Mapped[float] = mapped_column(Float, nullable=False, default=0.15)
    uncertainty_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.20)

class TransformationWeakSignal(Base):
    __tablename__ = "transformation_weak_signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    signal_text: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    possible_meaning: Mapped[Text] = mapped_column(Text, nullable=False)
    alternative_interpretations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.65, index=True)

class TransformationEmergingPattern(Base):
    __tablename__ = "transformation_emerging_patterns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    pattern_name: Mapped[str] = mapped_column(String(255), nullable=False)
    signals_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    frequency: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.88, index=True)
    time_window: Mapped[str] = mapped_column(String(100), nullable=False, default="90_days")

class TransformationFutureState(Base):
    __tablename__ = "transformation_future_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    state_type: Mapped[str] = mapped_column(String(50), nullable=False, default="baseline", index=True) # baseline, alternative, stress, disruptive, opportunity
    variables_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    description: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationScenarioImpact(Base):
    __tablename__ = "transformation_scenario_impacts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    transformation_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    impact_range_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict) # low, expected, high
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)

class TransformationSecondOrderEffect(Base):
    __tablename__ = "transformation_second_order_effects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_impact_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    propagation_path_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)

class TransformationVulnerabilityProfile(Base):
    __tablename__ = "transformation_vulnerability_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transformation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    vulnerability_dimensions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict) # dependency, capacity, technology, assumption, risk, optionality, reversibility
    overall_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.18)

class TransformationOpportunityProfile(Base):
    __tablename__ = "transformation_opportunity_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transformation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    opportunity_type: Mapped[str] = mapped_column(String(100), nullable=False) # new_capability, new_market, new_efficiency, new_resilience, new_strategic_option
    potential_benefit: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.91)

class TransformationNoRegretAction(Base):
    __tablename__ = "transformation_no_regret_actions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    action_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    multiscenario_utility: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    reversibility: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    downside_risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")

class TransformationContingentAction(Base):
    __tablename__ = "transformation_contingent_actions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trigger_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    predefined_option_desc: Mapped[Text] = mapped_column(Text, nullable=False)
    approval_status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending_review", index=True)

class TransformationForesightThreshold(Base):
    __tablename__ = "transformation_foresight_thresholds"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_name: Mapped[str] = mapped_column(String(255), nullable=False)
    threshold_value: Mapped[float] = mapped_column(Float, nullable=False, default=0.80)
    direction: Mapped[str] = mapped_column(String(50), nullable=False, default="above")
    action_recommendation: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationForesightTrigger(Base):
    __tablename__ = "transformation_foresight_triggers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    threshold_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="inactive", index=True) # inactive, watching, triggered, resolved
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class TransformationScenarioAssumptionDrift(Base):
    __tablename__ = "transformation_scenario_assumption_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    assumption_text: Mapped[Text] = mapped_column(Text, nullable=False)
    drift_type: Mapped[str] = mapped_column(String(50), nullable=False, default="weakening", index=True) # strengthening, weakening, invalidating, uncertain

class TransformationForecastVersion(Base):
    __tablename__ = "transformation_forecast_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version_tag: Mapped[str] = mapped_column(String(100), nullable=False)
    prediction_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    model_version: Mapped[str] = mapped_column(String(100), nullable=False, default="vpr_foresight_v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationForecastError(Base):
    __tablename__ = "transformation_forecast_errors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forecast_version_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    actual_outcome_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    error_magnitude: Mapped[float] = mapped_column(Float, nullable=False, default=0.04)
    direction: Mapped[str] = mapped_column(String(50), nullable=False, default="overestimate")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationForesightReview(Base):
    __tablename__ = "transformation_foresight_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    review_cadence: Mapped[str] = mapped_column(String(50), nullable=False, default="monthly") # event_driven, weekly, monthly, quarterly
    summary_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationDecisionCase(Base):
    __tablename__ = "transformation_decision_cases"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    decision_type: Mapped[str] = mapped_column(String(50), nullable=False, default="scale", index=True) # start, stop, continue, pause, resume, sequence, resequence, scale, pilot, expand, reduce_scope, change_design, accept_risk, mitigate_risk, change_dependency, change_target_state
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="analysis", index=True) # draft, evidence_collection, analysis, ready, under_review, decided, approved, executing, verified, closed, reopened
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationDecisionQuestion(Base):
    __tablename__ = "transformation_decision_questions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    question_text: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationEvidencePack(Base):
    __tablename__ = "transformation_evidence_packs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    summary_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    quality_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)

class TransformationEvidenceItem(Base):
    __tablename__ = "transformation_evidence_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evidence_pack_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # fact, observation, measurement, forecast, scenario, document, decision_history, graph_relationship, expert_input
    source: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    value_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    freshness: Mapped[str] = mapped_column(String(50), nullable=False, default="realtime")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    provenance: Mapped[str] = mapped_column(String(255), nullable=False)

class TransformationEvidenceConflict(Base):
    __tablename__ = "transformation_evidence_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_a: Mapped[str] = mapped_column(String(255), nullable=False)
    source_b: Mapped[str] = mapped_column(String(255), nullable=False)
    conflicting_claim: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="surfaced", index=True) # surfaced, under_review, resolved

class TransformationDecisionAssumption(Base):
    __tablename__ = "transformation_decision_assumptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    assumption_text: Mapped[Text] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="valid", index=True) # valid, questioned, fragile, invalidated, unknown
    impact: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class TransformationDecisionOption(Base):
    __tablename__ = "transformation_decision_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    expected_outcome: Mapped[Text] = mapped_column(Text, nullable=False)
    risks_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    cost: Mapped[str] = mapped_column(String(100), nullable=False, default="$150,000")
    capacity: Mapped[str] = mapped_column(String(100), nullable=False, default="4 FTEs")
    timing: Mapped[str] = mapped_column(String(100), nullable=False, default="Q3 2026")
    reversibility: Mapped[str] = mapped_column(String(50), nullable=False, default="partially_reversible", index=True) # reversible, partially_reversible, hard_to_reverse, irreversible

class TransformationDecisionTradeoff(Base):
    __tablename__ = "transformation_decision_tradeoffs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    option_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    benefit_gained: Mapped[Text] = mapped_column(Text, nullable=False)
    cost_incurred: Mapped[Text] = mapped_column(Text, nullable=False)
    risk_accepted: Mapped[Text] = mapped_column(Text, nullable=False)
    optionality_lost: Mapped[Text] = mapped_column(Text, nullable=False)
    optionality_gained: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationDecisionRecommendation(Base):
    __tablename__ = "transformation_decision_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    recommended_option_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    rationale_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence_references_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True) # high, medium, low, insufficient_evidence

class TransformationDecisionPacket(Base):
    __tablename__ = "transformation_decision_packets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version_tag: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")
    packet_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationDecisionReadiness(Base):
    __tablename__ = "transformation_decision_readinesses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="ready", index=True) # ready, insufficient_evidence, missing_approvals
    readiness_dimensions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class TransformationDecisionValue(Base):
    __tablename__ = "transformation_decision_values"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expected_strategic_value: Mapped[Text] = mapped_column(Text, nullable=False)
    expected_benefit: Mapped[Text] = mapped_column(Text, nullable=False)
    risk_reduction: Mapped[Text] = mapped_column(Text, nullable=False)
    optionality: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationInformationAction(Base):
    __tablename__ = "transformation_information_actions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String(100), nullable=False) # run_pilot, collect_metric, validate_dependency, test_assumption, conduct_assessment
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    information_gain_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class TransformationDecisionLearning(Base):
    __tablename__ = "transformation_decision_learnings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    prediction_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    actual_outcome_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    lesson_text: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationDecisionReassessment(Base):
    __tablename__ = "transformation_decision_reassessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    reassessment_reason: Mapped[Text] = mapped_column(Text, nullable=False)
    changed_evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="reassessing", index=True)

class TransformationDecisionDrift(Base):
    __tablename__ = "transformation_decision_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    approved_decision_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    implemented_decision_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    drift_severity: Mapped[str] = mapped_column(String(50), nullable=False, default="minor", index=True)

class TransformationDecisionLifecycle(Base):
    __tablename__ = "transformation_decision_lifecycles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    current_stage: Mapped[str] = mapped_column(String(50), nullable=False, default="learning", index=True) # question, evidence, analysis, recommendation, decision, approval, execution, verification, learning, closed, reopened
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_transition_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")

class TransformationDecisionStageTransition(Base):
    __tablename__ = "transformation_decision_stage_transitions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lifecycle_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    from_stage: Mapped[str] = mapped_column(String(50), nullable=False)
    to_stage: Mapped[str] = mapped_column(String(50), nullable=False)
    actor: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")
    decision_packet_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")

class TransformationDecisionBaseline(Base):
    __tablename__ = "transformation_decision_baselines"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expected_benefits_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    expected_risks_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    expected_timing_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    expected_capacity_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    expected_dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    expected_scenario: Mapped[str] = mapped_column(String(100), nullable=False, default="baseline")
    expected_outcome: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationDecisionExpectedOutcome(Base):
    __tablename__ = "transformation_decision_expected_outcomes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    metric: Mapped[str] = mapped_column(String(100), nullable=False)
    target: Mapped[str] = mapped_column(String(100), nullable=False)
    range_str: Mapped[str] = mapped_column(String(100), nullable=False, default="30-35%")
    time_horizon: Mapped[str] = mapped_column(String(100), nullable=False, default="90 days")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    source: Mapped[str] = mapped_column(String(255), nullable=False)

class TransformationDecisionActualOutcome(Base):
    __tablename__ = "transformation_decision_actual_outcomes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    metric: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[str] = mapped_column(String(100), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.98)

class TransformationDecisionVariance(Base):
    __tablename__ = "transformation_decision_variances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expected: Mapped[str] = mapped_column(String(100), nullable=False)
    actual: Mapped[str] = mapped_column(String(100), nullable=False)
    difference: Mapped[str] = mapped_column(String(100), nullable=False)
    direction: Mapped[str] = mapped_column(String(50), nullable=False, default="favorable") # favorable, unfavorable, neutral
    materiality: Mapped[str] = mapped_column(String(50), nullable=False, default="minor", index=True) # minor, moderate, material, critical
    variance_type: Mapped[str] = mapped_column(String(50), nullable=False, default="benefit") # benefit, cost, timing, risk, capacity, quality, adoption, dependency, strategic

class TransformationDecisionAssumptionOutcome(Base):
    __tablename__ = "transformation_decision_assumption_outcomes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    assumption: Mapped[Text] = mapped_column(Text, nullable=False)
    original_status: Mapped[str] = mapped_column(String(50), nullable=False, default="valid")
    actual_state: Mapped[str] = mapped_column(String(50), nullable=False, default="valid") # valid, weaker, stronger, invalidated, unknown
    impact: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationRecommendationOutcome(Base):
    __tablename__ = "transformation_recommendation_outcomes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    recommendation: Mapped[Text] = mapped_column(Text, nullable=False)
    decision: Mapped[Text] = mapped_column(Text, nullable=False)
    result: Mapped[Text] = mapped_column(Text, nullable=False)
    alignment: Mapped[str] = mapped_column(String(50), nullable=False, default="aligned")

class TransformationDecisionLesson(Base):
    __tablename__ = "transformation_decision_lessons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson: Mapped[Text] = mapped_column(Text, nullable=False)
    source_decision: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evidence: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True) # high, medium, low, emerging
    scope: Mapped[str] = mapped_column(String(50), nullable=False, default="enterprise_relevant", index=True) # decision_specific, transformation_specific, capability_specific, portfolio_specific, enterprise_relevant
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationDecisionPattern(Base):
    __tablename__ = "transformation_decision_patterns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pattern: Mapped[Text] = mapped_column(Text, nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False, default=12, index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    limitations: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationDecisionLearningReview(Base):
    __tablename__ = "transformation_decision_learning_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="approved", index=True) # candidate, under_review, approved, rejected
    reviewer: Mapped[str] = mapped_column(String(255), nullable=False)
    feedback: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationDecisionCounterfactual(Base):
    __tablename__ = "transformation_decision_counterfactuals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    actual_path: Mapped[Text] = mapped_column(Text, nullable=False)
    alternative_path: Mapped[Text] = mapped_column(Text, nullable=False)
    assumptions: Mapped[Text] = mapped_column(Text, nullable=False)
    uncertainty: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")

class TransformationDecisionRegretAnalysis(Base):
    __tablename__ = "transformation_decision_regret_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    missed_benefit: Mapped[Text] = mapped_column(Text, nullable=False)
    avoidable_risk: Mapped[Text] = mapped_column(Text, nullable=False)
    timing_loss: Mapped[Text] = mapped_column(Text, nullable=False)
    optionality_loss: Mapped[Text] = mapped_column(Text, nullable=False)
    uncertainty: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")

class TransformationDecisionSuccessCondition(Base):
    __tablename__ = "transformation_decision_success_conditions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    condition_text: Mapped[Text] = mapped_column(Text, nullable=False)
    metric_target: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="verified")

class TransformationDecisionFailureAnalysis(Base):
    __tablename__ = "transformation_decision_failure_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    decision_effect: Mapped[Text] = mapped_column(Text, nullable=False)
    execution_effect: Mapped[Text] = mapped_column(Text, nullable=False)
    assumption_effect: Mapped[Text] = mapped_column(Text, nullable=False)
    external_effect: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationDecisionQualityReview(Base):
    __tablename__ = "transformation_decision_quality_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    cadence: Mapped[str] = mapped_column(String(50), nullable=False, default="post_transformation")
    evidence_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    forecast_accuracy: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    outcome_variance: Mapped[str] = mapped_column(String(50), nullable=False, default="favorable")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationGovernanceProfile(Base):
    __tablename__ = "transformation_governance_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # draft, active, under_review, proposed_change, approved_change, deprecated
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationGovernanceDomain(Base):
    __tablename__ = "transformation_governance_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    domain_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # strategy, portfolio, program, wave, decision, risk, benefit, capacity, execution, technology, data, security, compliance

class TransformationDecisionRight(Base):
    __tablename__ = "transformation_decision_rights"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    decision_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    scope: Mapped[str] = mapped_column(String(255), nullable=False)
    authority_level: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    required_evidence: Mapped[Text] = mapped_column(Text, nullable=False)
    approval_requirement: Mapped[Text] = mapped_column(Text, nullable=False)
    escalation_requirement: Mapped[Text] = mapped_column(Text, nullable=False)
    delegation_allowed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class TransformationDecisionRightMatrix(Base):
    __tablename__ = "transformation_decision_right_matrices"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    decision_type: Mapped[str] = mapped_column(String(100), nullable=False)
    authority_level: Mapped[str] = mapped_column(String(100), nullable=False)
    approval_rule: Mapped[Text] = mapped_column(Text, nullable=False)
    escalation_rule: Mapped[Text] = mapped_column(Text, nullable=False)
    delegation_rule: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationDecisionRightConflict(Base):
    __tablename__ = "transformation_decision_right_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    authority_a: Mapped[str] = mapped_column(String(255), nullable=False)
    authority_b: Mapped[str] = mapped_column(String(255), nullable=False)
    conflict_description: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="surfaced", index=True)

class TransformationGovernanceControl(Base):
    __tablename__ = "transformation_governance_controls"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    control_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # approval, segregation, evidence_requirement, threshold, escalation, review, audit, simulation, reconciliation, verification
    purpose: Mapped[Text] = mapped_column(Text, nullable=False)
    scope: Mapped[str] = mapped_column(String(255), nullable=False)
    trigger: Mapped[str] = mapped_column(String(255), nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    policy_reference: Mapped[str] = mapped_column(String(255), nullable=False)
    effectiveness_method: Mapped[str] = mapped_column(String(255), nullable=False)

class TransformationGovernanceFriction(Base):
    __tablename__ = "transformation_governance_frictions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    friction_type: Mapped[str] = mapped_column(String(100), nullable=False)
    cause: Mapped[Text] = mapped_column(Text, nullable=False)
    affected_decisions: Mapped[Text] = mapped_column(Text, nullable=False)
    time_impact_hours: Mapped[float] = mapped_column(Float, nullable=False, default=48.0)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="moderate", index=True)

class TransformationGovernanceGap(Base):
    __tablename__ = "transformation_governance_gaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    gap_type: Mapped[str] = mapped_column(String(100), nullable=False)
    risk_description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    recommendation: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationGovernanceOvercontrol(Base):
    __tablename__ = "transformation_governance_overcontrols"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    control_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    overcontrol_reason: Mapped[Text] = mapped_column(Text, nullable=False)
    recommendation: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationGovernanceLoad(Base):
    __tablename__ = "transformation_governance_loads"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    decisions_count: Mapped[int] = mapped_column(Integer, nullable=False, default=24)
    approvals_count: Mapped[int] = mapped_column(Integer, nullable=False, default=18)
    reviews_count: Mapped[int] = mapped_column(Integer, nullable=False, default=8)
    escalations_count: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    exceptions_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    time_spent_hours: Mapped[float] = mapped_column(Float, nullable=False, default=36.5)
    time_window: Mapped[str] = mapped_column(String(50), nullable=False, default="monthly", index=True)

class TransformationGovernanceBottleneck(Base):
    __tablename__ = "transformation_governance_bottlenecks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    bottleneck_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # approval, authority, evidence, review, policy, capacity, escalation
    cause: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="moderate")

class TransformationDelegationCandidate(Base):
    __tablename__ = "transformation_delegation_candidates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    decision_type: Mapped[str] = mapped_column(String(100), nullable=False)
    rationale: Mapped[Text] = mapped_column(Text, nullable=False)
    safety_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    policy_coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.98)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="recommended", index=True)

class TransformationEscalationPattern(Base):
    __tablename__ = "transformation_escalation_patterns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    pattern_description: Mapped[Text] = mapped_column(Text, nullable=False)
    frequency: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    impact: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationGovernanceException(Base):
    __tablename__ = "transformation_governance_exceptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    scope: Mapped[str] = mapped_column(String(255), nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    approver: Mapped[str] = mapped_column(String(255), nullable=False)
    risk: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class TransformationGovernanceChangeRequest(Base):
    __tablename__ = "transformation_governance_change_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    change_type: Mapped[str] = mapped_column(String(100), nullable=False) # decision_right, approval, threshold, control, escalation, delegation, review, evidence_requirement
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    proposed_state: Mapped[Text] = mapped_column(Text, nullable=False)
    simulation_results_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="under_review", index=True) # under_review, approved, rejected, executed

class TransformationGovernanceDrift(Base):
    __tablename__ = "transformation_governance_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    drift_type: Mapped[str] = mapped_column(String(50), nullable=False) # process, authority, policy, approval, control, exception, execution
    approved_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    actual_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="minor", index=True)

class TransformationGovernanceReview(Base):
    __tablename__ = "transformation_governance_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    cadence: Mapped[str] = mapped_column(String(50), nullable=False, default="quarterly")
    trigger_reason: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="recommended", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationGovernanceLesson(Base):
    __tablename__ = "transformation_governance_lessons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    control_id: Mapped[str] = mapped_column(String(255), nullable=False)
    event: Mapped[Text] = mapped_column(Text, nullable=False)
    outcome: Mapped[Text] = mapped_column(Text, nullable=False)
    lesson: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class TransformationGovernancePattern(Base):
    __tablename__ = "transformation_governance_patterns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    pattern_description: Mapped[Text] = mapped_column(Text, nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)

class TransformationDigitalTwin(Base):
    __tablename__ = "transformation_digital_twins"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise") # enterprise, portfolio, transformation, program, business_unit, capability
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    baseline_snapshot_id: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # draft, active, simulating, review, archived
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationTwinBaseline(Base):
    __tablename__ = "transformation_twin_baselines"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    twin_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    strategy_state_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    operating_model_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    portfolio_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    governance_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    capacity_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    dependencies_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    risks_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    benefits_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    kpis_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class TransformationTwinSnapshot(Base):
    __tablename__ = "transformation_twin_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    twin_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    source_versions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    included_systems_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    data_freshness_minutes: Mapped[float] = mapped_column(Float, nullable=False, default=5.0)

class TransformationTwinState(Base):
    __tablename__ = "transformation_twin_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    twin_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    state_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # current, proposed, alternative, stress
    state_data_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class TransformationSimulationChangeSet(Base):
    __tablename__ = "transformation_simulation_change_sets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    twin_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    changes_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="validated", index=True)

class TransformationSimulationRun(Base):
    __tablename__ = "transformation_simulation_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    twin_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    baseline_state_id: Mapped[str] = mapped_column(String(255), nullable=False)
    proposed_state_id: Mapped[str] = mapped_column(String(255), nullable=False)
    scenario: Mapped[str] = mapped_column(String(100), nullable=False, default="baseline") # baseline, optimistic, stress, disruptive, custom
    model_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="completed", index=True) # queued, running, completed, failed, cancelled, stale
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    hash_fingerprint: Mapped[str] = mapped_column(String(255), nullable=False, default="hash_sim_01")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationSimulationModel(Base):
    __tablename__ = "transformation_simulation_models"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # dependency_propagation, capacity, timeline, risk, benefit, governance, scenario, portfolio, operating_model, combined
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    assumptions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    parameters_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    evaluation_status: Mapped[str] = mapped_column(String(50), nullable=False, default="validated")
    limitations: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationSimulationInput(Base):
    __tablename__ = "transformation_simulation_inputs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    entity: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[Text] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    assumption: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationSimulationOutput(Base):
    __tablename__ = "transformation_simulation_outputs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    metric: Mapped[str] = mapped_column(String(100), nullable=False)
    low_value: Mapped[float] = mapped_column(Float, nullable=False)
    expected_value: Mapped[float] = mapped_column(Float, nullable=False)
    high_value: Mapped[float] = mapped_column(Float, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    time_horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="Q4 2026", index=True)
    scenario: Mapped[str] = mapped_column(String(100), nullable=False, default="baseline")

class TransformationMultiScenarioRun(Base):
    __tablename__ = "transformation_multi_scenario_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    twin_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    change_set_id: Mapped[str] = mapped_column(String(255), nullable=False)
    scenarios_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    robustness_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="completed")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationSimulationComparison(Base):
    __tablename__ = "transformation_simulation_comparisons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    current_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    proposed_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    alternative_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    comparison_dimensions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class TransformationSimulationTradeoff(Base):
    __tablename__ = "transformation_simulation_tradeoffs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    benefit_gained: Mapped[Text] = mapped_column(Text, nullable=False)
    risk_gained: Mapped[Text] = mapped_column(Text, nullable=False)
    cost_impact: Mapped[float] = mapped_column(Float, nullable=False, default=150000.0)
    delay_days: Mapped[float] = mapped_column(Float, nullable=False, default=14.0)
    optionality_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)

class TransformationSensitivityAnalysis(Base):
    __tablename__ = "transformation_sensitivity_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    variable_name: Mapped[str] = mapped_column(String(255), nullable=False)
    low_value: Mapped[float] = mapped_column(Float, nullable=False)
    expected_value: Mapped[float] = mapped_column(Float, nullable=False)
    high_value: Mapped[float] = mapped_column(Float, nullable=False)
    impact_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationSimulationReview(Base):
    __tablename__ = "transformation_simulation_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    decision_impact: Mapped[Text] = mapped_column(Text, nullable=False)
    limitations: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="approved")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationWarRoom(Base):
    __tablename__ = "transformation_war_rooms"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise") # enterprise, portfolio, transformation, program, wave, business_unit
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="monitoring", index=True) # inactive, monitoring, attention, active_response, review, closed
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True) # low, medium, high, critical
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationWarRoomLiveState(Base):
    __tablename__ = "transformation_war_room_live_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    war_room_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    milestones_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    dependencies_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    risks_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    benefits_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    capacity_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    governance_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    kpis_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    source_versions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    staleness_status: Mapped[str] = mapped_column(String(50), nullable=False, default="fresh") # fresh, lagging, stale

class TransformationPlanVariance(Base):
    __tablename__ = "transformation_plan_variances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    war_room_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    variance_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # schedule, scope, cost, capacity, dependency, risk, benefit, quality, governance, adoption
    planned_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    actual_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    forecast_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)

class TransformationDeviation(Base):
    __tablename__ = "transformation_deviations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    war_room_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    entity: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    metric: Mapped[str] = mapped_column(String(100), nullable=False)
    expected_value: Mapped[float] = mapped_column(Float, nullable=False)
    actual_value: Mapped[float] = mapped_column(Float, nullable=False)
    variance_value: Mapped[float] = mapped_column(Float, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True) # low, medium, high, critical
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)

class TransformationRootCauseHypothesis(Base):
    __tablename__ = "transformation_root_cause_hypotheses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    war_room_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    deviation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    hypothesis_text: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.88, index=True)
    alternative_explanations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class TransformationLiveImpactAssessment(Base):
    __tablename__ = "transformation_live_impact_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    war_room_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    affected_transformations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_capabilities_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_benefits_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_risks_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    strategic_impact: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationInterventionOption(Base):
    __tablename__ = "transformation_intervention_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    war_room_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    intervention_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # monitor, investigate, resequence, pause, accelerate, reduce_scope, increase_capacity, change_dependency, mitigate_risk, pilot, escalate
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    safety_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    reversibility_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    blast_radius_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="proposed", index=True) # proposed, simulated, recommended, approved, executing, completed, rejected

class TransformationInterventionRecommendation(Base):
    __tablename__ = "transformation_intervention_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    war_room_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    recommended_option_id: Mapped[str] = mapped_column(String(255), nullable=False)
    evidence_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    risk_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    uncertainty_level: Mapped[str] = mapped_column(String(50), nullable=False, default="low")
    alternatives_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class TransformationWarRoomEscalation(Base):
    __tablename__ = "transformation_war_room_escalations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    war_room_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger_reason: Mapped[Text] = mapped_column(Text, nullable=False)
    escalation_path: Mapped[str] = mapped_column(String(255), nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="critical")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="escalated", index=True) # escalated, acknowledged, resolved

class TransformationResponsePlan(Base):
    __tablename__ = "transformation_response_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    war_room_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    signal_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    assessment_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    options_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    decision_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", index=True) # draft, analysis, awaiting_decision, awaiting_approval, approved, executing, verified, cancelled, closed

class TransformationResponseCheckpoint(Base):
    __tablename__ = "transformation_response_checkpoints"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    response_plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    checkpoint_name: Mapped[str] = mapped_column(String(255), nullable=False)
    expected_state: Mapped[Text] = mapped_column(Text, nullable=False)
    actual_state: Mapped[Text] = mapped_column(Text, nullable=False)
    next_checkpoint: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")

class TransformationTrajectory(Base):
    __tablename__ = "transformation_trajectories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    war_room_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    metric: Mapped[str] = mapped_column(String(100), nullable=False)
    trajectory_data_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    time_horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="Q4 2026")
    scenario: Mapped[str] = mapped_column(String(100), nullable=False, default="baseline")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)

class TransformationEarlyWarning(Base):
    __tablename__ = "transformation_early_warnings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    war_room_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    signal_name: Mapped[str] = mapped_column(String(255), nullable=False)
    signal_strength: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    historical_reliability: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    model_confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class TransformationSituationSummary(Base):
    __tablename__ = "transformation_situation_summaries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    war_room_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    what_changed: Mapped[Text] = mapped_column(Text, nullable=False)
    why_it_matters: Mapped[Text] = mapped_column(Text, nullable=False)
    affected_areas_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    uncertainty_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    recommended_review: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationRecoveryDomain(Base):
    __tablename__ = "transformation_recovery_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise") # enterprise, portfolio, transformation, program, wave, business_unit
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="prepared", index=True) # prepared, monitoring, degraded, recovery_active, stabilizing, recovering, verified, closed, review
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationDisruption(Base):
    __tablename__ = "transformation_disruptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    disruption_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # dependency_failure, capacity_loss, technology_failure, vendor_failure, data_issue, governance_failure, execution_failure, benefit_failure, risk_event, scenario_shock, external_event
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True) # low, medium, high, critical
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="confirmed", index=True) # observed, suspected, confirmed, resolved

class TransformationRecoveryImpact(Base):
    __tablename__ = "transformation_recovery_impacts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    disruption_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    affected_transformations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_capabilities_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_benefits_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    strategic_impact: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationRecoveryCriticality(Base):
    __tablename__ = "transformation_recovery_criticalities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    strategic_importance: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    dependency_centrality: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    benefit_exposure: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    recovery_urgency: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    reversibility: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)

class TransformationRecoveryPriority(Base):
    __tablename__ = "transformation_recovery_priorities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    priority_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.94, index=True)
    evidence_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    criteria_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class TransformationProtectionTarget(Base):
    __tablename__ = "transformation_protection_targets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_type: Mapped[str] = mapped_column(String(100), nullable=False) # critical_capability, critical_dependency, critical_milestone, critical_benefit, critical_outcome
    target_name: Mapped[str] = mapped_column(String(255), nullable=False)
    protection_level: Mapped[str] = mapped_column(String(50), nullable=False, default="maximum")

class TransformationRecoveryObjective(Base):
    __tablename__ = "transformation_recovery_objectives"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    objective_name: Mapped[str] = mapped_column(String(255), nullable=False)
    target_recovery_time_hours: Mapped[float] = mapped_column(Float, nullable=False, default=72.0)
    estimated_range_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.93)

class TransformationRecoveryPath(Base):
    __tablename__ = "transformation_recovery_paths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    path_name: Mapped[str] = mapped_column(String(255), nullable=False)
    action_sequence_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="proposed", index=True) # proposed, simulated, recommended, approved, executing, completed, rejected

class TransformationRecoveryOption(Base):
    __tablename__ = "transformation_recovery_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    option_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # restore, reroute, substitute, degrade_gracefully, pause, resequence, rollback, isolate, accelerate_recovery
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    safety_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.91)
    secondary_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="simulated", index=True)

class TransformationRecoveryBottleneck(Base):
    __tablename__ = "transformation_recovery_bottlenecks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    bottleneck_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # capacity, dependency, decision, approval, technology, vendor, data, execution
    entity_name: Mapped[str] = mapped_column(String(255), nullable=False)
    impact_description: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationRecoveryTrajectory(Base):
    __tablename__ = "transformation_recovery_trajectories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    path_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    metric: Mapped[str] = mapped_column(String(100), nullable=False)
    trajectory_data_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)

class TransformationRecoveryComparison(Base):
    __tablename__ = "transformation_recovery_comparisons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    compared_path_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    time_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.08)
    cost_score: Mapped[float] = mapped_column(Float, nullable=False, default=120000.0)
    reversibility_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)

class TransformationRecoveryCheckpoint(Base):
    __tablename__ = "transformation_recovery_checkpoints"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    checkpoint_name: Mapped[str] = mapped_column(String(255), nullable=False)
    expected_state: Mapped[Text] = mapped_column(Text, nullable=False)
    actual_state: Mapped[Text] = mapped_column(Text, nullable=False)
    next_decision_point: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")

class TransformationRecoveryGate(Base):
    __tablename__ = "transformation_recovery_gates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    gate_name: Mapped[str] = mapped_column(String(255), nullable=False)
    criteria_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, verified, passed, failed

class TransformationReturnToNormalPlan(Base):
    __tablename__ = "transformation_return_to_normal_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    criteria_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    action_sequence_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", index=True) # draft, approved, active, verified, closed

class TransformationRecoveryDrift(Base):
    __tablename__ = "transformation_recovery_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expected_action: Mapped[Text] = mapped_column(Text, nullable=False)
    actual_action: Mapped[Text] = mapped_column(Text, nullable=False)
    drift_severity: Mapped[str] = mapped_column(String(50), nullable=False, default="low")

class TransformationRecoveryEscalation(Base):
    __tablename__ = "transformation_recovery_escalations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger_reason: Mapped[Text] = mapped_column(Text, nullable=False)
    escalation_path: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="escalated", index=True)

class TransformationRecoveryCommunication(Base):
    __tablename__ = "transformation_recovery_communications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    audience: Mapped[str] = mapped_column(String(255), nullable=False)
    message_text: Mapped[Text] = mapped_column(Text, nullable=False)
    approval_status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft")

class TransformationResilienceGap(Base):
    __tablename__ = "transformation_resilience_gaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    gap_type: Mapped[str] = mapped_column(String(100), nullable=False) # missing_redundancy, single_point_dependency, insufficient_capacity, weak_recovery_path, unclear_ownership, governance_bottleneck
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class TransformationResilienceImprovement(Base):
    __tablename__ = "transformation_resilience_improvements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    improvement_type: Mapped[str] = mapped_column(String(100), nullable=False) # redundancy, substitution, capacity_buffer, dependency_diversification, process_change, governance_change, technology_change, training, simulation
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    recommendation_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class TransformationRecoveryReadiness(Base):
    __tablename__ = "transformation_recovery_readinesses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    readiness_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    dimension_scores_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationRecoveryDrill(Base):
    __tablename__ = "transformation_recovery_drills"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    drill_name: Mapped[str] = mapped_column(String(255), nullable=False)
    scenario_description: Mapped[Text] = mapped_column(Text, nullable=False)
    results_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    no_production_mutation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceEngineeringDomain(Base):
    __tablename__ = "transformation_resilience_engineering_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise") # enterprise, portfolio, transformation, program, wave, business_unit
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="baseline", index=True) # baseline, monitoring, degraded, improvement_planned, improvement_active, verified, review
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceBaseline(Base):
    __tablename__ = "transformation_resilience_baselines"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    robustness_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.91)
    redundancy_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.86)
    recoverability_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    adaptability_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.89)
    optionality_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    observability_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    governability_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)

class TransformationFailureMode(Base):
    __tablename__ = "transformation_failure_modes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    failure_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # single_dependency, capacity_shortage, governance_bottleneck, decision_delay, technology_failure, data_failure, vendor_failure, skill_dependency, sequencing_failure, benefit_dependency, scenario_shock
    frequency: Mapped[int] = mapped_column(Integer, nullable=False, default=3, index=True)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    recovery_time_hours: Mapped[float] = mapped_column(Float, nullable=False, default=48.0)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.93)

class TransformationFailureModeAnalysis(Base):
    __tablename__ = "transformation_failure_mode_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    failure_mode_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger_description: Mapped[Text] = mapped_column(Text, nullable=False)
    conditions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    propagation_path_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    recovery_behavior: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationSystemicWeakness(Base):
    __tablename__ = "transformation_systemic_weaknesses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    affected_transformations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_capabilities_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)

class TransformationSinglePointOfFailure(Base):
    __tablename__ = "transformation_single_points_of_failure"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False) # vendor, capability, dependency, system, approval_path, recovery_path
    entity_name: Mapped[str] = mapped_column(String(255), nullable=False)
    criticality_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.95, index=True)

class TransformationRedundancyOption(Base):
    __tablename__ = "transformation_redundancy_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    redundancy_type: Mapped[str] = mapped_column(String(100), nullable=False) # dependency, capacity, process, technology, governance, recovery_path
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    cost_estimate: Mapped[float] = mapped_column(Float, nullable=False, default=150000.0)
    risk_reduction_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.88, index=True)

class TransformationSubstitutionOption(Base):
    __tablename__ = "transformation_substitution_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    substitution_type: Mapped[str] = mapped_column(String(100), nullable=False) # vendor, capability, technology, process, dependency
    primary_entity: Mapped[str] = mapped_column(String(255), nullable=False)
    substitute_entity: Mapped[str] = mapped_column(String(255), nullable=False)
    feasibility_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)

class TransformationCapacityBufferOption(Base):
    __tablename__ = "transformation_capacity_buffer_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    required_buffer_fte: Mapped[float] = mapped_column(Float, nullable=False, default=15.0)
    cost_estimate: Mapped[float] = mapped_column(Float, nullable=False, default=180000.0)
    activation_condition: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationOptionalityAnalysis(Base):
    __tablename__ = "transformation_optionality_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    path_count: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    dimension_scores_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceInvestmentCandidate(Base):
    __tablename__ = "transformation_resilience_investment_candidates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    problem_statement: Mapped[Text] = mapped_column(Text, nullable=False)
    improvement_title: Mapped[str] = mapped_column(String(255), nullable=False)
    investment_amount: Mapped[float] = mapped_column(Float, nullable=False, default=250000.0)
    expected_benefit: Mapped[Text] = mapped_column(Text, nullable=False)
    risk_reduction_pct: Mapped[float] = mapped_column(Float, nullable=False, default=45.0)
    uncertainty_level: Mapped[str] = mapped_column(String(50), nullable=False, default="low", index=True)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)

class TransformationCascadingFailureAnalysis(Base):
    __tablename__ = "transformation_cascading_failure_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    initial_trigger: Mapped[Text] = mapped_column(Text, nullable=False)
    propagation_graph_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    uncertainty_label: Mapped[str] = mapped_column(String(100), nullable=False, default="estimated")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceIntervention(Base):
    __tablename__ = "transformation_resilience_interventions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    intervention_type: Mapped[str] = mapped_column(String(100), nullable=False) # redundancy, buffer, substitution, decoupling, sequencing, governance, monitoring, recovery, simulation
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    priority_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    recommendation_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class TransformationResilienceRoadmap(Base):
    __tablename__ = "transformation_resilience_roadmaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    milestones_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    investment_total: Mapped[float] = mapped_column(Float, nullable=False, default=430000.0)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", index=True) # draft, approved, in_progress, verified

class TransformationResilienceComparison(Base):
    __tablename__ = "transformation_resilience_comparisons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    baseline_scores_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    improved_scores_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    actual_scores_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class TransformationResilienceLesson(Base):
    __tablename__ = "transformation_resilience_lessons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    failure_trigger: Mapped[Text] = mapped_column(Text, nullable=False)
    observed_behavior: Mapped[Text] = mapped_column(Text, nullable=False)
    lesson_text: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)

class TransformationResiliencePattern(Base):
    __tablename__ = "transformation_resilience_patterns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    pattern_name: Mapped[str] = mapped_column(String(255), nullable=False)
    pattern_type: Mapped[str] = mapped_column(String(100), nullable=False) # failure_mode, recovery_bottleneck, successful_intervention, weak_dependency
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95, index=True)

class TransformationResilienceWarning(Base):
    __tablename__ = "transformation_resilience_warnings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    warning_signal: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    metrics_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)


class TransformationResiliencePortfolio(Base):
    __tablename__ = "transformation_resilience_portfolios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise") # enterprise, multi_program, strategic_portfolio
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="baseline", index=True) # baseline, monitoring, optimization, review, approved_plan, executing, verification, closed
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationPortfolioResilienceExposure(Base):
    __tablename__ = "transformation_portfolio_resilience_exposures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    transformation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    exposure_type: Mapped[str] = mapped_column(String(100), nullable=False) # dependency, capacity, recovery, governance, benefit
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)

class TransformationSharedDependency(Base):
    __tablename__ = "transformation_shared_dependencies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dependency_name: Mapped[str] = mapped_column(String(255), nullable=False)
    affected_transformations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    criticality: Mapped[float] = mapped_column(Float, nullable=False, default=0.95, index=True)
    failure_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    substitution_options_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class TransformationSharedCapacityExposure(Base):
    __tablename__ = "transformation_shared_capacity_exposures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    capacity_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # engineering_fte, governance_board, cloud_quota, vendor_team
    affected_transformations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    required_capacity: Mapped[float] = mapped_column(Float, nullable=False)
    available_capacity: Mapped[float] = mapped_column(Float, nullable=False)
    contention_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)

class TransformationPortfolioCapacityConflict(Base):
    __tablename__ = "transformation_portfolio_capacity_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    conflicting_investments_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    capacity_resource: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)

class TransformationPortfolioFailurePattern(Base):
    __tablename__ = "transformation_portfolio_failure_patterns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    pattern_name: Mapped[str] = mapped_column(String(255), nullable=False)
    recurring_failure_type: Mapped[str] = mapped_column(String(100), nullable=False)
    affected_transformations_count: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.94, index=True)

class TransformationPortfolioSystemicRisk(Base):
    __tablename__ = "transformation_portfolio_systemic_risks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_dependency: Mapped[str] = mapped_column(String(255), nullable=False)
    affected_scope_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="critical", index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)

class TransformationPortfolioMultiFailureScenario(Base):
    __tablename__ = "transformation_portfolio_multi_failure_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    scenario_title: Mapped[str] = mapped_column(String(255), nullable=False)
    simultaneous_failures_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    correlated_propagation_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationPortfolioResilienceInvestment(Base):
    __tablename__ = "transformation_portfolio_resilience_investments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    investment_title: Mapped[str] = mapped_column(String(255), nullable=False)
    cost: Mapped[float] = mapped_column(Float, nullable=False, default=350000.0)
    protected_transformations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    risk_reduction_pct: Mapped[float] = mapped_column(Float, nullable=False, default=60.0)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)

class TransformationResilienceInvestmentOverlap(Base):
    __tablename__ = "transformation_resilience_investment_overlaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    overlapping_investments_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    duplicated_coverage_description: Mapped[Text] = mapped_column(Text, nullable=False)
    potential_savings: Mapped[float] = mapped_column(Float, nullable=False, default=120000.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceInvestmentGap(Base):
    __tablename__ = "transformation_resilience_investment_gaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    unprotected_systemic_exposure: Mapped[Text] = mapped_column(Text, nullable=False)
    affected_transformations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)

class TransformationResiliencePortfolioTradeoff(Base):
    __tablename__ = "transformation_resilience_portfolio_tradeoffs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    option_a_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    option_b_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    tradeoff_comparison_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceInvestmentSequence(Base):
    __tablename__ = "transformation_resilience_investment_sequences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    sequence_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1, index=True)
    investment_id: Mapped[str] = mapped_column(String(255), nullable=False)
    prerequisites_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class TransformationResilienceOptionValue(Base):
    __tablename__ = "transformation_resilience_option_values"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    option_name: Mapped[str] = mapped_column(String(255), nullable=False)
    flexibility_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.91)
    preserved_future_paths_count: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDiversificationPlan(Base):
    __tablename__ = "transformation_resilience_diversification_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    concentration_target: Mapped[str] = mapped_column(String(255), nullable=False)
    proposed_diversification: Mapped[Text] = mapped_column(Text, nullable=False)
    recommendation_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class TransformationPortfolioResilienceRoadmap(Base):
    __tablename__ = "transformation_portfolio_resilience_roadmaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    roadmap_title: Mapped[str] = mapped_column(String(255), nullable=False)
    milestones_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    total_budget: Mapped[float] = mapped_column(Float, nullable=False, default=750000.0)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft")

class TransformationPortfolioResilienceReview(Base):
    __tablename__ = "transformation_portfolio_resilience_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    review_trigger: Mapped[str] = mapped_column(String(255), nullable=False)
    summary_findings_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

# ------------------------------------------------------------------------------
# SPRINT 89 — ENTERPRISE TRANSFORMATION RESILIENCE SENSING 2.0 MODELS
# ------------------------------------------------------------------------------

class TransformationResilienceSensingDomain(Base):
    __tablename__ = "transformation_resilience_sensing_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceObservation(Base):
    __tablename__ = "transformation_resilience_observations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    metric: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    freshness: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="portfolio", index=True)

class TransformationResilienceObservationQuality(Base):
    __tablename__ = "transformation_resilience_observation_qualities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    observation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    completeness: Mapped[float] = mapped_column(Float, nullable=False, default=0.98)
    freshness: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    consistency: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    reliability: Mapped[float] = mapped_column(Float, nullable=False, default=0.96, index=True)

class TransformationResilienceSignalNormalization(Base):
    __tablename__ = "transformation_resilience_signal_normalizations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_metric: Mapped[str] = mapped_column(String(255), nullable=False)
    normalized_dimension: Mapped[str] = mapped_column(String(100), nullable=False)
    normalized_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)

class TransformationResilienceDynamicBaseline(Base):
    __tablename__ = "transformation_resilience_dynamic_baselines"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")
    effective_period: Mapped[str] = mapped_column(String(100), nullable=False, default="2026-Q3")
    change_reason: Mapped[Text] = mapped_column(Text, nullable=False)
    approval_context_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    baseline_metrics_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class TransformationResilienceDrift(Base):
    __tablename__ = "transformation_resilience_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    drift_type: Mapped[str] = mapped_column(String(50), nullable=False, default="persistent")
    metric_name: Mapped[str] = mapped_column(String(255), nullable=False)
    deviation_pct: Mapped[float] = mapped_column(Float, nullable=False, default=5.0)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceStructuralChange(Base):
    __tablename__ = "transformation_resilience_structural_changes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    change_type: Mapped[str] = mapped_column(String(100), nullable=False)
    affected_scope_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    materiality: Mapped[str] = mapped_column(String(50), nullable=False, default="material", index=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceAlertEvaluation(Base):
    __tablename__ = "transformation_resilience_alert_evaluations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    condition_name: Mapped[str] = mapped_column(String(255), nullable=False)
    persistence_count: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    corroboration_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    actionable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class TransformationResilienceSensingWarning(Base):
    __tablename__ = "transformation_resilience_sensing_warnings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    condition: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    affected_scope_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    recommended_review: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class TransformationResilienceSignalCorrelation(Base):
    __tablename__ = "transformation_resilience_signal_correlations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    signal_a: Mapped[str] = mapped_column(String(255), nullable=False)
    signal_b: Mapped[str] = mapped_column(String(255), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(50), nullable=False, default="observed_correlation")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.93, index=True)

class TransformationResilienceStateChange(Base):
    __tablename__ = "transformation_resilience_state_changes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    previous_state: Mapped[str] = mapped_column(String(50), nullable=False)
    new_state: Mapped[str] = mapped_column(String(50), nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceTrend(Base):
    __tablename__ = "transformation_resilience_trends"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dimension: Mapped[str] = mapped_column(String(100), nullable=False)
    trend_direction: Mapped[str] = mapped_column(String(50), nullable=False, default="stable")
    window: Mapped[str] = mapped_column(String(50), nullable=False, default="30d", index=True)

class TransformationResilienceForecast(Base):
    __tablename__ = "transformation_resilience_forecasts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_metric: Mapped[str] = mapped_column(String(255), nullable=False)
    forecast_value: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    uncertainty_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssumption(Base):
    __tablename__ = "transformation_resilience_assumptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    assumption_title: Mapped[str] = mapped_column(String(255), nullable=False)
    source_context: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="valid", index=True)

class TransformationResilienceAssumptionDrift(Base):
    __tablename__ = "transformation_resilience_assumption_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assumption_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    drift_description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    affected_scenarios_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class TransformationResilienceInvestmentReviewTrigger(Base):
    __tablename__ = "transformation_resilience_investment_review_triggers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    affected_investment_id: Mapped[str] = mapped_column(String(255), nullable=False)
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    review_deadline: Mapped[str] = mapped_column(String(100), nullable=False, default="2026-Q3")

class TransformationPortfolioResilienceState(Base):
    __tablename__ = "transformation_portfolio_resilience_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    robustness: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    redundancy: Mapped[float] = mapped_column(Float, nullable=False, default=0.91)
    recoverability: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    adaptability: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    optionality: Mapped[float] = mapped_column(Float, nullable=False, default=0.93)
    observability: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    governability: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

# ------------------------------------------------------------------------------
# SPRINT 90 — ENTERPRISE TRANSFORMATION RESILIENCE COMMAND CENTER 2.0 MODELS
# ------------------------------------------------------------------------------

class TransformationResilienceCommandCenter(Base):
    __tablename__ = "transformation_resilience_command_centers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="healthy", index=True)
    last_evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceExecutiveState(Base):
    __tablename__ = "transformation_resilience_executive_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    command_center_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dimension: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(50), nullable=False, default="stable")
    trend: Mapped[str] = mapped_column(String(50), nullable=False, default="improving")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    freshness: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    evidence_count: Mapped[int] = mapped_column(Integer, nullable=False, default=12)

class TransformationResiliencePriorityItem(Base):
    __tablename__ = "transformation_resilience_priority_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    command_center_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    item_type: Mapped[str] = mapped_column(String(100), nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    impact_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    urgency_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="portfolio")
    reversibility: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    decision_deadline: Mapped[str] = mapped_column(String(100), nullable=False, default="2026-Q3")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

class TransformationResilienceSituation(Base):
    __tablename__ = "transformation_resilience_situations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    command_center_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    summary: Mapped[Text] = mapped_column(Text, nullable=False)
    changes_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_scope_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    uncertainty_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    recommended_review: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceSituationSnapshot(Base):
    __tablename__ = "transformation_resilience_situation_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    command_center_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    state_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    source_versions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    freshness: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)

class TransformationResilienceExposureMap(Base):
    __tablename__ = "transformation_resilience_exposure_maps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    command_center_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    transformation_id: Mapped[str] = mapped_column(String(255), nullable=False)
    dimension: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    freshness: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)

class TransformationResilienceEvidenceSummary(Base):
    __tablename__ = "transformation_resilience_evidence_summaries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    command_center_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_diversity_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    freshness_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.98)
    quality_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    has_conflicts: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    conflicts_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95, index=True)

class TransformationResilienceUnappliedLesson(Base):
    __tablename__ = "transformation_resilience_unapplied_lessons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    command_center_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    lesson_title: Mapped[str] = mapped_column(String(255), nullable=False)
    affected_scope_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    reason_not_applied: Mapped[Text] = mapped_column(Text, nullable=False)
    recommended_review: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="unapplied", index=True)

# ------------------------------------------------------------------------------
# SPRINT 91 — ENTERPRISE TRANSFORMATION RESILIENCE DECISION LIFECYCLE 2.0 MODELS
# ------------------------------------------------------------------------------

class TransformationResilienceDecisionDomain(Base):
    __tablename__ = "transformation_resilience_decision_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceDecisionQuestion(Base):
    __tablename__ = "transformation_resilience_decision_questions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    question: Mapped[Text] = mapped_column(Text, nullable=False)
    context_description: Mapped[Text] = mapped_column(Text, nullable=False)
    trigger: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="portfolio")
    deadline: Mapped[str] = mapped_column(String(100), nullable=False, default="2026-Q3")
    decision_owner: Mapped[str] = mapped_column(String(255), nullable=False)
    required_approvers_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class TransformationResilienceDecisionContext(Base):
    __tablename__ = "transformation_resilience_decision_contexts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    portfolio_state_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    resilience_state_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    capacity_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    recovery_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    risk_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    assumptions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    scenario_versions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceDecisionEvidencePack(Base):
    __tablename__ = "transformation_resilience_decision_evidence_packs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evidence_items_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    freshness: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.94, index=True)
    conflicts_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class TransformationResilienceDecisionAssumption(Base):
    __tablename__ = "transformation_resilience_decision_assumptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    assumption: Mapped[Text] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    sensitivity: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="valid", index=True)

class TransformationResilienceDecisionOption(Base):
    __tablename__ = "transformation_resilience_decision_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    option_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    benefits_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    risks_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    capacity_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    reversibility: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    optionality_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)

class TransformationResilienceDecisionScenarioSet(Base):
    __tablename__ = "transformation_resilience_decision_scenario_sets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evaluated_scenarios_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    scenario_comparisons_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceDecisionTradeoff(Base):
    __tablename__ = "transformation_resilience_decision_tradeoffs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    tradeoff_matrix_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceDecisionRecommendation(Base):
    __tablename__ = "transformation_resilience_decision_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    recommended_option_id: Mapped[str] = mapped_column(String(255), nullable=False)
    supporting_evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95, index=True)
    alternatives_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    limitations: Mapped[Text] = mapped_column(Text, nullable=False)
    required_approval: Mapped[str] = mapped_column(String(255), nullable=False)
    label: Mapped[str] = mapped_column(String(100), nullable=False, default="RECOMMENDATION - NOT DECISION")

class TransformationResilienceDecision(Base):
    __tablename__ = "transformation_resilience_decisions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    decision_title: Mapped[str] = mapped_column(String(255), nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending_decision", index=True)
    selected_option_id: Mapped[str] = mapped_column(String(255), nullable=True)
    rationale_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    approval_state: Mapped[str] = mapped_column(String(50), nullable=False, default="submitted")
    deadline: Mapped[str] = mapped_column(String(100), nullable=False, default="2026-Q3", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceDecisionConsequence(Base):
    __tablename__ = "transformation_resilience_decision_consequences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expected_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    affected_transformations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    delay_consequence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class TransformationResilienceDecisionExecutionPlan(Base):
    __tablename__ = "transformation_resilience_decision_execution_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    actions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    milestones_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    rollback_strategy: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceDecisionVerification(Base):
    __tablename__ = "transformation_resilience_decision_verifications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expected_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    observed_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    variance_pct: Mapped[float] = mapped_column(Float, nullable=False, default=2.1)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)

class TransformationResilienceDecisionEffectiveness(Base):
    __tablename__ = "transformation_resilience_decision_effectivenesses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    objective_achievement: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    resilience_improvement: Mapped[float] = mapped_column(Float, nullable=False, default=0.05)
    risk_reduction_pct: Mapped[float] = mapped_column(Float, nullable=False, default=65.0)

class TransformationResilienceDecisionFailure(Base):
    __tablename__ = "transformation_resilience_decision_failures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    failure_classification: Mapped[str] = mapped_column(String(100), nullable=False, default="bad_assumption")
    details: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceDecisionReview(Base):
    __tablename__ = "transformation_resilience_decision_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger_reason: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="review_requested", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceDecisionPrecedent(Base):
    __tablename__ = "transformation_resilience_decision_precedents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prior_decision_id: Mapped[str] = mapped_column(String(255), nullable=False)
    context_description: Mapped[Text] = mapped_column(Text, nullable=False)
    outcome: Mapped[str] = mapped_column(String(100), nullable=False)
    applicability: Mapped[float] = mapped_column(Float, nullable=False, default=0.92, index=True)
    limitations: Mapped[Text] = mapped_column(Text, nullable=False)

# ------------------------------------------------------------------------------
# SPRINT 92 — ENTERPRISE TRANSFORMATION RESILIENCE DECISION LEARNING 2.0 MODELS
# ------------------------------------------------------------------------------

class TransformationResilienceDecisionLearningDomain(Base):
    __tablename__ = "transformation_resilience_decision_learning_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceDecisionExpectedOutcome(Base):
    __tablename__ = "transformation_resilience_decision_expected_outcomes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    objective: Mapped[Text] = mapped_column(Text, nullable=False)
    metric: Mapped[str] = mapped_column(String(255), nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    expected_time: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    source: Mapped[str] = mapped_column(String(255), nullable=False)

class TransformationResilienceDecisionObservedOutcome(Base):
    __tablename__ = "transformation_resilience_decision_observed_outcomes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    metric: Mapped[str] = mapped_column(String(255), nullable=False)
    observed_value: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    freshness: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)

class TransformationResilienceDecisionOutcomeComparison(Base):
    __tablename__ = "transformation_resilience_decision_outcome_comparisons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expected_value: Mapped[float] = mapped_column(Float, nullable=False)
    observed_value: Mapped[float] = mapped_column(Float, nullable=False)
    variance_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    variance_type: Mapped[str] = mapped_column(String(50), nullable=False, default="as_expected")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    materiality: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)

class TransformationResilienceDecisionAttribution(Base):
    __tablename__ = "transformation_resilience_decision_attributions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    attribution_level: Mapped[str] = mapped_column(String(50), nullable=False, default="likely_related")
    rationale: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.88, index=True)

class TransformationResilienceDecisionExternalFactor(Base):
    __tablename__ = "transformation_resilience_decision_external_factors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    factor_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    impact_level: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")

class TransformationResilienceDecisionFailureAnalysis(Base):
    __tablename__ = "transformation_resilience_decision_failure_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    failure_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    root_cause_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    lessons_learned_ref: Mapped[str] = mapped_column(String(255), nullable=True)

class TransformationResilienceDecisionSuccessPattern(Base):
    __tablename__ = "transformation_resilience_decision_success_patterns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    pattern_title: Mapped[str] = mapped_column(String(255), nullable=False)
    conditions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    supporting_cases_count: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.94, index=True)
    limitations: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceDecisionFailurePattern(Base):
    __tablename__ = "transformation_resilience_decision_failure_patterns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    pattern_title: Mapped[str] = mapped_column(String(255), nullable=False)
    frequency: Mapped[int] = mapped_column(Integer, nullable=False, default=3, index=True)
    scope_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)

class TransformationResilienceDecisionPattern(Base):
    __tablename__ = "transformation_resilience_decision_patterns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    context_type: Mapped[str] = mapped_column(String(100), nullable=False)
    typical_outcome: Mapped[str] = mapped_column(String(100), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.91, index=True)

class TransformationResilienceDecisionLesson(Base):
    __tablename__ = "transformation_resilience_decision_lessons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    lesson_type: Mapped[str] = mapped_column(String(100), nullable=False)
    lesson: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    confidence: Mapped[str] = mapped_column(String(50), nullable=False, default="validated", index=True)
    scope_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class TransformationResilienceDecisionLessonApplication(Base):
    __tablename__ = "transformation_resilience_decision_lesson_applications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    affected_transformation_id: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="applied", index=True)
    notes: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceDecisionLessonConflict(Base):
    __tablename__ = "transformation_resilience_decision_lesson_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_a_id: Mapped[str] = mapped_column(String(255), nullable=False)
    lesson_b_id: Mapped[str] = mapped_column(String(255), nullable=False)
    conflict_description: Mapped[Text] = mapped_column(Text, nullable=False)
    context_differences_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDecisionQualityAssessment(Base):
    __tablename__ = "transformation_resilience_decision_quality_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evidence_completeness: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    assumption_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    scenario_coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    option_diversity: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    tradeoff_completeness: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    decision_timeliness: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    execution_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    verification_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDecisionCalibration(Base):
    __tablename__ = "transformation_resilience_decision_calibrations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    prediction_value: Mapped[float] = mapped_column(Float, nullable=False)
    actual_value: Mapped[float] = mapped_column(Float, nullable=False)
    error_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    bias_direction: Mapped[str] = mapped_column(String(50), nullable=False, default="neutral")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDecisionModelPerformance(Base):
    __tablename__ = "transformation_resilience_decision_model_performances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_version: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    outcome_accuracy_pct: Mapped[float] = mapped_column(Float, nullable=False, default=94.5)
    evaluated_cases_count: Mapped[int] = mapped_column(Integer, nullable=False, default=42)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceDecisionDelayAnalysis(Base):
    __tablename__ = "transformation_resilience_decision_delay_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    deadline: Mapped[str] = mapped_column(String(100), nullable=False)
    actual_decision_time: Mapped[str] = mapped_column(String(100), nullable=False)
    delay_days: Mapped[float] = mapped_column(Float, nullable=False, default=0.0, index=True)
    consequence_summary: Mapped[Text] = mapped_column(Text, nullable=False)

# ------------------------------------------------------------------------------
# SPRINT 93 — ENTERPRISE TRANSFORMATION RESILIENCE DECISION KNOWLEDGE 2.0 MODELS
# ------------------------------------------------------------------------------

class TransformationResilienceDecisionKnowledgeDomain(Base):
    __tablename__ = "transformation_resilience_decision_knowledge_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceDecisionKnowledgeObject(Base):
    __tablename__ = "transformation_resilience_decision_knowledge_objects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    statement: Mapped[Text] = mapped_column(Text, nullable=False)
    context_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95, index=True)
    applicability_level: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    limitations: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="validated", index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    source_decision_id: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceDecisionKnowledgeValidation(Base):
    __tablename__ = "transformation_resilience_decision_knowledge_validations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    supporting_cases_count: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    contradicting_cases_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    evidence_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    reproducibility: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    context_consistency: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDecisionKnowledgeContext(Base):
    __tablename__ = "transformation_resilience_decision_knowledge_contexts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    transformation_type: Mapped[str] = mapped_column(String(100), nullable=False)
    dependency_profile: Mapped[str] = mapped_column(String(255), nullable=False)
    capacity_profile: Mapped[str] = mapped_column(String(255), nullable=False)
    risk_profile: Mapped[str] = mapped_column(String(255), nullable=False)
    recovery_profile: Mapped[str] = mapped_column(String(255), nullable=False)
    governance_context: Mapped[str] = mapped_column(String(255), nullable=False)
    time_horizon: Mapped[str] = mapped_column(String(100), nullable=False)

class TransformationResilienceDecisionKnowledgeApplicability(Base):
    __tablename__ = "transformation_resilience_decision_knowledge_applicabilities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_decision_context_id: Mapped[str] = mapped_column(String(255), nullable=False)
    level: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    applicability_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    explanation: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceDecisionKnowledgeConflict(Base):
    __tablename__ = "transformation_resilience_decision_knowledge_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_a_id: Mapped[str] = mapped_column(String(255), nullable=False)
    knowledge_object_b_id: Mapped[str] = mapped_column(String(255), nullable=False)
    conflicting_claims: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    context_differences: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDecisionKnowledgeInvalidation(Base):
    __tablename__ = "transformation_resilience_decision_knowledge_invalidations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger: Mapped[str] = mapped_column(String(100), nullable=False)
    rationale: Mapped[Text] = mapped_column(Text, nullable=False)
    contradictory_evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDecisionKnowledgeReview(Base):
    __tablename__ = "transformation_resilience_decision_knowledge_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger_reason: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending_review", index=True)
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    review_after: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc) + timedelta(days=90))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc) + timedelta(days=180))

class TransformationResilienceDecisionKnowledgeReuse(Base):
    __tablename__ = "transformation_resilience_decision_knowledge_reuses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    context_description: Mapped[Text] = mapped_column(Text, nullable=False)
    recommendation_influence: Mapped[str] = mapped_column(String(100), nullable=False, default="high")
    result: Mapped[str] = mapped_column(String(50), nullable=False, default="successful", index=True)
    outcome_summary: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceDecisionKnowledgePack(Base):
    __tablename__ = "transformation_resilience_decision_knowledge_packs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    pack_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")
    lessons_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    precedents_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    patterns_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    assumptions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    conflicts_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    limitations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDecisionKnowledgeQuality(Base):
    __tablename__ = "transformation_resilience_decision_knowledge_qualities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    completeness: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    provenance: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    freshness: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    consistency: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    validation_level: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)

class TransformationResilienceDecisionKnowledgeGap(Base):
    __tablename__ = "transformation_resilience_decision_knowledge_gaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    gap_title: Mapped[str] = mapped_column(String(255), nullable=False)
    gap_type: Mapped[str] = mapped_column(String(100), nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    recommended_activity: Mapped[Text] = mapped_column(Text, nullable=False)

# ------------------------------------------------------------------------------
# SPRINT 94 — ENTERPRISE TRANSFORMATION RESILIENCE KNOWLEDGE GOVERNANCE 2.0 MODELS
# ------------------------------------------------------------------------------

class TransformationResilienceKnowledgeAssuranceDomain(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeHealth(Base):
    __tablename__ = "transformation_resilience_knowledge_healths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    freshness_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    provenance_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.98)
    validation_strength: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    applicability_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    reuse_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    consistency_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    context_stability: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    evidence_coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    overall_status: Mapped[str] = mapped_column(String(50), nullable=False, default="trusted", index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeEvidenceAssurance(Base):
    __tablename__ = "transformation_resilience_knowledge_evidence_assurances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    freshness: Mapped[float] = mapped_column(Float, nullable=False, default=0.96, index=True)
    quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    reliability: Mapped[float] = mapped_column(Float, nullable=False, default=0.98)
    independence_type: Mapped[str] = mapped_column(String(50), nullable=False, default="independent")
    coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    conflicts_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

class TransformationResilienceKnowledgeClaim(Base):
    __tablename__ = "transformation_resilience_knowledge_claims"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    statement: Mapped[Text] = mapped_column(Text, nullable=False)
    claim_type: Mapped[str] = mapped_column(String(100), nullable=False, default="validated")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeClaimSupport(Base):
    __tablename__ = "transformation_resilience_knowledge_claim_supports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evidence_id: Mapped[str] = mapped_column(String(255), nullable=False)
    support_strength: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    source_independence: Mapped[str] = mapped_column(String(50), nullable=False, default="independent")

class TransformationResilienceKnowledgeClaimConflict(Base):
    __tablename__ = "transformation_resilience_knowledge_claim_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_a_id: Mapped[str] = mapped_column(String(255), nullable=False)
    claim_b_id: Mapped[str] = mapped_column(String(255), nullable=False)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    context_description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeContextDrift(Base):
    __tablename__ = "transformation_resilience_knowledge_context_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dimension: Mapped[str] = mapped_column(String(100), nullable=False)
    drift_description: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="changing", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeReuseAssurance(Base):
    __tablename__ = "transformation_resilience_knowledge_reuse_assurances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    reuse_count: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    successful_reuse_count: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    failed_reuse_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    inconclusive_reuse_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    context_similarity_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)

class TransformationResilienceKnowledgeInfluence(Base):
    __tablename__ = "transformation_resilience_knowledge_influences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_type: Mapped[str] = mapped_column(String(100), nullable=False)
    target_id: Mapped[str] = mapped_column(String(255), nullable=False)
    influence_level: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeRisk(Base):
    __tablename__ = "transformation_resilience_knowledge_risks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_type: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    affected_decisions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)

class TransformationResilienceKnowledgeAssuranceReview(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger: Mapped[str] = mapped_column(String(100), nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    recommended_action: Mapped[str] = mapped_column(String(100), nullable=False, default="revalidate")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeAssuranceReviewPacket(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_review_packets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False)
    claims_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    conflicts_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    context_drift_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    reuse_history_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    influence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    risk_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    recommended_action: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeRevalidation(Base):
    __tablename__ = "transformation_resilience_knowledge_revalidations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    review_question: Mapped[Text] = mapped_column(Text, nullable=False)
    new_evidence_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    new_context: Mapped[Text] = mapped_column(Text, nullable=False)
    result: Mapped[str] = mapped_column(String(50), nullable=False, default="confirmed", index=True)
    reviewer: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeLineage(Base):
    __tablename__ = "transformation_resilience_knowledge_lineages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_decision_id: Mapped[str] = mapped_column(String(255), nullable=False)
    outcome_id: Mapped[str] = mapped_column(String(255), nullable=False)
    lesson_id: Mapped[str] = mapped_column(String(255), nullable=False)
    pattern_id: Mapped[str] = mapped_column(String(255), nullable=False)
    claim_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    evidence_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    reuse_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    review_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class TransformationResilienceKnowledgeEvidenceGap(Base):
    __tablename__ = "transformation_resilience_knowledge_evidence_gaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    gap_title: Mapped[str] = mapped_column(String(255), nullable=False)
    gap_type: Mapped[str] = mapped_column(String(100), nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    recommended_activity: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceKnowledgeGovernanceState(Base):
    __tablename__ = "transformation_resilience_knowledge_governance_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(50), nullable=False, default="trusted", index=True)
    authorized_by: Mapped[str] = mapped_column(String(255), nullable=False)
    rationale: Mapped[Text] = mapped_column(Text, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

# ------------------------------------------------------------------------------
# SPRINT 95 — ENTERPRISE TRANSFORMATION RESILIENCE KNOWLEDGE OPERATIONS 2.0 MODELS
# ------------------------------------------------------------------------------

class TransformationResilienceKnowledgeOperationsDomain(Base):
    __tablename__ = "transformation_resilience_knowledge_operations_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeRiskCase(Base):
    __tablename__ = "transformation_resilience_knowledge_risk_cases"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_type: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    impact: Mapped[str] = mapped_column(String(100), nullable=False, default="high_decision_impact")
    urgency: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    owner: Mapped[str] = mapped_column(String(255), nullable=False, default="unassigned", index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="detected", index=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

class TransformationResilienceKnowledgeRiskQueue(Base):
    __tablename__ = "transformation_resilience_knowledge_risk_queues"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    impact: Mapped[str] = mapped_column(String(100), nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    deadline: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="queued")

class TransformationResilienceKnowledgeRiskAssignment(Base):
    __tablename__ = "transformation_resilience_knowledge_risk_assignments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    owner: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    assigned_by: Mapped[str] = mapped_column(String(255), nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    reason: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceKnowledgeRemediationPlan(Base):
    __tablename__ = "transformation_resilience_knowledge_remediation_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    objective: Mapped[Text] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    actions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    success_criteria: Mapped[Text] = mapped_column(Text, nullable=False)
    rollback_strategy: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="planned", index=True)

class TransformationResilienceKnowledgeRemediationAction(Base):
    __tablename__ = "transformation_resilience_knowledge_remediation_actions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String(100), nullable=False, default="collect_evidence")
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="planned", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeEvidenceTask(Base):
    __tablename__ = "transformation_resilience_knowledge_evidence_tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gap_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    requested_evidence: Mapped[Text] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="assigned", index=True)
    quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)

class TransformationResilienceKnowledgeReviewTask(Base):
    __tablename__ = "transformation_resilience_knowledge_review_tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    review_question: Mapped[Text] = mapped_column(Text, nullable=False)
    reviewer: Mapped[str] = mapped_column(String(255), nullable=False)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="assigned", index=True)
    result: Mapped[str] = mapped_column(String(50), nullable=False, default="inconclusive")

class TransformationResilienceKnowledgeRemediationVerification(Base):
    __tablename__ = "transformation_resilience_knowledge_remediation_verifications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_before: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    risk_after: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    knowledge_health_before: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    knowledge_health_after: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    evidence_quality_before: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    evidence_quality_after: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeRemediationEffectiveness(Base):
    __tablename__ = "transformation_resilience_knowledge_remediation_effectivenesses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_reduction: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    evidence_improvement: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    confidence_improvement: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    applicability_improvement: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    reuse_improvement: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeRiskEscalation(Base):
    __tablename__ = "transformation_resilience_knowledge_risk_escalations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="critical")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="escalated", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeRemediationFailure(Base):
    __tablename__ = "transformation_resilience_knowledge_remediation_failures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    failure_category: Mapped[str] = mapped_column(String(100), nullable=False, default="evidence_unavailable")
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeRecurringRiskPattern(Base):
    __tablename__ = "transformation_resilience_knowledge_recurring_risk_patterns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pattern_title: Mapped[str] = mapped_column(String(255), nullable=False)
    frequency: Mapped[int] = mapped_column(Integer, nullable=False, default=3, index=True)
    affected_knowledge_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_decisions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)

class TransformationResilienceKnowledgeRemediationQuality(Base):
    __tablename__ = "transformation_resilience_knowledge_remediation_qualities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    completeness: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    evidence_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    verification_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    timeliness: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    repeatability: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeOperatingPattern(Base):
    __tablename__ = "transformation_resilience_knowledge_operating_patterns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

# ------------------------------------------------------------------------------
# SPRINT 96 — ENTERPRISE TRANSFORMATION RESILIENCE KNOWLEDGE ASSURANCE PLANNING 2.0 MODELS
# ------------------------------------------------------------------------------

class TransformationResilienceKnowledgeAssurancePlanningDomain(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_planning_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeAssurancePortfolio(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_portfolios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_transformations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    decision_domains_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    exposure_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    current_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=0.75)
    planned_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeSystemicRisk(Base):
    __tablename__ = "transformation_resilience_knowledge_systemic_risks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    breadth: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    dependency_centrality: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    decision_influence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    recurrence: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    uncertainty: Mapped[float] = mapped_column(Float, nullable=False, default=0.25)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="critical", index=True)

class TransformationResilienceKnowledgeRootCauseGroup(Base):
    __tablename__ = "transformation_resilience_knowledge_root_cause_groups"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    root_cause_type: Mapped[str] = mapped_column(String(100), nullable=False, default="stale_source")
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    frequency: Mapped[int] = mapped_column(Integer, nullable=False, default=4, index=True)
    affected_risk_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class TransformationResilienceKnowledgeRemediationLever(Base):
    __tablename__ = "transformation_resilience_knowledge_remediation_levers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lever_type: Mapped[str] = mapped_column(String(100), nullable=False, default="shared_evidence_source")
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    risk_coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.94, index=True)
    limitations: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceKnowledgeAssuranceCapacity(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_capacities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    available_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=0.80)
    required_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    specialist_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=0.75)
    simulation_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    review_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=0.70)
    evidence_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceCapacityConstraint(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_capacity_constraints"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    constraint_type: Mapped[str] = mapped_column(String(100), nullable=False, default="limited_experts")
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)

class TransformationResilienceKnowledgeAssuranceDemand(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_demands"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_workload: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    evidence_workload: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    review_workload: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    simulation_workload: Mapped[float] = mapped_column(Float, nullable=False, default=0.80)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceOption(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    option_type: Mapped[str] = mapped_column(String(100), nullable=False, default="parallel")
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    effort: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    time_est: Mapped[str] = mapped_column(String(50), nullable=False, default="14 days")
    risk_reduction: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceSequence(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_sequences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sequence_order_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    dependencies_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    rationale: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceScenario(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_type: Mapped[str] = mapped_column(String(100), nullable=False, default="full_capacity")
    coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    residual_risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.05)
    capacity_required: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssurancePlan(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    objective: Mapped[Text] = mapped_column(Text, nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    selected_options_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    sequence_id: Mapped[str] = mapped_column(String(255), nullable=False)
    capacity_allocation_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    risk_coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    residual_risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.08)
    assumptions: Mapped[Text] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", index=True)

class TransformationResilienceKnowledgeAssuranceResidualRisk(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_residual_risks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    unaddressed_risk: Mapped[Text] = mapped_column(Text, nullable=False)
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    review_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

class TransformationResilienceKnowledgeAssuranceTradeoff(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_tradeoffs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    tradeoff_description: Mapped[Text] = mapped_column(Text, nullable=False)
    coverage_vs_effort: Mapped[str] = mapped_column(String(100), nullable=False)
    speed_vs_uncertainty: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceRecommendation(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    label: Mapped[str] = mapped_column(String(100), nullable=False, default="ANALYTICAL RECOMMENDATION — NOT APPROVAL")
    recommendation_text: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)

class TransformationResilienceKnowledgeAssurancePlanVerification(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_plan_verifications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    planned_coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    actual_coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    planned_risk_reduction: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    actual_risk_reduction: Mapped[float] = mapped_column(Float, nullable=False, default=0.82)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssurancePlanEffectiveness(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_plan_effectivenesses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_reduction: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    coverage_improvement: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    assurance_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    timeliness: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    capacity_efficiency: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssurancePlanFailure(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_plan_failures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    failure_type: Mapped[str] = mapped_column(String(100), nullable=False, default="capacity_failure", index=True)
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

# ------------------------------------------------------------------------------
# SPRINT 97 — ENTERPRISE TRANSFORMATION RESILIENCE ADAPTIVE KNOWLEDGE ASSURANCE 2.0 MODELS
# ------------------------------------------------------------------------------

class TransformationResilienceAdaptiveKnowledgeAssuranceDomain(Base):
    __tablename__ = "transformation_resilience_adaptive_knowledge_assurance_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeAssurancePlanBaseline(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_plan_baselines"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    plan_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")
    assumptions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    risks_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    capacity_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    sequence_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    options_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    residual_risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.08)
    approval_state: Mapped[str] = mapped_column(String(50), nullable=False, default="approved")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceChangeSignal(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_change_signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="resilience_sensing")
    change_type: Mapped[str] = mapped_column(String(100), nullable=False, default="dependency_change")
    significance: Mapped[str] = mapped_column(String(50), nullable=False, default="material", index=True)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceChangeDetection(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_change_detections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    affected_assumptions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_risks_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_actions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeAssuranceAssumptionImpact(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_assumption_impacts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    assumption: Mapped[Text] = mapped_column(Text, nullable=False)
    previous_state: Mapped[str] = mapped_column(String(255), nullable=False)
    current_state: Mapped[str] = mapped_column(String(255), nullable=False)
    impact: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssurancePlanImpact(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_plan_impacts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_impact: Mapped[Text] = mapped_column(Text, nullable=False)
    sequence_impact: Mapped[Text] = mapped_column(Text, nullable=False)
    capacity_impact: Mapped[Text] = mapped_column(Text, nullable=False)
    coverage_impact: Mapped[Text] = mapped_column(Text, nullable=False)
    residual_risk_impact: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="material", index=True)

class TransformationResilienceKnowledgeAssurancePlanHealth(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_plan_healths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_alignment: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    evidence_alignment: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    capacity_alignment: Mapped[float] = mapped_column(Float, nullable=False, default=0.75)
    sequence_alignment: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    deadline_alignment: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    assumption_alignment: Mapped[float] = mapped_column(Float, nullable=False, default=0.80)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssurancePlanStaleness(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_plan_stalenesses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="materially_stale", index=True)
    outdated_assumptions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    outdated_evidence_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    changed_dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class TransformationResilienceKnowledgeAssuranceReplanTrigger(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_replan_triggers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger_type: Mapped[str] = mapped_column(String(100), nullable=False, default="material_plan_impact")
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True)
    triggered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeAssuranceReplanRecommendation(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_replan_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    label: Mapped[str] = mapped_column(String(100), nullable=False, default="ANALYTICAL RECOMMENDATION — NOT APPROVAL")
    recommended_option: Mapped[str] = mapped_column(String(100), nullable=False, default="resequence")
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    tradeoffs: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)

class TransformationResilienceKnowledgeAssurancePlanVersion(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_plan_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version_number: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0", index=True)
    parent_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")
    change_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    approval_state: Mapped[str] = mapped_column(String(50), nullable=False, default="approved")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeAssurancePlanDiff(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_plan_diffs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    from_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")
    to_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    added_risks_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    removed_risks_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    reordered_actions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    changed_assumptions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceReplanQueue(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_replan_queues"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger_type: Mapped[str] = mapped_column(String(100), nullable=False, default="material_plan_impact")
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="material")
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=1, index=True)
    recommended_action: Mapped[str] = mapped_column(String(100), nullable=False, default="resequence")
    approval_requirement: Mapped[str] = mapped_column(String(50), nullable=False, default="approval_required")

class TransformationResilienceKnowledgeAssuranceEmergencyReplan(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_emergency_replans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger_reason: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    war_room_session_id: Mapped[str] = mapped_column(String(255), nullable=False, default="war_room_01")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeAssuranceCrossPlanImpact(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_cross_plan_impacts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    affected_plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    impact_description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="material", index=True)
    recommended_action: Mapped[str] = mapped_column(String(100), nullable=False, default="resequence_affected_plan")

class TransformationResilienceKnowledgeAssurancePortfolioDrift(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_portfolio_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_drift: Mapped[float] = mapped_column(Float, nullable=False, default=0.12)
    capacity_drift: Mapped[float] = mapped_column(Float, nullable=False, default=0.15)
    evidence_drift: Mapped[float] = mapped_column(Float, nullable=False, default=0.08)
    dependency_drift: Mapped[float] = mapped_column(Float, nullable=False, default=0.10)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

# ------------------------------------------------------------------------------
# SPRINT 98 — ENTERPRISE TRANSFORMATION RESILIENCE ASSURANCE COORDINATION 2.0 MODELS
# ------------------------------------------------------------------------------

class TransformationResilienceKnowledgeAssuranceCoordinationDomain(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_coordination_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeAssuranceActivePlanSet(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_active_plan_sets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    active_plan_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    active_versions_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    owners_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    deadlines_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssurancePlanRelationship(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_plan_relationships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    relationship_type: Mapped[str] = mapped_column(String(100), nullable=False, default="depends_on", index=True)
    description: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceKnowledgeAssuranceResource(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_resources"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False, default="simulation_capacity", index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    total_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    unit: Mapped[str] = mapped_column(String(50), nullable=False, default="units")

class TransformationResilienceKnowledgeAssuranceResourceDemand(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_resource_demands"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    resource_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    required_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    time_window: Mapped[str] = mapped_column(String(100), nullable=False, default="Q3", index=True)
    criticality: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)

class TransformationResilienceKnowledgeAssuranceResourceAvailability(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_resource_availabilities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    available_capacity: Mapped[float] = mapped_column(Float, nullable=False, default=0.8)
    time_window: Mapped[str] = mapped_column(String(100), nullable=False, default="Q3", index=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="resilience_portfolio")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)

class TransformationResilienceKnowledgeAssuranceResourceContention(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_resource_contentions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    competing_plan_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    demand_deficit: Mapped[float] = mapped_column(Float, nullable=False, default=0.25)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceEvidenceContention(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_evidence_contentions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evidence_source_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    competing_plan_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="material", index=True)

class TransformationResilienceKnowledgeAssuranceReviewContention(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_review_contentions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_domain: Mapped[str] = mapped_column(String(100), nullable=False, default="cloud_security", index=True)
    competing_plan_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    review_capacity_deficit: Mapped[float] = mapped_column(Float, nullable=False, default=0.30)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)

class TransformationResilienceKnowledgeAssuranceSimulationContention(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_simulation_contentions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    simulation_cluster: Mapped[str] = mapped_column(String(100), nullable=False, default="governance_twin_cluster_01", index=True)
    competing_plan_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    compute_deficit_pct: Mapped[float] = mapped_column(Float, nullable=False, default=20.0)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="material", index=True)

class TransformationResilienceKnowledgeAssuranceDeadlineCollision(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_deadline_collisions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    colliding_plan_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    shared_deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    impact_description: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceCoordinationOption(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_coordination_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    option_type: Mapped[str] = mapped_column(String(100), nullable=False, default="sequence", index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    risk_reduction: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    effort: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    time_est: Mapped[str] = mapped_column(String(50), nullable=False, default="14 days")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceCoordinationRecommendation(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_coordination_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    coordination_plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    label: Mapped[str] = mapped_column(String(100), nullable=False, default="ANALYTICAL RECOMMENDATION — NOT APPROVAL")
    recommended_option: Mapped[str] = mapped_column(String(100), nullable=False, default="sequence")
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    tradeoffs: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)

class TransformationResilienceKnowledgeAssuranceCoordinationPlan(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_coordination_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    objective: Mapped[Text] = mapped_column(Text, nullable=False)
    coordinating_plan_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    relationships_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    resource_assumptions: Mapped[Text] = mapped_column(Text, nullable=False)
    sequence_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    residual_conflicts: Mapped[Text] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", index=True)

class TransformationResilienceKnowledgeAssuranceCoordinationAction(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_coordination_actions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    coordination_plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String(100), nullable=False, default="sequence_plans")
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="planned", index=True)

class TransformationResilienceKnowledgeAssuranceCoordinationConflict(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_coordination_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conflict_type: Mapped[str] = mapped_column(String(100), nullable=False, default="resource", index=True)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    selected_resolution: Mapped[str] = mapped_column(String(255), nullable=False, default="resequence")

class TransformationResilienceKnowledgeAssuranceCoordinationCascade(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_coordination_cascades"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    affected_plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    depth: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="material", index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)

class TransformationResilienceKnowledgeAssuranceCoordinationDrift(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_coordination_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trigger_reason: Mapped[Text] = mapped_column(Text, nullable=False)
    impact: Mapped[Text] = mapped_column(Text, nullable=False)
    recommended_response: Mapped[str] = mapped_column(String(100), nullable=False, default="recoordinate")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceBottleneck(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_bottlenecks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bottleneck_type: Mapped[str] = mapped_column(String(100), nullable=False, default="simulation_capacity", index=True)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    affected_plan_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="critical", index=True)

class TransformationResilienceKnowledgeAssuranceCoordinationEffectiveness(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_coordination_effectivenesses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    coordination_plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    contention_reduction: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    risk_reduction: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    coverage_improvement: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    timeliness: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    capacity_efficiency: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    coordination_stability: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceCoordinationFailure(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_coordination_failures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    coordination_plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    failure_type: Mapped[str] = mapped_column(String(100), nullable=False, default="resource_unavailable", index=True)
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

# ------------------------------------------------------------------------------
# SPRINT 99 — ENTERPRISE TRANSFORMATION RESILIENCE ASSURANCE CONFLICT INTELLIGENCE 2.0 MODELS
# ------------------------------------------------------------------------------

class TransformationResilienceKnowledgeAssuranceConflictIntelligenceDomain(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_intelligence_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeAssuranceConflictCase(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_cases"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conflict_type: Mapped[str] = mapped_column(String(100), nullable=False, default="resource", index=True)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="detected", index=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="assurance_coordination")
    affected_plan_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_resources_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_dependencies_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_deadlines_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)

class TransformationResilienceKnowledgeAssuranceConflictImpact(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_impacts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conflict_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_exposure: Mapped[float] = mapped_column(Float, nullable=False, default=0.25)
    coverage_loss: Mapped[float] = mapped_column(Float, nullable=False, default=0.15)
    deadline_exposure_days: Mapped[int] = mapped_column(Integer, nullable=False, default=7)
    capacity_exposure_pct: Mapped[float] = mapped_column(Float, nullable=False, default=20.0)
    dependency_exposure: Mapped[str] = mapped_column(String(100), nullable=False, default="material")
    residual_uncertainty: Mapped[float] = mapped_column(Float, nullable=False, default=0.10)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)

class TransformationResilienceKnowledgeAssuranceConflictRootCause(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_root_causes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conflict_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    root_cause_category: Mapped[str] = mapped_column(String(100), nullable=False, default="shared_resource")
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    frequency: Mapped[int] = mapped_column(Integer, nullable=False, default=1, index=True)

class TransformationResilienceKnowledgeAssuranceConflictResolutionOption(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_resolution_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conflict_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    option_type: Mapped[str] = mapped_column(String(100), nullable=False, default="sequence", index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.10)
    coverage_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    deadline_shift_days: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    effort: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceConflictTradeoff(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_tradeoffs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conflict_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dimension_a: Mapped[str] = mapped_column(String(100), nullable=False, default="coverage")
    dimension_b: Mapped[str] = mapped_column(String(100), nullable=False, default="speed")
    tradeoff_description: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceConflictScenarioResult(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_scenario_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conflict_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    scenario_type: Mapped[str] = mapped_column(String(100), nullable=False, default="baseline")
    risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.25)
    coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.84)
    residual_risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.16)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceConflictRecommendation(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conflict_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    label: Mapped[str] = mapped_column(String(100), nullable=False, default="ANALYTICAL RECOMMENDATION — NOT DECISION")
    recommended_option: Mapped[str] = mapped_column(String(100), nullable=False, default="sequence")
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    tradeoffs: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    unresolved_concerns: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceConflictDecisionPacket(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_decision_packets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conflict_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    summary: Mapped[Text] = mapped_column(Text, nullable=False)
    affected_plans_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    root_cause_description: Mapped[Text] = mapped_column(Text, nullable=False)
    options_summary_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    recommendation: Mapped[Text] = mapped_column(Text, nullable=False)
    residual_risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.08)
    required_authority: Mapped[str] = mapped_column(String(100), nullable=False, default="governance_authority")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceConflictResolutionPlan(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_resolution_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conflict_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    selected_option: Mapped[str] = mapped_column(String(100), nullable=False, default="sequence")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="planned", index=True)
    rollback_plan: Mapped[Text] = mapped_column(Text, nullable=False)
    residual_conflicts: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceKnowledgeAssuranceConflictResolutionAction(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_resolution_actions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resolution_plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String(100), nullable=False, default="resequence")
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="planned", index=True)

class TransformationResilienceKnowledgeAssuranceResidualConflict(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_residual_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conflict_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    remaining_conflict: Mapped[Text] = mapped_column(Text, nullable=False)
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    review_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    impact: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceKnowledgeAssuranceConflictCascade(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_cascades"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_conflict_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    affected_conflict_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    depth: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="material", index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)

class TransformationResilienceKnowledgeAssuranceConflictCluster(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_clusters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cluster_type: Mapped[str] = mapped_column(String(100), nullable=False, default="shared_dependency")
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    conflict_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceSystemicConflict(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_systemic_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pattern_description: Mapped[Text] = mapped_column(Text, nullable=False)
    affected_transformations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="critical", index=True)

class TransformationResilienceKnowledgeAssuranceConflictDrift(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trigger_reason: Mapped[Text] = mapped_column(Text, nullable=False)
    severity_change: Mapped[str] = mapped_column(String(50), nullable=False, default="increased")
    recommended_response: Mapped[str] = mapped_column(String(100), nullable=False, default="escalate")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceConflictEscalation(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_escalations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conflict_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger_reason: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="escalated", index=True)
    routed_to: Mapped[str] = mapped_column(String(100), nullable=False, default="Governance Board")

class TransformationResilienceKnowledgeAssuranceConflictResolutionEffectiveness(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_resolution_effectivenesses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conflict_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_reduction: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    coverage_preservation: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    deadline_recovery: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    capacity_relief: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    dependency_stabilization: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    uncertainty_reduction: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceKnowledgeAssuranceConflictResolutionFailure(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_resolution_failures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conflict_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    failure_type: Mapped[str] = mapped_column(String(100), nullable=False, default="resource_failure", index=True)
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceKnowledgeAssuranceConflictResolutionPattern(Base):
    __tablename__ = "transformation_resilience_knowledge_assurance_conflict_resolution_patterns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    pattern_description: Mapped[Text] = mapped_column(Text, nullable=False)
    reusability_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95, index=True)

# ------------------------------------------------------------------------------
# SPRINT 100 — ENTERPRISE TRANSFORMATION RESILIENCE ASSURANCE DECISION INTELLIGENCE 2.0 MODELS
# ------------------------------------------------------------------------------

class TransformationResilienceAssuranceDecisionIntelligenceDomain(Base):
    __tablename__ = "transformation_resilience_assurance_decision_intelligence_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceAssuranceDecisionOutcome(Base):
    __tablename__ = "transformation_resilience_assurance_decision_outcomes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    conflict_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    recommendation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    selected_option: Mapped[str] = mapped_column(String(100), nullable=False, default="sequence")
    execution_status: Mapped[str] = mapped_column(String(50), nullable=False, default="completed")
    verification_status: Mapped[str] = mapped_column(String(50), nullable=False, default="verified")
    outcome_status: Mapped[str] = mapped_column(String(50), nullable=False, default="positive", index=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceExpectedActualComparison(Base):
    __tablename__ = "transformation_resilience_assurance_expected_actual_comparisons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_outcome_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expected_risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.08)
    actual_risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.07)
    expected_coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    actual_coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    expected_effort: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    actual_effort: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    expected_timeline_days: Mapped[int] = mapped_column(Integer, nullable=False, default=14)
    actual_timeline_days: Mapped[int] = mapped_column(Integer, nullable=False, default=13)
    expected_capacity_pct: Mapped[float] = mapped_column(Float, nullable=False, default=80.0)
    actual_capacity_pct: Mapped[float] = mapped_column(Float, nullable=False, default=78.0)
    expected_residual_risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.08)
    actual_residual_risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.06)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceOutcomeVariance(Base):
    __tablename__ = "transformation_resilience_assurance_outcome_variances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    comparison_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dimension: Mapped[str] = mapped_column(String(100), nullable=False, default="coverage", index=True)
    expected_val: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    actual_val: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    delta: Mapped[float] = mapped_column(Float, nullable=False, default=0.02)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    explanation_status: Mapped[str] = mapped_column(String(50), nullable=False, default="explained")

class TransformationResilienceAssuranceOutcomeEvidence(Base):
    __tablename__ = "transformation_resilience_assurance_outcome_evidences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_outcome_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="resilience_sensing")
    evidence_type: Mapped[str] = mapped_column(String(100), nullable=False, default="telemetry_verification")
    quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.95, index=True)
    relationship: Mapped[str] = mapped_column(String(100), nullable=False, default="verified_telemetry")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceAssuranceOutcomeCausalAnalysis(Base):
    __tablename__ = "transformation_resilience_assurance_outcome_causal_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_outcome_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    causal_relationship: Mapped[str] = mapped_column(String(100), nullable=False, default="contributed_to")
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceRecommendationQuality(Base):
    __tablename__ = "transformation_resilience_assurance_recommendation_qualities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recommendation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evidence_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    scenario_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    risk_calibration: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    coverage_accuracy: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    timeline_accuracy: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    capacity_accuracy: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    uncertainty_calibration: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceDecisionQuality(Base):
    __tablename__ = "transformation_resilience_assurance_decision_qualities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    information_sufficiency: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    option_completeness: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    tradeoff_visibility: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    uncertainty_visibility: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    governance_alignment: Mapped[float] = mapped_column(Float, nullable=False, default=0.98)
    outcome_alignment: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceDecisionQualityTrend(Base):
    __tablename__ = "transformation_resilience_assurance_decision_quality_trends"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    average_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    trend_direction: Mapped[str] = mapped_column(String(50), nullable=False, default="improving")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceResolutionPatternPerformance(Base):
    __tablename__ = "transformation_resilience_assurance_resolution_pattern_performances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pattern_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    usage_count: Mapped[int] = mapped_column(Integer, nullable=False, default=12)
    success_count: Mapped[int] = mapped_column(Integer, nullable=False, default=11)
    failure_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    risk_reduction_avg: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    coverage_preservation_avg: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    deadline_recovery_avg: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    capacity_relief_avg: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    uncertainty_reduction_avg: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceContextSimilarity(Base):
    __tablename__ = "transformation_resilience_assurance_context_similarities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_a_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    case_b_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    similarity_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    matching_dimensions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class TransformationResilienceAssuranceHistoricalAnalogue(Base):
    __tablename__ = "transformation_resilience_assurance_historical_analogues"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    current_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    historical_case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    similarities_description: Mapped[Text] = mapped_column(Text, nullable=False)
    differences_description: Mapped[Text] = mapped_column(Text, nullable=False)
    historical_outcome: Mapped[str] = mapped_column(String(50), nullable=False, default="positive")
    relevance_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92, index=True)

class TransformationResilienceAssuranceRecommendationCalibration(Base):
    __tablename__ = "transformation_resilience_assurance_recommendation_calibrations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    predicted_confidence_avg: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    observed_accuracy_avg: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    calibration_error: Mapped[float] = mapped_column(Float, nullable=False, default=0.01)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="well_calibrated")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceLearningSignal(Base):
    __tablename__ = "transformation_resilience_assurance_learning_signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_type: Mapped[str] = mapped_column(String(100), nullable=False, default="recurring_pattern", index=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="resolution_learning")
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceAssuranceLearningPriority(Base):
    __tablename__ = "transformation_resilience_assurance_learning_priorities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learning_signal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    priority_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    decision_impact: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    recurrence_frequency: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high")

class TransformationResilienceAssuranceKnowledgeUpdateProposal(Base):
    __tablename__ = "transformation_resilience_assurance_knowledge_update_proposals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learning_signal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    proposal_type: Mapped[str] = mapped_column(String(100), nullable=False, default="new_validation_requirement")
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending_review", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceAssuranceRecommendationUpdateProposal(Base):
    __tablename__ = "transformation_resilience_assurance_recommendation_update_proposals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learning_signal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    current_behavior: Mapped[Text] = mapped_column(Text, nullable=False)
    observed_weakness: Mapped[Text] = mapped_column(Text, nullable=False)
    proposed_improvement: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending_review", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceAssuranceLearningVersion(Base):
    __tablename__ = "transformation_resilience_assurance_learning_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version_number: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0", index=True)
    parent_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")
    changes_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    approval_state: Mapped[str] = mapped_column(String(50), nullable=False, default="approved")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceAssuranceRecommendationRegression(Base):
    __tablename__ = "transformation_resilience_assurance_recommendation_regressions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    previous_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")
    new_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    affected_dimension: Mapped[str] = mapped_column(String(100), nullable=False, default="risk_calibration")
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="low", index=True)
    description: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceAssuranceRecommendationDrift(Base):
    __tablename__ = "transformation_resilience_assurance_recommendation_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    drift_type: Mapped[str] = mapped_column(String(100), nullable=False, default="confidence_drift")
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceLesson(Base):
    __tablename__ = "transformation_resilience_assurance_lessons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_type: Mapped[str] = mapped_column(String(100), nullable=False, default="success")
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceLessonQuality(Base):
    __tablename__ = "transformation_resilience_assurance_lesson_qualities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evidence_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    recurrence_count: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.96, index=True)

# ------------------------------------------------------------------------------
# SPRINT 101 — ENTERPRISE TRANSFORMATION RESILIENCE ASSURANCE FORESIGHT 2.0 MODELS
# ------------------------------------------------------------------------------

class TransformationResilienceAssuranceForesightDomain(Base):
    __tablename__ = "transformation_resilience_assurance_foresight_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceAssuranceForesightSignal(Base):
    __tablename__ = "transformation_resilience_assurance_foresight_signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="resilience_sensing")
    type: Mapped[str] = mapped_column(String(100), nullable=False, default="trend", index=True)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    source_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    freshness: Mapped[float] = mapped_column(Float, nullable=False, default=0.98)
    consistency: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceLeadingIndicator(Base):
    __tablename__ = "transformation_resilience_assurance_leading_indicators"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    definition: Mapped[Text] = mapped_column(Text, nullable=False)
    signal_sources_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    direction: Mapped[str] = mapped_column(String(50), nullable=False, default="increasing")
    threshold: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    warning_level: Mapped[float] = mapped_column(Float, nullable=False, default=0.75)
    critical_level: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="near_term")
    state: Mapped[str] = mapped_column(String(50), nullable=False, default="watch", index=True)

class TransformationResilienceAssurancePressureSignal(Base):
    __tablename__ = "transformation_resilience_assurance_pressure_signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_pressure: Mapped[float] = mapped_column(Float, nullable=False, default=0.20)
    capacity_pressure: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    deadline_pressure: Mapped[float] = mapped_column(Float, nullable=False, default=0.75)
    evidence_pressure: Mapped[float] = mapped_column(Float, nullable=False, default=0.15)
    dependency_pressure: Mapped[float] = mapped_column(Float, nullable=False, default=0.30)
    governance_pressure: Mapped[float] = mapped_column(Float, nullable=False, default=0.10)
    conflict_pressure: Mapped[float] = mapped_column(Float, nullable=False, default=0.40)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceEmergingRisk(Base):
    __tablename__ = "transformation_resilience_assurance_emerging_risks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_name: Mapped[str] = mapped_column(String(255), nullable=False)
    signal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    affected_plans_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_transformations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="near_term", index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    uncertainty: Mapped[float] = mapped_column(Float, nullable=False, default=0.08)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="detected", index=True)

class TransformationResilienceAssuranceForecast(Base):
    __tablename__ = "transformation_resilience_assurance_forecasts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target: Mapped[str] = mapped_column(String(255), nullable=False)
    horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="near_term", index=True)
    baseline_value: Mapped[float] = mapped_column(Float, nullable=False, default=0.84)
    expected_state_value: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    lower_bound: Mapped[float] = mapped_column(Float, nullable=False, default=0.88)
    central_estimate: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    upper_bound: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    uncertainty: Mapped[float] = mapped_column(Float, nullable=False, default=0.05)
    assumptions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceForecastScenario(Base):
    __tablename__ = "transformation_resilience_assurance_forecast_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forecast_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    scenario_type: Mapped[str] = mapped_column(String(100), nullable=False, default="baseline")
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.08)
    coverage_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    capacity_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceForecastComparison(Base):
    __tablename__ = "transformation_resilience_assurance_forecast_comparisons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forecast_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    scenario_a: Mapped[str] = mapped_column(String(100), nullable=False, default="continue_current_state")
    scenario_b: Mapped[str] = mapped_column(String(100), nullable=False, default="resequence")
    comparison_summary: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceAssuranceEarlyWarning(Base):
    __tablename__ = "transformation_resilience_assurance_early_warnings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="near_term")
    affected_plans_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    recommended_attention: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

class TransformationResilienceAssuranceInterventionWindow(Base):
    __tablename__ = "transformation_resilience_assurance_intervention_windows"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    early_warning_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    opening: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    closing: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    estimated_duration_days: Mapped[int] = mapped_column(Integer, nullable=False, default=7)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    constraints: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceAssurancePreventiveOption(Base):
    __tablename__ = "transformation_resilience_assurance_preventive_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    option_type: Mapped[str] = mapped_column(String(100), nullable=False, default="do_nothing")
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    risk_reduction: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.84)
    effort: Mapped[str] = mapped_column(String(50), nullable=False, default="none")
    reversibility: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceForesightRecommendation(Base):
    __tablename__ = "transformation_resilience_assurance_foresight_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label: Mapped[str] = mapped_column(String(100), nullable=False, default="ANALYTICAL RECOMMENDATION — NOT DECISION")
    recommended_option: Mapped[str] = mapped_column(String(100), nullable=False, default="resequence")
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    forecast_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    uncertainty: Mapped[float] = mapped_column(Float, nullable=False, default=0.05)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceForecastInvalidationCondition(Base):
    __tablename__ = "transformation_resilience_assurance_forecast_invalidation_conditions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forecast_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    condition_description: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")

class TransformationResilienceAssuranceForesightQuality(Base):
    __tablename__ = "transformation_resilience_assurance_foresight_qualities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    forecast_accuracy: Mapped[float] = mapped_column(Float, nullable=False, default=0.94)
    lead_time_days: Mapped[float] = mapped_column(Float, nullable=False, default=14.0)
    false_positive_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.02)
    false_negative_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.01)
    intervention_usefulness: Mapped[float] = mapped_column(Float, nullable=False, default=0.96)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceFalsePositive(Base):
    __tablename__ = "transformation_resilience_assurance_false_positives"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    early_warning_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expected_event: Mapped[Text] = mapped_column(Text, nullable=False)
    actual_result: Mapped[Text] = mapped_column(Text, nullable=False)
    cause: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceFalseNegative(Base):
    __tablename__ = "transformation_resilience_assurance_false_negatives"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    missed_condition: Mapped[Text] = mapped_column(Text, nullable=False)
    later_materialization: Mapped[Text] = mapped_column(Text, nullable=False)
    cause: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceForesightDrift(Base):
    __tablename__ = "transformation_resilience_assurance_foresight_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    drift_type: Mapped[str] = mapped_column(String(100), nullable=False, default="calibration_drift")
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceContextShift(Base):
    __tablename__ = "transformation_resilience_assurance_context_shifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dimension: Mapped[str] = mapped_column(String(100), nullable=False, default="capacity")
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceRegimeChange(Base):
    __tablename__ = "transformation_resilience_assurance_regime_changes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="suspected", index=True)

class TransformationResilienceAssuranceForesightCluster(Base):
    __tablename__ = "transformation_resilience_assurance_foresight_clusters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cluster_name: Mapped[str] = mapped_column(String(255), nullable=False)
    signal_ids_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceSystemicEarlyWarning(Base):
    __tablename__ = "transformation_resilience_assurance_systemic_early_warnings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pattern_description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="critical", index=True)
    affected_transformations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

class TransformationResilienceAssuranceForesightCascade(Base):
    __tablename__ = "transformation_resilience_assurance_foresight_cascades"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_signal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    affected_signal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    depth: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="material", index=True)

class TransformationResilienceAssuranceForesightEscalation(Base):
    __tablename__ = "transformation_resilience_assurance_foresight_escalations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    early_warning_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    trigger_reason: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="escalated", index=True)

class TransformationResilienceAssuranceForesightLesson(Base):
    __tablename__ = "transformation_resilience_assurance_foresight_lessons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_type: Mapped[str] = mapped_column(String(100), nullable=False, default="leading_indicator")
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

# ------------------------------------------------------------------------------
# SPRINT 102 — ENTERPRISE TRANSFORMATION RESILIENCE ASSURANCE INTERVENTIONS 2.0 MODELS
# ------------------------------------------------------------------------------

class TransformationResilienceAssuranceInterventionDomain(Base):
    __tablename__ = "transformation_resilience_assurance_intervention_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceAssuranceInterventionCase(Base):
    __tablename__ = "transformation_resilience_assurance_intervention_cases"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    warning_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    forecast_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    affected_plans_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    affected_transformations_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    horizon: Mapped[str] = mapped_column(String(50), nullable=False, default="near_term")
    intervention_window: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="detected", index=True)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceInterventionTrigger(Base):
    __tablename__ = "transformation_resilience_assurance_intervention_triggers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column(String(100), nullable=False, default="early_warning", index=True)
    signal_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evidence_description: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    freshness: Mapped[float] = mapped_column(Float, nullable=False, default=0.98)
    threshold_value: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    validation_status: Mapped[str] = mapped_column(String(50), nullable=False, default="validated", index=True)

class TransformationResilienceAssuranceInterventionOption(Base):
    __tablename__ = "transformation_resilience_assurance_intervention_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    option_type: Mapped[str] = mapped_column(String(100), nullable=False, default="continue_current_state")
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    reversibility: Mapped[str] = mapped_column(String(50), nullable=False, default="reversible")
    risk_reduction: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.84)
    effort: Mapped[str] = mapped_column(String(50), nullable=False, default="none")
    capacity_required: Mapped[str] = mapped_column(String(100), nullable=False, default="0 compute nodes")
    residual_risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.25)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceRollbackPlan(Base):
    __tablename__ = "transformation_resilience_assurance_rollback_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    option_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    rollback_trigger: Mapped[Text] = mapped_column(Text, nullable=False)
    rollback_actions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    authorization_required: Mapped[str] = mapped_column(String(255), nullable=False, default="Governance Board Authorization")
    expected_recovery_time_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    residual_risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.05)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceContingencyPlan(Base):
    __tablename__ = "transformation_resilience_assurance_contingency_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    activation_criteria: Mapped[Text] = mapped_column(Text, nullable=False)
    actions_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    owners_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    capacity_reserved: Mapped[str] = mapped_column(String(100), nullable=False, default="2 backup compute nodes")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="ready", index=True)

class TransformationResilienceAssuranceContingencyReadiness(Base):
    __tablename__ = "transformation_resilience_assurance_contingency_readinesses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contingency_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evidence_readiness: Mapped[str] = mapped_column(String(50), nullable=False, default="ready")
    resource_readiness: Mapped[str] = mapped_column(String(50), nullable=False, default="ready")
    dependency_readiness: Mapped[str] = mapped_column(String(50), nullable=False, default="partially_ready")
    execution_readiness: Mapped[str] = mapped_column(String(50), nullable=False, default="ready")
    governance_readiness: Mapped[str] = mapped_column(String(50), nullable=False, default="ready")
    overall_status: Mapped[str] = mapped_column(String(50), nullable=False, default="partially_ready", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceInterventionRecommendation(Base):
    __tablename__ = "transformation_resilience_assurance_intervention_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    label: Mapped[str] = mapped_column(String(100), nullable=False, default="ANALYTICAL RECOMMENDATION — NOT DECISION")
    recommended_option_id: Mapped[str] = mapped_column(String(255), nullable=False)
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceInterventionDecisionPacket(Base):
    __tablename__ = "transformation_resilience_assurance_intervention_decision_packets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    governance_requirement: Mapped[Text] = mapped_column(Text, nullable=False)
    packet_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceInterventionPlan(Base):
    __tablename__ = "transformation_resilience_assurance_intervention_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    objective: Mapped[str] = mapped_column(String(255), nullable=False)
    selected_option_id: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="approved", index=True)

class TransformationResilienceAssuranceInterventionAction(Base):
    __tablename__ = "transformation_resilience_assurance_intervention_actions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String(100), nullable=False, default="change_sequence")
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="ready", index=True)

class TransformationResilienceAssuranceInterventionExpiration(Base):
    __tablename__ = "transformation_resilience_assurance_intervention_expirations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

class TransformationResilienceAssuranceInterventionConflict(Base):
    __tablename__ = "transformation_resilience_assurance_intervention_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    conflicting_plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    conflict_summary: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceAssuranceInterventionCascade(Base):
    __tablename__ = "transformation_resilience_assurance_intervention_cascades"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_action_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    affected_plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="material", index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)

class TransformationResilienceAssuranceInterventionImpact(Base):
    __tablename__ = "transformation_resilience_assurance_intervention_impacts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_reduction: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    coverage_change: Mapped[float] = mapped_column(Float, nullable=False, default=0.08)
    capacity_impact: Mapped[str] = mapped_column(String(100), nullable=False, default="Shifted load by 7 days")
    residual_risk: Mapped[float] = mapped_column(Float, nullable=False, default=0.08)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceInterventionEffectiveness(Base):
    __tablename__ = "transformation_resilience_assurance_intervention_effectivenesses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    lead_time_days: Mapped[float] = mapped_column(Float, nullable=False, default=14.0)
    risk_reduction: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    coverage_preservation: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    rollback_success: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceInterventionFailure(Base):
    __tablename__ = "transformation_resilience_assurance_intervention_failures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    failure_type: Mapped[str] = mapped_column(String(100), nullable=False, default="execution_failure", index=True)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    cause: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceAssuranceInterventionLesson(Base):
    __tablename__ = "transformation_resilience_assurance_intervention_lessons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_type: Mapped[str] = mapped_column(String(100), nullable=False, default="timing")
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

# ------------------------------------------------------------------------------
# SPRINT 103: Enterprise Transformation Resilience Assurance Command & Control 2.0
# ------------------------------------------------------------------------------

class TransformationResilienceAssuranceCommandDomain(Base):
    __tablename__ = "transformation_resilience_assurance_command_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # initializing, active, degraded, paused
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceAssuranceOperationalPicture(Base):
    __tablename__ = "transformation_resilience_assurance_operational_pictures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    command_domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="stable", index=True) # stable, watch, elevated, critical, degraded
    active_risks_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    active_warnings_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    active_conflicts_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    active_interventions_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    blocked_actions_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    critical_dependencies_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    capacity_pressure: Mapped[str] = mapped_column(String(100), nullable=False, default="nominal")
    decision_backlog_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    approval_backlog_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    residual_exposure: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceAssuranceCommandEvent(Base):
    __tablename__ = "transformation_resilience_assurance_command_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_domain: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    affected_objects_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="projected")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)

class TransformationResilienceAssuranceCommandPriority(Base):
    __tablename__ = "transformation_resilience_assurance_command_priorities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    object_type: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False)
    urgency: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    impact: Mapped[str] = mapped_column(String(50), nullable=False)
    intervention_window: Mapped[str] = mapped_column(String(100), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    decision_dependency: Mapped[str] = mapped_column(String(255), nullable=False, default="none")
    rank_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

class TransformationResilienceAssuranceCriticalObject(Base):
    __tablename__ = "transformation_resilience_assurance_critical_objects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # risk, warning, conflict, intervention, dependency, decision, approval, plan, transformation
    object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    deadline: Mapped[str] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")

class TransformationResilienceAssuranceCommandAttention(Base):
    __tablename__ = "transformation_resilience_assurance_command_attentions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    urgency: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    deadline: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    required_action: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceAssuranceExecutiveDecisionQueue(Base):
    __tablename__ = "transformation_resilience_assurance_executive_decision_queues"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    impact: Mapped[Text] = mapped_column(Text, nullable=False)
    deadline: Mapped[str] = mapped_column(String(100), nullable=False)
    authority_required: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True)
    blocking_objects_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)

class TransformationResilienceAssuranceDecisionBottleneck(Base):
    __tablename__ = "transformation_resilience_assurance_decision_bottlenecks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    bottleneck_type: Mapped[str] = mapped_column(String(100), nullable=False) # missing_authority, missing_evidence, approval_delay, conflicting_decisions, expired_window
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    impact: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceApprovalBottleneck(Base):
    __tablename__ = "transformation_resilience_assurance_approval_bottlenecks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    approval_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    required_authority: Mapped[str] = mapped_column(String(255), nullable=False)
    age_days: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    impact: Mapped[Text] = mapped_column(Text, nullable=False)
    blocking_actions_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceInterventionBottleneck(Base):
    __tablename__ = "transformation_resilience_assurance_intervention_bottlenecks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    intervention_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    bottleneck_cause: Mapped[str] = mapped_column(String(100), nullable=False) # blocked_action, dependency, capacity, approval, policy
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceDependencyHotspot(Base):
    __tablename__ = "transformation_resilience_assurance_dependency_hotspots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dependency_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    affected_plans_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    affected_risks_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    affected_conflicts_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    affected_interventions_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)

class TransformationResilienceAssuranceResourcePressure(Base):
    __tablename__ = "transformation_resilience_assurance_resource_pressures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_category: Mapped[str] = mapped_column(String(100), nullable=False) # compute_capacity, QA_testing_capacity, governance_review_capacity
    pressure_level: Mapped[str] = mapped_column(String(50), nullable=False, default="elevated")
    affected_plans_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    affected_interventions_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    trend: Mapped[str] = mapped_column(String(50), nullable=False, default="increasing")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.9)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceKnowledgeHealthProjection(Base):
    __tablename__ = "transformation_resilience_assurance_knowledge_health_projections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evidence_freshness: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    coverage: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    validation_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    review_backlog_count: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    staleness_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.05)
    uncertainty_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.10)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssurancePlanHealthProjection(Base):
    __tablename__ = "transformation_resilience_assurance_plan_health_projections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    plan_health: Mapped[str] = mapped_column(String(50), nullable=False, default="healthy")
    staleness: Mapped[str] = mapped_column(String(50), nullable=False, default="fresh")
    dependency_health: Mapped[str] = mapped_column(String(50), nullable=False, default="stable")
    risk_exposure: Mapped[float] = mapped_column(Float, nullable=False, default=0.12)
    execution_status: Mapped[str] = mapped_column(String(50), nullable=False, default="on_track")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceTransformationHealthProjection(Base):
    __tablename__ = "transformation_resilience_assurance_transformation_health_projections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transformation_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.15)
    coverage_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.90)
    execution_health: Mapped[str] = mapped_column(String(50), nullable=False, default="stable")
    dependency_health: Mapped[str] = mapped_column(String(50), nullable=False, default="stable")
    active_interventions_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    residual_exposure: Mapped[float] = mapped_column(Float, nullable=False, default=0.08)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceCrossDomainHeatmap(Base):
    __tablename__ = "transformation_resilience_assurance_cross_domain_heatmaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_name: Mapped[str] = mapped_column(String(100), nullable=False)
    risk_level: Mapped[float] = mapped_column(Float, nullable=False, default=0.2)
    knowledge_level: Mapped[float] = mapped_column(Float, nullable=False, default=0.9)
    capacity_level: Mapped[float] = mapped_column(Float, nullable=False, default=0.8)
    dependency_level: Mapped[float] = mapped_column(Float, nullable=False, default=0.3)
    deadline_level: Mapped[float] = mapped_column(Float, nullable=False, default=0.4)
    conflict_level: Mapped[float] = mapped_column(Float, nullable=False, default=0.2)
    intervention_level: Mapped[float] = mapped_column(Float, nullable=False, default=0.3)
    decision_level: Mapped[float] = mapped_column(Float, nullable=False, default=0.2)

class TransformationResilienceAssuranceOperationalScene(Base):
    __tablename__ = "transformation_resilience_assurance_operational_scenes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # forming, active, escalating, stabilizing, resolved, archived
    contained_objects_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceAssuranceSceneTimeline(Base):
    __tablename__ = "transformation_resilience_assurance_scene_timelines"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scene_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    stage: Mapped[str] = mapped_column(String(50), nullable=False) # detection, escalation, decision, intervention, execution, recovery
    event_description: Mapped[Text] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceAssuranceSceneRelationship(Base):
    __tablename__ = "transformation_resilience_assurance_scene_relationships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scene_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_object_id: Mapped[str] = mapped_column(String(255), nullable=False)
    target_object_id: Mapped[str] = mapped_column(String(255), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(50), nullable=False) # causes, contributes_to, depends_on, blocks, mitigates, follows, correlates_with, unknown

class TransformationResilienceAssuranceCommandSnapshot(Base):
    __tablename__ = "transformation_resilience_assurance_command_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    state_data_json: Mapped[JSON] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceCommandSnapshotDiff(Base):
    __tablename__ = "transformation_resilience_assurance_command_snapshot_diffs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    previous_snapshot_id: Mapped[str] = mapped_column(String(255), nullable=False)
    current_snapshot_id: Mapped[str] = mapped_column(String(255), nullable=False)
    new_risks_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    resolved_risks_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    new_warnings_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    resolved_warnings_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    new_conflicts_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    resolved_conflicts_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    new_interventions_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    completed_interventions_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    decision_changes_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceAssuranceCommandEscalation(Base):
    __tablename__ = "transformation_resilience_assurance_command_escalations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trigger_reason: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="detected", index=True) # detected, acknowledged, investigating, escalated, stabilizing, resolved, closed
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceAssuranceOperationsHandoff(Base):
    __tablename__ = "transformation_resilience_assurance_operations_handoffs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    outgoing_owner: Mapped[str] = mapped_column(String(255), nullable=False)
    incoming_owner: Mapped[str] = mapped_column(String(255), nullable=False)
    current_state_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    open_actions_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    risks_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    decisions_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    dependencies_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    next_review: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceAssuranceCommandAuditProjection(Base):
    __tablename__ = "transformation_resilience_assurance_command_audit_projections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_event_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    summary: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceAssuranceCommandProjectionHealth(Base):
    __tablename__ = "transformation_resilience_assurance_command_projection_healths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lag_seconds: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    errors_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_processed_event_id: Mapped[str] = mapped_column(String(255), nullable=False, default="evt_none")
    rebuild_status: Mapped[str] = mapped_column(String(50), nullable=False, default="idle")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

# ------------------------------------------------------------------------------
# SPRINT 104: Enterprise Transformation Resilience Cross-Domain Assurance Intelligence 2.0
# ------------------------------------------------------------------------------

class TransformationResilienceCrossDomainIntelligenceDomain(Base):
    __tablename__ = "transformation_resilience_cross_domain_intelligence_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True) # initializing, active, degraded, paused
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceCrossDomainResilienceGraph(Base):
    __tablename__ = "transformation_resilience_cross_domain_resilience_graphs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    total_nodes_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_edges_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceCrossDomainGraphNode(Base):
    __tablename__ = "transformation_resilience_cross_domain_graph_nodes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # transformation, portfolio, plan, risk, knowledge, evidence, decision, conflict, warning, intervention, dependency, resource, deadline, governance
    node_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    domain: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    state: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)

class TransformationResilienceCrossDomainGraphEdge(Base):
    __tablename__ = "transformation_resilience_cross_domain_graph_edges"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_node_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_node_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    relationship: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # depends_on, supports, blocks, affects, shared_with, constrained_by, derived_from, mitigates, causes, contributes_to, correlates_with, precedes, governed_by
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.9, index=True)
    evidence_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    evidence_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    last_validated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceCrossDomainPropagationPath(Base):
    __tablename__ = "transformation_resilience_cross_domain_propagation_paths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    intermediate_nodes_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    relationships_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    depth: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.9)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)

class TransformationResilienceCrossDomainPropagation(Base):
    __tablename__ = "transformation_resilience_cross_domain_propagations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_condition: Mapped[Text] = mapped_column(Text, nullable=False)
    propagation_type: Mapped[str] = mapped_column(String(100), nullable=False) # dependency, resource, deadline, evidence, decision, conflict, execution, governance, capacity, knowledge
    affected_objects_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    propagation_path_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    estimated_impact: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.9)
    uncertainty: Mapped[float] = mapped_column(Float, nullable=False, default=0.1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceCrossDomainSystemicExposure(Base):
    __tablename__ = "transformation_resilience_cross_domain_systemic_exposures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    affected_domains_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    affected_transformations_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    affected_plans_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    shared_dependencies_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    shared_resources_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="critical", index=True)
    exposure_state: Mapped[str] = mapped_column(String(50), nullable=False, default="emerging") # emerging, elevated, critical, stabilizing, resolved, unknown
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    uncertainty: Mapped[float] = mapped_column(Float, nullable=False, default=0.08)

class TransformationResilienceCrossDomainConcentration(Base):
    __tablename__ = "transformation_resilience_cross_domain_concentrations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    concentration_type: Mapped[str] = mapped_column(String(100), nullable=False) # dependency, resource, evidence, decision, transformation, deadline, knowledge domain
    object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    concentration_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceCrossDomainSinglePointExposure(Base):
    __tablename__ = "transformation_resilience_cross_domain_single_point_exposures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    component_type: Mapped[str] = mapped_column(String(100), nullable=False) # shared evidence source, shared dependency, shared infrastructure, shared approval window, shared critical milestone
    component_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    affected_systems_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)

class TransformationResilienceCrossDomainFragility(Base):
    __tablename__ = "transformation_resilience_cross_domain_fragilities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dependents_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    alternative_paths_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    recovery_options_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.9)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceCrossDomainRedundancy(Base):
    __tablename__ = "transformation_resilience_cross_domain_redundancies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    alternative_evidence_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    alternative_dependencies_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    alternative_resources_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    alternative_execution_paths_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceCrossDomainResilienceGap(Base):
    __tablename__ = "transformation_resilience_cross_domain_resilience_gaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gap_type: Mapped[str] = mapped_column(String(100), nullable=False) # missing_redundancy, single_dependency, insufficient_evidence, limited_recovery_path, governance_bottleneck, capacity_concentration
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high", index=True)
    recommended_mitigation: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceCrossDomainCompoundRisk(Base):
    __tablename__ = "transformation_resilience_cross_domain_compound_risks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    contributing_conditions_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="critical", index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)

class TransformationResilienceCrossDomainCompoundCondition(Base):
    __tablename__ = "transformation_resilience_cross_domain_compound_conditions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    compound_risk_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    condition_description: Mapped[Text] = mapped_column(Text, nullable=False)
    relationship: Mapped[str] = mapped_column(String(50), nullable=False)
    threshold: Mapped[float] = mapped_column(Float, nullable=False, default=0.7)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.9)
    evidence_ref: Mapped[str] = mapped_column(String(255), nullable=False)

class TransformationResilienceCrossDomainCascadeProjection(Base):
    __tablename__ = "transformation_resilience_cross_domain_cascade_projections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    path_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    affected_domains_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    depth: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="critical", index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.9)
    intervention_points_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)

class TransformationResilienceCrossDomainCascadeBreakpoint(Base):
    __tablename__ = "transformation_resilience_cross_domain_cascade_breakpoints"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cascade_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    location_node_id: Mapped[str] = mapped_column(String(255), nullable=False)
    option_type: Mapped[str] = mapped_column(String(100), nullable=False)
    expected_effect: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.9)
    cost: Mapped[str] = mapped_column(String(100), nullable=False, default="low")
    reversibility: Mapped[str] = mapped_column(String(50), nullable=False, default="reversible")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceCrossDomainSecondOrderEffect(Base):
    __tablename__ = "transformation_resilience_cross_domain_second_order_effects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    intervention_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    affected_object_id: Mapped[str] = mapped_column(String(255), nullable=False)
    effect_description: Mapped[Text] = mapped_column(Text, nullable=False)
    direction: Mapped[str] = mapped_column(String(50), nullable=False, default="increased_capacity_pressure") # risk_reduced, capacity_pressure_increased, deadline_improved, new_dependency_created
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.9)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceCrossDomainInterventionCollision(Base):
    __tablename__ = "transformation_resilience_cross_domain_intervention_collisions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    intervention_a_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    intervention_b_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    collision_type: Mapped[str] = mapped_column(String(50), nullable=False) # compete, conflict, cancel, amplify
    affected_domains_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    resolution: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceCrossDomainGovernanceContext(Base):
    __tablename__ = "transformation_resilience_cross_domain_governance_contexts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    required_authorities_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    decision_dependencies_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    approval_dependencies_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    policy_evaluation_ref: Mapped[str] = mapped_column(String(255), nullable=False)

class TransformationResilienceCrossDomainSystemicWarning(Base):
    __tablename__ = "transformation_resilience_cross_domain_systemic_warnings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trigger_reason: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True) # open, acknowledged, investigating, mitigating, resolved, expired, invalidated
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="critical", index=True)
    evidence_count: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

# ------------------------------------------------------------------------------
# SPRINT 105: Enterprise Transformation Resilience Digital Twin 2.0
# ------------------------------------------------------------------------------

class TransformationResilienceDigitalTwinDomain(Base):
    __tablename__ = "transformation_resilience_digital_twin_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="enterprise")
    source_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    state_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="current", index=True) # initializing, synchronizing, current, stale, degraded, paused, archived
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceDigitalTwinState(Base):
    __tablename__ = "transformation_resilience_digital_twin_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    source_event_id: Mapped[str] = mapped_column(String(255), nullable=False)
    source_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    state_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    freshness: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    completeness: Mapped[float] = mapped_column(Float, nullable=False, default=0.98)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)

class TransformationResilienceDigitalTwinSnapshot(Base):
    __tablename__ = "transformation_resilience_digital_twin_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    parent_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0")
    transformations_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    plans_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    dependencies_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    risks_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    knowledge_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    evidence_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    warnings_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    conflicts_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    interventions_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    decisions_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    resources_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    deadlines_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    state_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceDigitalTwinSynchronization(Base):
    __tablename__ = "transformation_resilience_digital_twin_synchronizations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    last_source_event_id: Mapped[str] = mapped_column(String(255), nullable=False)
    last_processed_event_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    lag_seconds: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    errors_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rebuild_status: Mapped[str] = mapped_column(String(50), nullable=False, default="idle")
    synchronization_mode: Mapped[str] = mapped_column(String(50), nullable=False, default="event_driven") # event_driven, scheduled_reconciliation, manual_rebuild
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceDigitalTwinStateDiff(Base):
    __tablename__ = "transformation_resilience_digital_twin_state_diffs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    previous_snapshot_version: Mapped[str] = mapped_column(String(50), nullable=False)
    current_snapshot_version: Mapped[str] = mapped_column(String(50), nullable=False)
    changed_objects_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    added_objects_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    removed_objects_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    changed_relationships_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDigitalTwinNode(Base):
    __tablename__ = "transformation_resilience_digital_twin_nodes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # transformation, portfolio, plan, risk, knowledge, evidence, decision, conflict, warning, intervention, dependency, resource, deadline, governance
    node_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    domain: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    state: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)

class TransformationResilienceDigitalTwinRelationship(Base):
    __tablename__ = "transformation_resilience_digital_twin_relationships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_node_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_node_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    relationship: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.9)
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    valid_to: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class TransformationResilienceDigitalTwinRealityComparison(Base):
    __tablename__ = "transformation_resilience_digital_twin_reality_comparisons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    production_state_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    twin_state_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    difference_description: Mapped[Text] = mapped_column(Text, nullable=False)
    freshness: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDigitalTwinScenarioFork(Base):
    __tablename__ = "transformation_resilience_digital_twin_scenario_forks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    base_snapshot_id: Mapped[str] = mapped_column(String(255), nullable=False)
    scenario_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc) + timedelta(days=7))

class TransformationResilienceDigitalTwinScenarioState(Base):
    __tablename__ = "transformation_resilience_digital_twin_scenario_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_fork_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    hypothetical_state_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=dict)
    isolation_level: Mapped[str] = mapped_column(String(50), nullable=False, default="strictly_isolated")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceDigitalTwinCounterfactualChange(Base):
    __tablename__ = "transformation_resilience_digital_twin_counterfactual_changes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    change_type: Mapped[str] = mapped_column(String(100), nullable=False) # dependency_failure, resource_reduction, deadline_change, scope_change, evidence_loss, risk_increase, intervention_activation, intervention_failure, external_shock
    target_object_id: Mapped[str] = mapped_column(String(255), nullable=False)
    parameters_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=dict)
    description: Mapped[Text] = mapped_column(Text, nullable=False)

class TransformationResilienceDigitalTwinCounterfactualScenario(Base):
    __tablename__ = "transformation_resilience_digital_twin_counterfactual_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    baseline_snapshot_id: Mapped[str] = mapped_column(String(255), nullable=False)
    changes_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    assumptions_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    horizon_days: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.9)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDigitalTwinScenarioOutcome(Base):
    __tablename__ = "transformation_resilience_digital_twin_scenario_outcomes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.8)
    coverage_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.9)
    capacity_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    deadline_impact_days: Mapped[int] = mapped_column(Integer, nullable=False, default=7)
    dependency_exposure_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.75)
    residual_risk_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.1)
    recovery_time_days: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDigitalTwinCounterfactualComparison(Base):
    __tablename__ = "transformation_resilience_digital_twin_counterfactual_comparisons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    baseline_id: Mapped[str] = mapped_column(String(255), nullable=False)
    scenario_id: Mapped[str] = mapped_column(String(255), nullable=False)
    difference_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    uncertainty: Mapped[float] = mapped_column(Float, nullable=False, default=0.1)

class TransformationResilienceDigitalTwinStressScenario(Base):
    __tablename__ = "transformation_resilience_digital_twin_stress_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stress_type: Mapped[str] = mapped_column(String(100), nullable=False) # capacity_stress, deadline_stress, dependency_stress, evidence_stress, governance_stress, compound_stress, external_shock
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="critical")
    affected_domains_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    recovery_impact: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDigitalTwinExternalShockScenario(Base):
    __tablename__ = "transformation_resilience_digital_twin_external_shock_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shock_name: Mapped[str] = mapped_column(String(255), nullable=False)
    affected_domains_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="high")
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False, default=14)
    recovery_assumptions_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDigitalTwinRecoveryScenario(Base):
    __tablename__ = "transformation_resilience_digital_twin_recovery_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recovery_mode: Mapped[str] = mapped_column(String(50), nullable=False) # no_recovery_action, normal_recovery, accelerated_recovery, contingency_recovery
    time_to_stabilization_days: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    risk_reduction_pct: Mapped[float] = mapped_column(Float, nullable=False, default=85.0)
    coverage_recovery_pct: Mapped[float] = mapped_column(Float, nullable=False, default=95.0)
    capacity_recovery_pct: Mapped[float] = mapped_column(Float, nullable=False, default=90.0)
    residual_exposure: Mapped[float] = mapped_column(Float, nullable=False, default=0.08)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDigitalTwinExperiment(Base):
    __tablename__ = "transformation_resilience_digital_twin_experiments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    hypothesis: Mapped[Text] = mapped_column(Text, nullable=False)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="simulation_only")
    assumptions_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    expected_result: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="approved", index=True) # draft, approved, running, completed, cancelled, invalidated
    authorization_ref: Mapped[str] = mapped_column(String(255), nullable=False, default="auth_sim_governance")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceDigitalTwinExperimentResult(Base):
    __tablename__ = "transformation_resilience_digital_twin_experiment_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    experiment_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    hypothesis: Mapped[Text] = mapped_column(Text, nullable=False)
    observed_result: Mapped[Text] = mapped_column(Text, nullable=False)
    expected_result: Mapped[Text] = mapped_column(Text, nullable=False)
    variance: Mapped[Text] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.92)
    limitations_json: Mapped[JSON] = mapped_column(JSON, nullable=False, default=list)
    snapshot_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    scenario_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDigitalTwinValidation(Base):
    __tablename__ = "transformation_resilience_digital_twin_validations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    accuracy_pct: Mapped[float] = mapped_column(Float, nullable=False, default=94.5)
    coverage_pct: Mapped[float] = mapped_column(Float, nullable=False, default=96.0)
    divergence_pct: Mapped[float] = mapped_column(Float, nullable=False, default=2.5)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDigitalTwinModelError(Base):
    __tablename__ = "transformation_resilience_digital_twin_model_errors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    error_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # state_error, relationship_error, forecast_error, propagation_error, recovery_error, unknown
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    predicted_value: Mapped[str] = mapped_column(String(255), nullable=False)
    observed_value: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TransformationResilienceDigitalTwinDrift(Base):
    __tablename__ = "transformation_resilience_digital_twin_drifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    drift_type: Mapped[str] = mapped_column(String(100), nullable=False) # state_drift, relationship_drift, behavior_drift, assumption_drift
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    drift_magnitude: Mapped[float] = mapped_column(Float, nullable=False, default=0.03)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class TransformationResilienceDigitalTwinScenarioLibrary(Base):
    __tablename__ = "transformation_resilience_digital_twin_scenario_libraries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False) # historical, baseline, stress, shock, recovery, counterfactual, experiment
    scenario_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    approved_for_reuse: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

















































































