from enum import IntEnum

__all__ = ['WSStatus']


class WSStatus(IntEnum):
    def __new__(cls, value, phrase, description=''):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.phrase = phrase
        obj.description = description
        return obj

    # informational
    RUNNING = 1000, 'runnning', 'Task is running'
    STOPPED = 4000, 'stopped', 'Task is stopped'
    PENDING = 3000, 'pending', 'Task is pending'
    FINISHED = 2000, 'finished', 'Task is finished'
    NOT_FOUND = 4004, 'not exist', 'Task is not exist'
    TASK_ERROR = 5000, 'task error', 'Task has error'