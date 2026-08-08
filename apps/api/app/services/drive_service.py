import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Tuple, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import integration_service, mission_service

_in_memory_files: Dict[str, dict] = {}
_in_memory_mission_docs: Dict[str, dict] = {}
MAX_EXTRACTED_CHARS = 50000

async def sync_drive_data(
    session: Optional[AsyncSession],
    workspace_id: str
) -> dict:
    conn = await integration_service.get_connection(session, workspace_id, "google")
    if not conn or conn["status"] != "connected":
        raise ValueError("Google integration is not connected. Drive sync requires Google OAuth.")

    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()

    # 1. Sync Sample Google Doc File
    f_1_id = f"file_doc_01_{workspace_id}"
    f_1 = {
        "id": f_1_id,
        "workspace_id": workspace_id,
        "integration_id": conn["id"],
        "external_file_id": "ext_drive_01",
        "name": "Q3 Platform Architecture Proposal",
        "mime_type": "application/vnd.google-apps.document",
        "description": "Comprehensive specification for Vapor OS scaling.",
        "web_url": "https://docs.google.com/document/d/ext_drive_01/edit",
        "owner_name": conn.get("external_account_name", "Alex"),
        "size_bytes": 45000,
        "created_time": (now - timedelta(days=5)).isoformat(),
        "modified_time": (now - timedelta(hours=2)).isoformat(),
        "trashed": False,
        "parent_external_id": None,
        "external_updated_at": now_iso,
        "created_at": now_iso,
        "updated_at": now_iso,
        "_sample_content": "# Q3 Platform Architecture Proposal\n\nExecutive Summary:\nThis document details the scaling requirements for Vapor OS execution engine and memory vault."
    }

    # 2. Sync Sample PDF File
    f_2_id = f"file_pdf_02_{workspace_id}"
    f_2 = {
        "id": f_2_id,
        "workspace_id": workspace_id,
        "integration_id": conn["id"],
        "external_file_id": "ext_drive_02",
        "name": "Creator OS Pricing & Guidelines 2026",
        "mime_type": "application/pdf",
        "description": "Standard tier pricing and legal guidelines.",
        "web_url": "https://drive.google.com/file/d/ext_drive_02/view",
        "owner_name": conn.get("external_account_name", "Alex"),
        "size_bytes": 120000,
        "created_time": (now - timedelta(days=10)).isoformat(),
        "modified_time": (now - timedelta(days=1)).isoformat(),
        "trashed": False,
        "parent_external_id": None,
        "external_updated_at": now_iso,
        "created_at": now_iso,
        "updated_at": now_iso,
        "_sample_content": "Page 1:\nCreator OS Tier Specifications and Enterprise Pricing matrix.\nPage 2:\nLegal compliance, data isolation, and SLA guarantees."
    }

    _in_memory_files[f_1_id] = f_1
    _in_memory_files[f_2_id] = f_2

    await integration_service.refresh_connection(session, workspace_id, "google")

    return {
        "is_connected": True,
        "last_synced_at": now_iso,
        "file_count": 2
    }

async def list_drive_files(
    session: Optional[AsyncSession],
    workspace_id: str,
    search_query: Optional[str] = None,
    mime_type: Optional[str] = None
) -> Tuple[List[dict], int]:
    files = [
        f for f in _in_memory_files.values()
        if f["workspace_id"] == workspace_id and not f["trashed"]
    ]

    if search_query:
        sq = search_query.lower()
        files = [
            f for f in files
            if sq in f["name"].lower() or sq in f["description"].lower()
        ]

    if mime_type:
        files = [f for f in files if f["mime_type"] == mime_type]

    files.sort(key=lambda x: x["modified_time"], reverse=True)
    return files, len(files)

async def get_drive_file(
    session: Optional[AsyncSession],
    workspace_id: str,
    file_id: str
) -> Optional[dict]:
    f = _in_memory_files.get(file_id)
    if not f or f["workspace_id"] != workspace_id:
        return None
    return f

async def extract_file_content(
    session: Optional[AsyncSession],
    workspace_id: str,
    file_id: str
) -> dict:
    f = await get_drive_file(session, workspace_id, file_id)
    if not f:
        raise ValueError("Drive file not found.")

    supported_mimes = [
        "application/vnd.google-apps.document",
        "application/pdf",
        "text/plain",
        "text/markdown"
    ]

    if f["mime_type"] not in supported_mimes:
        raise ValueError(f"Content extraction is not supported for binary MIME type '{f['mime_type']}'.")

    raw_text = f.get("_sample_content", f"Extracted contents of document '{f['name']}'.")
    is_truncated = len(raw_text) > MAX_EXTRACTED_CHARS
    final_text = raw_text[:MAX_EXTRACTED_CHARS]

    return {
        "file_id": file_id,
        "name": f["name"],
        "mime_type": f["mime_type"],
        "text": final_text,
        "pages": 2 if f["mime_type"] == "application/pdf" else 1,
        "truncated": is_truncated
    }

async def attach_document_to_mission(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str,
    file_id: str
) -> dict:
    f = await get_drive_file(session, workspace_id, file_id)
    if not f:
        raise ValueError("Drive file not found.")

    mission = await mission_service.get_mission_by_id(session, workspace_id, mission_id)
    if not mission:
        raise ValueError("Mission not found.")

    ref_id = f"ref_{mission_id}_{file_id}"
    now_iso = datetime.now(timezone.utc).isoformat()
    ref = {
        "id": ref_id,
        "workspace_id": workspace_id,
        "mission_id": mission_id,
        "drive_file_id": file_id,
        "file_name": f["name"],
        "mime_type": f["mime_type"],
        "web_url": f["web_url"],
        "added_by": "usr_alex",
        "created_at": now_iso
    }

    _in_memory_mission_docs[ref_id] = ref
    return ref

async def list_mission_documents(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> List[dict]:
    refs = [
        r for r in _in_memory_mission_docs.values()
        if r["workspace_id"] == workspace_id and r["mission_id"] == mission_id
    ]
    return refs
