from pathlib import Path


class AsyncClient:
    def __init__(self, rac_path: Path | str):
        self.rac_path = rac_path
