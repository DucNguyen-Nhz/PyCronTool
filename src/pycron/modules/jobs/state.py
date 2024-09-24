from __future__ import annotations
from abc import ABC, abstractmethod
import logging
from .job import Job

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class JobState(ABC):

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context: JobContext) -> None:
        self._context = context

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass

    @abstractmethod
    def cancel(self):
        pass


class JobContext:

    _state = None

    @property
    def job(self) -> Job:
        return self._job

    @job.setter
    def job(self, job: Job) -> None:
        self._job = job

    def __init__(self, state: JobState) -> None:
        if state is None:
            raise ValueError("State must not be None")

        self.transition_to(state)

    def run_job(self):
        if self.job is None:
            raise ValueError("Job must not be None")

        self._state.run()

    def cleanup_job(self):

        if self.job is None:
            raise ValueError("Job must not be None")
        
        if self.job.is_alive():
            log.warning("Job is still running")
            return
        
        self._state.cleanup()

    def cancel_job(self):

        log.warning("Cancelling job")
        if self.job is None:
            raise ValueError("Job must not be None")

        self._state.cancel()

    def transition_to(self, state: JobState):
        self._state = state
        self._state.context = self


class JobIdle(JobState):

    def run(self):
        log.info("Job Idle - Running job")
        self.context.job.run(callable=self.context.cleanup_job)
        self.context.transition_to(JobRunning())

    def cleanup(self):
        log.info("Job Idle - Nothing to clean up")

    def cancel(self):
        log.info("Job Idle - Nothing to cancel")


class JobRunning(JobState):

    def run(self):
        log.info("Job Running - Job is already running")

    def cleanup(self):
        log.info("Job Running - Cleaning up job")
        self.context.transition_to(JobIdle())

    def cancel(self):
        log.info("Job Running - Cancelling job")
        self.context.job.cancel()
        self.context.transition_to(JobCancelled())

class JobCancelled(JobState):

    def run(self):
        log.info("Job Cancelled - Re-running job")
        self.context.job.run(callable=self.cleanup)
        self.context.transition_to(JobRunning())

    def cleanup(self):
        log.info("Job Cancelled - Job is already cancelled")
        self.context.transition_to(JobIdle())

    def cancel(self):
        log.info("Job Cancelled - Job is already cancelled")
