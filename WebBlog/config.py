#  django项目名/django项目名/celeryConf.py

# 任务存储
broker_url = r"redis://127.0.0.1:6379/14"
# 结果存储
result_backend = r"redis://127.0.0.1:6379/15"

# 时区
timezone = 'Asia/Shanghai'
# 过期时间
# event_queue_ttl = 5
# celery不回复结果
task_ignore_result = True

# 为防止内存泄漏，一个进程执行过N次之后杀死，建议是100次，我没听
worker_max_tasks_per_child = 10
# 错误 DatabaseWrapper objects created in a thread can only be used in that same thread
CELERY_TASK_ALWAYS_EAGER = True