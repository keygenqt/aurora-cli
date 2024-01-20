from pathlib import Path


class Conf:
    def __init__(self, path):
        if path is not None and Path(path).is_file() and path.lower().endswith('.yaml'):
            self.path = Path(path)
        else:
            self.path = Path.home() / ".aurora-cli" / "configuration.yaml"
