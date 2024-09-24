import logging
import subprocess, multiprocessing
from typing import List, Callable
from .cron import Cron
from .cache import Cache
from .exception import ExecutionError


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Job:

    def __init__(self, id: str, cron: str, command: List[str]) -> None:
        self.cron = Cron(cron)
        self.command = command
        self.cache = Cache(id=id)
        self.pid = None
        self._process = None

    def __str__(self) -> str:
        return f"{self.cron}\n{' '.join(self.command)}"

    def is_alive(self) -> bool:
        return self._process is not None and self._process.is_alive()

    def _run(self, callable: Callable) -> None:
        proc = subprocess.run(
            self.command,
            stdout=subprocess.PIPE,
            shell=True,
            text=True,
        )

        if proc.stderr is not None:
            raise ExecutionError(proc.stderr)

        log.info(proc.stdout)
        if callable is not None:
            callable()

    def run(self, **kwargs) -> str:
        callable: Callable = kwargs.get("callable", None)
        self._process = multiprocessing.Process(target=self._run, args=(callable,))
        self._process.start()

    def cancel(self):
        if self._process is not None:
            self._process.terminate()
