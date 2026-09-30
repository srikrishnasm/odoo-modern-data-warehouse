from datetime import datetime
from pathlib import Path

from src.extractors.product_products import ProductExtractor
from src.loaders.jsonl_loader import JsonlLoader
from src.utils.checkpoint import Checkpoint
from src.client.r2_client import R2Client
from config.settings import R2_BUCKET_NAME


def main():
    load_date = datetime.now().strftime("%Y-%m-%d")

    local_file = (
        Path("data/raw/product")
        / f"load_date={load_date}"
        / "product.jsonl"
    )

    r2_object_key = (
        f"raw/odoo/product/"
        f"load_date={load_date}/"
        f"product.jsonl"
    )

    extractor = ProductExtractor()
    loader = JsonlLoader(local_file)
    checkpoint = Checkpoint(
        "data/checkpoints/product.json"
    )
    r2 = R2Client()

    last_write_date = checkpoint.get()

    if last_write_date:
        print(f"Previous checkpoint: {last_write_date}")
    else:
        print("No checkpoint found. Running full extraction.")

    latest_write_date = extractor.extract(
        batch_size=10,
        batch_handler=loader.write_batch,
        last_write_date=last_write_date,
    )

    if latest_write_date:
        print(f"Latest write_date: {latest_write_date}")
        print(f"Local file: {local_file}")
        print("Uploading to Cloudflare R2...")

        r2.upload_file(
            file_path=str(local_file),
            bucket=R2_BUCKET_NAME,
            object_key=r2_object_key,
        )

        checkpoint.save(latest_write_date)
        print(f"Checkpoint saved: {latest_write_date}")
    else:
        print("No new records found.")


if __name__ == "__main__":
    main()