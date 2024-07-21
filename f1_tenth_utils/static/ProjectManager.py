import os

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ProjectManager(metaclass=SingletonMeta):
    def __init__(self):
        self.value = None
        self.src_code_path = None
        self.projects_path = None
