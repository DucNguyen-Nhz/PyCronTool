import unittest
from pycron.modules.jobs.job import Job
from pycron.modules.jobs.state import *
import uuid
import time


class TestJobBasicFunctions(unittest.TestCase):

    def test_job_creation(self):

        id = str(uuid.uuid4())
        cron = "1 * * * *"
        job = Job(id=id, cron=cron, command=["ls"])

        # Check job attributes
        self.assertEqual(job.cron.cron, cron.split(" "))
        self.assertEqual(job.command, ["ls"])
        self.assertEqual(job.cache._id, id)

    def test_job_run(self):

        id = str(uuid.uuid4())
        cron = "1 * * * *"
        job = Job(id=id, cron=cron, command=["ls"])
        job.run()

        # Check job attributes
        self.assertEqual(job.cron.cron, cron.split(" "))
        self.assertEqual(job.command, ["ls"])
        self.assertEqual(job.cache._id, id)


class TestJobStateBasicFunctions(unittest.TestCase):

    def test_job_init_running(self):
        context = JobContext(state=JobRunning())
        self.assertIsInstance(context._state, JobRunning)

    def test_job_init_idle(self):
        context = JobContext(state=JobIdle())
        self.assertIsInstance(context._state, JobIdle)

    def test_job_init_cancelled(self):
        context = JobContext(state=JobCancelled())
        self.assertIsInstance(context._state, JobCancelled)

    def test_job_state_transition(self):
        context = JobContext(state=JobRunning())
        self.assertIsInstance(context._state, JobRunning)

        context.transition_to(JobIdle())
        self.assertIsInstance(context._state, JobIdle)

        context = JobContext(state=JobRunning())
        context.transition_to(JobCancelled())

    def test_job_execution(self):
        context = JobContext(state=JobIdle())
        job = Job(id=str(uuid.uuid4()), cron="1 * * * *", command=["ls"])
        context.job = job

        self.assertIsInstance(context._state, JobIdle)

        context.run_job()
        self.assertIsInstance(context._state, JobRunning)
        time.sleep(1)

        context.cleanup_job()
        self.assertIsInstance(context._state, JobIdle)

    def test_job_timer(self):
        context = JobContext(state=JobIdle())
        job = Job(id=str(uuid.uuid4()), cron="1 * * * *", command=["sleep", "10"])
        context.job = job

        context.run_job()
        log.info(context._state)

        self.assertIsInstance(context._state, JobRunning)
        time.sleep(2)
        self.assertIsInstance(context._state, JobRunning)

        time.sleep(9)
        context.cleanup_job()

        self.assertIsInstance(context._state, JobIdle)

    def test_job_cancelled(self):
        context = JobContext(state=JobIdle())
        job = Job(id=str(uuid.uuid4()), cron="1 * * * *", command=["sleep", "10"])
        context.job = job

        context.run_job()
        log.info(context._state)

        self.assertIsInstance(context._state, JobRunning)
        time.sleep(2)

        context.cancel_job()
        self.assertIsInstance(context._state, JobCancelled)

        context.cleanup_job()
        self.assertIsInstance(context._state, JobIdle)
