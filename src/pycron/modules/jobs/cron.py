from .exception import InvalidCronLength


def _parse_crontab(cron: str, pos: str):
    """
    *	any value
    ,	value list separator
    -	range of values
    /	step values
    """

    cron = cron.strip()
    if cron == "*":
        return f"every {pos}"

    if "," in cron:
        return f"at {pos} {cron} in {cron}"

    if "-" in cron:
        return f'from {cron.split("-")[0]} to {cron.split("-")[1]} {pos}'

    if "/" in cron:
        return f'every {cron.split("/")[1]} {pos}'
    
    if cron.isdigit():
        return f"at {pos} {cron}"

class Cron:
    def __init__(self, cron: str) -> None:
        self.cron = cron.split(" ")
        if len(self.cron) != 5:
            raise InvalidCronLength(cron)

    def __str__(self) -> str:
        return (
            _parse_crontab(self.cron[0], "minute")
            + "\n"
            + _parse_crontab(self.cron[1], "hour")
            + "\n"
            + _parse_crontab(self.cron[2], "day")
            + "\n"
            + _parse_crontab(self.cron[3], "month")
            + "\n"
            + _parse_crontab(self.cron[4], "day of week")
        )
    

    def til_next(self):
        pass

    def from_last(self):
        pass

    def has_been(self):
        pass
    