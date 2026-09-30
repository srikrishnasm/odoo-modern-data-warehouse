import json
from pathlib import Path


class JsonlLoader:
    """
    Writes records to a JSON Lines file.
    """

    def __init__(self, file_path):
        self.file_path = Path(file_path)

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def write_batch(self, records):
        """
        Append a batch of records to the JSONL file.
        """

        with self.file_path.open(
            "a",
            encoding="utf-8"
        ) as file:

            for record in records:
                file.write(
                    json.dumps(
                        record,
                        ensure_ascii=False
                    )
                    + "\n"
                )