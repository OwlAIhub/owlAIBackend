from fastapi import APIRouter, HTTPException
from database.project import create_project, get_projects, update_project, delete_project
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ProjectCreateRequest(BaseModel):
    user_id: str
    project_title: str
    goal: str
    subject_ids: List[str]

class ProjectUpdateRequest(BaseModel):
    project_title: Optional[str]
    goal: Optional[str]
    subject_ids: Optional[List[str]]

@router.post("/create")
def create_project_api(req: ProjectCreateRequest):
    try:
        project_id = create_project(req.user_id, req.project_title, req.goal, req.subject_ids)
        return {"status": "success", "project_id": project_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}")
def get_projects_api(user_id: str):
    try:
        projects = get_projects(user_id)
        return {"status": "success", "data": projects}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{project_id}/update")
def update_project_api(project_id: str, req: ProjectUpdateRequest):
    try:
        update_project(project_id, req.dict(exclude_none=True))
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{project_id}")
def delete_project_api(project_id: str):
    try:
        delete_project(project_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
