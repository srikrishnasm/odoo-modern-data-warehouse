import json
from pathlib import Path


class Checkpoint:
    """
    Stores the last successful extraction timestamp.
    """

    def __init__(self, file_path):
        self.file_path = Path(file_path)

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def get(self):
        """
        Return the saved checkpoint.
        """

        if not self.file_path.exists():
            return None

        with self.file_path.open(
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        return data.get("last_write_date")

    def save(self, timestamp):
        """
        Save the latest successful timestamp.
        """

        with self.file_path.open(
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                {
                    "last_write_date": timestamp
                },
                file,
                indent=2
            )