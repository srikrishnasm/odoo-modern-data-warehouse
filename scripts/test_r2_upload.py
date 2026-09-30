from config.settings import R2_BUCKET_NAME

from src.client.r2_client import R2Client


def main():

    r2 = R2Client()

    r2.upload_file(
        file_path="data/raw/res_partner.jsonl",
        bucket=R2_BUCKET_NAME,
        object_key="raw/odoo/res_partner.jsonl",
    )


if __name__ == "__main__":
    main()