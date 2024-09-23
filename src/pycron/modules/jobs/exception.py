class InvalidCronFormat(Exception):

    def __init__(self, cron: str, message: str = "Invalid Cron Format") -> None:
        self.message = f"{message}: {cron}"
        super().__init__(self.message)


class InvalidCronLength(Exception):

    def __init__(self, cron: str, message: str = "Invalid Cron Format") -> None:
        self.message = (
            f"{message}: {cron} must have 5 fields. Found {len(cron.split(' '))}"
        )
        super().__init__(self.message)

class ExecutionError(Exception):

    def __init__(self, message: str = "Execution Error") -> None:
        self.message = message
        super().__init__(self.message)