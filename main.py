from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, StrictInt
from typing import Optional

app = FastAPI()

tasks = []
counter = 1

class TaskCreate(BaseModel):
    title: str
    owner: str
    priority: StrictInt = 2

@app.get("/tasks")
def get_tasks(priority: Optional[str] = Query(default=None)):
    if priority is not None:
        if not priority.isdigit() or int(priority) not in (1, 2, 3):
            raise HTTPException(status_code=400, detail="Priority must be an integer between 1 and 3")
        p_val = int(priority)
        return [task for task in tasks if task["priority"] == p_val]
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def add_task(task: TaskCreate):
    global counter
    if task.priority not in (1, 2, 3):
        raise HTTPException(status_code=400, detail="Priority must be an integer between 1 and 3")
    new_task = {
        "id": counter,
        "title": task.title,
        "owner": task.owner,
        "priority": task.priority
    }
    tasks.append(new_task)
    counter += 1
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")