from fastapi import FastAPI, HTTPException
from typing import List, Optional
from datetime import datetime
from models.models import Task, TaskCreate, TaskStatusUpdate, TaskUpdate
from utils import read_tasks, write_tasks


app = FastAPI()


@app.post('/add', response_model=Task, status_code=201)
def add_task(task_create: TaskCreate):
    """
    Adds a new task to the task list.
    
    Args:
        task_create (TaskCreate): Task creation data (description).
        
    Returns:
        Task: The newly created task.
        
    Raises:
        None
    """
    tasks = read_tasks()
    new_id = tasks[-1].id + 1 if tasks else 1
    now = datetime.utcnow().isoformat()
    new_task = Task(
        id=new_id,
        description=task_create.description,
        status="Not completed",
        created_at=now,
        updated_at=now
    )
    tasks.append(new_task)
    write_tasks(tasks)
    return new_task


@app.delete('/delete/{task_id}', status_code=204)
def delete_task(task_id: int):
    """
    Deletes a task by its ID.
    
    Args:
        task_id (int): The ID of the task to delete.
        
    Returns:
        None
        
    Raises:
        HTTPException: If the task is not found (404).
    """
    tasks = read_tasks()
    new_tasks = [task for task in tasks if task.id != task_id]

    if len(new_tasks) == len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    
    write_tasks(new_tasks)
    return


@app.patch('/update/{task_id}', response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    """
    Updates a task's description by its ID.
    
    Args:
        task_id (int): The ID of the task to update.
        task_update (TaskUpdate): Data for updating the task (new description).
        
    Returns:
        Task: The updated task.
        
    Raises:
        HTTPException: If the task is not found (404).
    """
    tasks = read_tasks()

    for task in tasks:
        if task.id == task_id:
            task.description = task_update.description
            task.updated_at = datetime.utcnow().isoformat()
            write_tasks(tasks)
            return task
        
    raise HTTPException(status_code=404, detail="Task not found")


@app.get('/allTasks', response_model=List[Task])
def get_all_tasks(status_filter: Optional[str] = None):
    """
    Retrieves all tasks, optionally filtering by status.
    
    Args:
        status_filter (Optional[str]): Filter tasks by status ('done', 'todo', 'in-progress').
        
    Returns:
        List[Task]: A list of tasks that match the filter, or all tasks if no filter is provided.
        
    Raises:
        HTTPException: If the status filter is invalid (400).
    """
    valid_filters = {"done": "Done", "todo": "Not completed", "in-progress": "In progress"}

    if status_filter and status_filter not in valid_filters:
        raise HTTPException(status_code=400, detail="Invalid filter")
    
    tasks = read_tasks()
    if status_filter:
        filtered_status = valid_filters[status_filter]
        tasks = [task for task in tasks if task.status == filtered_status]

    return tasks


@app.patch('/mark/{task_id}', response_model=Task)
def mark_task(task_id: int, task_status_update: TaskStatusUpdate):
    """
    Updates the status of a task (mark as 'Done' or 'In progress').
    
    Args:
        task_id (int): The ID of the task to mark.
        task_status_update (TaskStatusUpdate): Data for updating the task status.
        
    Returns:
        Task: The task with the updated status.
        
    Raises:
        HTTPException: If the status is invalid (400) or if the task is not found (404).
    """
    valid_statuses = ["Done", "In progress"]

    if task_status_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    tasks = read_tasks()
    for task in tasks:
        if task.id == task_id:
            task.status = task_status_update.status
            task.updated_at = datetime.utcnow().isoformat()
            write_tasks(tasks)
            return task
        
    raise HTTPException(status_code=404, detail="Task not found")
