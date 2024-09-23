from typing import List
from .cron import Cron

class Job:
    
    def __init__(self, cron: str, command: List[str]) -> None:
        self.cron = Cron(cron)
        self.command = command
    
    def __str__(self) -> str:
        return f"{self.cron}\n{' '.join(self.command)}"
    
    def run(self):
        pass