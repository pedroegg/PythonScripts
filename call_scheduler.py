from collections import OrderedDict
from typing import Dict, Union, Tuple, Any, OrderedDict as OrderedDictType

SERVICE_TYPE_PRIORITY_ORDER: Dict[str, int] = {'backend': 3, 'frontend': 2, 'design': 1}

class Task:
	def __init__(self, task_id: int, service: str, priority: int) -> None:
		self.id = task_id
		self.service = service
		self.priority = priority
		self.service_priority = SERVICE_TYPE_PRIORITY_ORDER.get(service, 0)

class Scheduler:
	def __init__(self) -> None:
		self.queue: OrderedDictType[str, Task] = OrderedDict()
		self.task_count_by_service: Dict[str, int] = {}

	def add(self, task_id: str, service_type: str, priority: int) -> None:
		self.queue[task_id] = Task(task_id, service_type, priority)

		if service_type not in self.task_count_by_service:
			self.task_count_by_service[service_type] = 0

		self.task_count_by_service[service_type] += 1

	def next_task_id(self) -> str:
		if len(self.queue) == 0:
			raise Exception('empty tasks queue')

		task = max(self.queue.values(), key=lambda t: (t.priority, t.service_priority))
		del self.queue[task.id]

		self.task_count_by_service[task.service] -= 1
		return task.id

	def status(self) -> Dict[str, int]:
		return self.task_count_by_service

scheduler = Scheduler()

scheduler.add('task_1', 'frontend', 3)
scheduler.add('task_2', 'frontend', 3)
scheduler.add('task_3', 'backend', 3)
scheduler.add('task_4', 'design', 4)
scheduler.add('task_5', 'backend', 1)
scheduler.add('task_6', 'design', 2)
scheduler.add('task_7', 'frontend', 5)
scheduler.add('task_8', 'frontend', 4)

print(scheduler.status())
print(scheduler.next_task_id())
print(scheduler.status())

scheduler.add('task_9', 'backend', 5)
print(scheduler.next_task_id())
print(scheduler.next_task_id())
print(scheduler.next_task_id())
print(scheduler.next_task_id())
print(scheduler.next_task_id())
print(scheduler.next_task_id())
print(scheduler.status())
