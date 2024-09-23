import unittest
from pycron.modules.jobs.cron import Cron
from pycron.modules.jobs.exception import InvalidCronLength

class TestCronBasicFunctions(unittest.TestCase):

    def test_cron_creation(self):
        cron_str = "* * * * *"
        cron = Cron(cron_str)
        self.assertEqual(cron.cron, cron_str.split(" "))
        self.assertEqual(str(cron), "every minute\nevery hour\nevery day\nevery month\nevery day of week")


    def test_cron_creation_invalid_length(self):
        cron_str = "* * *"
        with self.assertRaises(InvalidCronLength):
            Cron(cron_str)
            