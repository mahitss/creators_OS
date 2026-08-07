from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class WorkspaceSummary(BaseModel):
    id: str
    name: str
    root_path: str

@router.get("/workspaces", response_model=List[WorkspaceSummary])
async def list_workspaces() -> List[WorkspaceSummary]:
    return [
        WorkspaceSummary(
            id="ws_default_01",
            name="Vapor Core Engine",
            root_path="c:\\Users\\pc\\OneDrive\\Desktop\\Hack vibe"
        )
    ]
