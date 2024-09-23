import unittest
from pycron.modules.jobs.job import Job
import uuid
import subprocess


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
        output = job.run()

        out = subprocess.run(["ls"], shell=True, capture_output=True, text=True)

        # Check job attributes
        self.assertEqual(job.cron.cron, cron.split(" "))
        self.assertEqual(job.command, ["ls"])
        self.assertEqual(job.cache._id, id)

        # Check job output
        self.assertEqual(output, out.stdout)