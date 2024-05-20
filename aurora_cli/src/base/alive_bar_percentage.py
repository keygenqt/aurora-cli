from alive_progress import alive_bar


class AliveBarPercentage:
    def __init__(self) -> None:
        super().__init__()
        self.alive_bar_instance = None

    def update(
            self,
            percentage: int,
    ) -> None:
        if not self.alive_bar_instance:
            self._dispatch_bar()
        self.bar(percentage * 0.01)
        if percentage == 100:
            self._destroy_bar()

    def _dispatch_bar(self, title: str | None = "") -> None:
        self.alive_bar_instance = alive_bar(manual=True, title=title)
        self.bar = self.alive_bar_instance.__enter__()

    def _destroy_bar(self) -> None:
        self.alive_bar_instance.__exit__(None, None, None)
