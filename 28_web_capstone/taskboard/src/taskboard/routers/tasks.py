"""Task CRUD with ownership rules, filtering and pagination (Modules 22-24, 26)."""
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import func, select

from taskboard.deps import DB, CurrentUser
from taskboard.models import Status, Task, User
from taskboard.realtime import notifier
from taskboard.schemas import Page, TaskIn, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


def owned_task(db: DB, task_id: int, user: User) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(404, "task not found")
    if task.owner_id != user.id and not user.is_admin:      # authorisation, not just authentication
        raise HTTPException(403, "not your task")
    return task


@router.get("")
def list_tasks(db: DB, user: CurrentUser, status: Status | None = None,
               limit: Annotated[int, Query(ge=1, le=100)] = 20,
               offset: Annotated[int, Query(ge=0)] = 0) -> Page:
    stmt = select(Task).where(Task.owner_id == user.id)
    if status:
        stmt = stmt.where(Task.status == status)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = db.scalars(stmt.order_by(Task.id).limit(limit).offset(offset))
    return Page(total=total, items=[TaskOut.model_validate(t) for t in rows])


@router.post("", status_code=201)
async def create_task(data: TaskIn, db: DB, user: CurrentUser) -> TaskOut:
    task = Task(title=data.title, owner_id=user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    out = TaskOut.model_validate(task)
    await notifier.publish("task_created", out.model_dump())
    return out


@router.patch("/{task_id}")
async def update_task(task_id: int, data: TaskUpdate, db: DB, user: CurrentUser) -> TaskOut:
    task = owned_task(db, task_id, user)
    for field, value in data.model_dump(exclude_unset=True).items():   # only what was sent
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    out = TaskOut.model_validate(task)
    await notifier.publish("task_updated", out.model_dump())
    return out


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int, db: DB, user: CurrentUser) -> None:
    task = owned_task(db, task_id, user)
    db.delete(task)
    db.commit()
    await notifier.publish("task_deleted", {"id": task_id})
