"""The logic layer: tasks and where they're saved. No printing, no argparse here,
so this code is easy to reuse and to test."""
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


class TaskStore:
    def __init__(self, path: Path):
        self.path = Path(path)

    def load(self) -> list[Task]:
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return [Task(**row) for row in data]

    def save(self, tasks: list[Task]) -> None:
        self.path.write_text(json.dumps([asdict(t) for t in tasks], indent=2), encoding="utf-8")

    def add(self, title: str) -> Task:
        tasks = self.load()
        task = Task(id=max((t.id for t in tasks), default=0) + 1, title=title)
        self.save([*tasks, task])
        return task

    def complete(self, task_id: int) -> Task:
        tasks = self.load()
        for task in tasks:
            if task.id == task_id:
                task.done = True
                self.save(tasks)
                return task
        raise KeyError(f"no task with id {task_id}")
