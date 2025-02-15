import asyncio

class TaskManager:
    def __init__(self):
        self.tasks = set()

    def create_task(self, coro):
        """Создает и отслеживает асинхронную задачу"""
        task = asyncio.create_task(coro)
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)