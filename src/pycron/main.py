from modules.jobs.cron import Cron
from modules.jobs.cache import Cache
import uuid

def main():

    cron = Cron("1 * * * *")
    print(cron)

    cache = Cache(id=str(uuid.uuid4()))
    cache.add("cron", "1 * * * *")
    cache.dump()
    cache.load()
    print(cache.get("cron"))


if __name__ == "__main__":
    main()