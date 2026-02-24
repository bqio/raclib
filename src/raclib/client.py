from pathlib import Path


class Client:
    def __init__(self, rac_path: Path | str):
        self.rac_path = rac_path
