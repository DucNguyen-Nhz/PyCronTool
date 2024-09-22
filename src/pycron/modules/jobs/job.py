from typing import List

class Job:
    
    def __init__(self, cron: str, command: List[str]) -> None:
        self.cron = cron
        self.command = command
    
    def __str__(self) -> str:
        pass