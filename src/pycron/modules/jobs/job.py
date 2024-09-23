import logging
from typing import List
from .cron import Cron
from .cache import Cache
import subprocess
from .exception import ExecutionError

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Job:

    def __init__(self, id: str, cron: str, command: List[str]) -> None:
        self.cron = Cron(cron)
        self.command = command
        self.cache = Cache(id=id)

    def __str__(self) -> str:
        return f"{self.cron}\n{' '.join(self.command)}"

    def run(self) -> str:
        out = subprocess.run(self.command, shell=True, capture_output=True, text=True)
        if out.stderr:
            raise ExecutionError(out.stderr)
        
        log.info(out.stdout)
        return out.stdout
