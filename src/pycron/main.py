from modules.jobs.cron import Cron
from modules.jobs.cache import Cache
from modules.jobs.job import Job
import uuid

import logging

log = logging.basicConfig()

def main():

    # cron = Cron("1 * * * *")
    # print(cron)

    # cache = Cache(id=str(uuid.uuid4()))
    # cache.add("cron", "1 * * * *")
    # cache.dump()
    # cache.load()
    # print(cache.get("cron"))

    job = Job(id=str(uuid.uuid4()), cron="1 * * * *", command=["ls"])
    job.run()


if __name__ == "__main__":
    main()