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




















































