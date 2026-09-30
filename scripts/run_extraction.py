from datetime import datetime
from pathlib import Path

from src.extractors.customers import CustomerExtractor
from src.loaders.jsonl_loader import JsonlLoader
from src.utils.checkpoint import Checkpoint
from src.client.r2_client import R2Client
from config.settings import R2_BUCKET_NAME


def main():

    # --------------------------------------------------
    # 1. Create load date
    # --------------------------------------------------

    load_date = datetime.now().strftime("%Y-%m-%d")

    local_file = (
        Path("data/raw/res_partner")
        / f"load_date={load_date}"
        / "res_partner.jsonl"
    )

    r2_object_key = (
        f"raw/odoo/res_partner/"
        f"load_date={load_date}/"
        f"res_partner.jsonl"
    )


    # --------------------------------------------------
    # 2. Initialize components
    # --------------------------------------------------

    extractor = CustomerExtractor()

    loader = JsonlLoader(
        local_file
    )

    checkpoint = Checkpoint(
        "data/checkpoints/res_partner.json"
    )

    r2 = R2Client()


    # --------------------------------------------------
    # 3. Read checkpoint
    # --------------------------------------------------

    last_write_date = checkpoint.get()

    if last_write_date:
        print(
            f"Previous checkpoint: {last_write_date}"
        )
    else:
        print(
            "No checkpoint found. "
            "Running full extraction."
        )


    # --------------------------------------------------
    # 4. Extract from Odoo
    # --------------------------------------------------

    latest_write_date = extractor.extract(
        batch_size=10,
        batch_handler=loader.write_batch,
        last_write_date=last_write_date,
    )


    # --------------------------------------------------
    # 5. Upload to R2
    # --------------------------------------------------

    if latest_write_date:

        print(
            f"Latest write_date: "
            f"{latest_write_date}"
        )

        print(
            f"Local file: {local_file}"
        )

        print(
            "Uploading to Cloudflare R2..."
        )

        r2.upload_file(
            file_path=str(local_file),
            bucket=R2_BUCKET_NAME,
            object_key=r2_object_key,
        )


        # --------------------------------------------------
        # 6. Save checkpoint ONLY after upload succeeds
        # --------------------------------------------------

        checkpoint.save(
            latest_write_date
        )

        print(
            f"Checkpoint saved: "
            f"{latest_write_date}"
        )

    else:

        print(
            "No new records found."
        )


if __name__ == "__main__":
    main()