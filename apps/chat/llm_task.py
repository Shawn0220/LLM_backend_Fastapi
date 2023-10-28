import threading

class LLMTask(object):
    def __init__(self, task_id, user_id, manager, session_id, chat_history_id, *args, **kwargs):
        self.task_id = task_id
        self.user_id = user_id
        self.manager = manager
        self.session_id = session_id
        self.chat_history_id = chat_history_id
        self.is_stopped = False
        self.is_scheduled = False
        self.future = None
        self.args = args
        self.lock = threading.RLock()
        self.extra_info = None

    def set_future(self, future):
        self.future = future

    def cancel(self):
        with self.lock:
            self.is_stopped = True
            if self.future is not None:
                print(f'taskID:{self.task_id}, future:{self.future} is canceling, {self.future.cancel()}')
                self.future.cancel()

    def set_extra_info(self, extra_info):
        self.extra_info = extra_info

