from typing import List
from models.models import Task
import json
import os

TASKS_FILE = 'tasks.json'


def read_tasks() -> List[Task]:
    if not os.path.exists(TASKS_FILE) or os.path.getsize(TASKS_FILE) == 0:
        return []
    with open(TASKS_FILE, 'r') as f:
        data = json.load(f)
    return [Task(**task) for task in data]

def write_tasks(tasks: List[Task]):
    with open(TASKS_FILE, 'w') as f:
        json.dump([task.model_dump() for task in tasks], f, indent=4)