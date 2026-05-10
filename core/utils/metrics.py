from prometheus_client import Gauge, Counter, Histogram

queue_size = Gauge(
    "taskiq_queue_size",
    "Count of tasks in PENDING status"
)

tasks_completed = Counter(
    "taskiq_tasks_completed_total",
    "Total count of completed tasks",
    ["task_name"]
)

tasks_failed = Counter(
    "taskiq_tasks_failed_total",
    "Total count of failed tasks",
    ["task_name"]
)

task_duration = Histogram(
    "taskiq_tasks_duration_seconds",
    "Task execution duration in seconds",
    ["task_name"]
)