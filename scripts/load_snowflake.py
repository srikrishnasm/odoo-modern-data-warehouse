import os

import snowflake.connector
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE"),
    )


def load_data():
    conn = get_connection()

    try:
        cursor = conn.cursor()
        # Load res_partner (customers)
        print("Loading customers into Snowflake...")

        cursor.execute("""
            COPY INTO ODOO_DWH.RAW.RES_PARTNER
            FROM (
                SELECT
                    $1:id::NUMBER,
                    $1:name::VARCHAR,
                    $1:email::VARCHAR,
                    $1:phone::VARCHAR,
                    $1:create_date::TIMESTAMP_NTZ,
                    $1:write_date::TIMESTAMP_NTZ
                FROM @ODOO_R2_STAGE
            )
            FILE_FORMAT = (
                FORMAT_NAME = 'ODOO_DWH.RAW.ODOO_JSON_FORMAT'
            )
            PATTERN = '.*res_partner/load_date=.*\\.jsonl'
            ON_ERROR = 'ABORT_STATEMENT'
        """)

        print("Customer COPY completed.")
        
        # Load sale order
        print("Loading sales orders into Snowflake...")

        cursor.execute("""
            COPY INTO ODOO_DWH.RAW.SALE_ORDER
            FROM (
                SELECT
                    $1:id::NUMBER,
                    $1:name::VARCHAR,
                    $1:partner_id[0]::NUMBER,
                    $1:date_order::TIMESTAMP_NTZ,
                    $1:state::VARCHAR,
                    $1:amount_total::NUMBER(18,2),
                    $1:create_date::TIMESTAMP_NTZ,
                    $1:write_date::TIMESTAMP_NTZ
                FROM @ODOO_R2_STAGE
            )
            FILE_FORMAT = (
                FORMAT_NAME = 'ODOO_DWH.RAW.ODOO_JSON_FORMAT'
            )
            PATTERN = '.*sale_order/load_date=.*\\.jsonl'
            ON_ERROR = 'ABORT_STATEMENT'
        """)

        print("Sales order COPY completed.")

        # Load sale order lines
        print("Loading sales order lines into Snowflake...")
        cursor.execute("""
            COPY INTO ODOO_DWH.RAW.SALE_ORDER_LINE
            FROM (
                SELECT
                    $1:id::NUMBER,
                    $1:order_id[0]::NUMBER,
                    $1:product_id[0]::NUMBER,
                    $1:product_uom_qty::NUMBER(18,2),
                    $1:price_unit::NUMBER(18,2),
                    $1:price_subtotal::NUMBER(18,2),
                    $1:create_date::TIMESTAMP_NTZ,
                    $1:write_date::TIMESTAMP_NTZ
                FROM @ODOO_R2_STAGE
            )
            FILE_FORMAT = (
                FORMAT_NAME = 'ODOO_DWH.RAW.ODOO_JSON_FORMAT'
            )
            PATTERN = '.*sale_order_line/load_date=.*\\.jsonl'
            ON_ERROR = 'ABORT_STATEMENT'
        """)

        print("Sale Order Line COPY Completed.")


        # Load products
        print("Loading products into Snowflake...")
        cursor.execute("""
            COPY INTO ODOO_DWH.RAW.PRODUCT
            FROM (
                SELECT
                    $1:id::NUMBER,
                    $1:name::VARCHAR,
                    $1:default_code::VARCHAR,
                    $1:list_price::NUMBER(18,2),
                    $1:create_date::TIMESTAMP_NTZ,
                    $1:write_date::TIMESTAMP_NTZ
                FROM @ODOO_R2_STAGE
            )
            FILE_FORMAT = (
                FORMAT_NAME = 'ODOO_DWH.RAW.ODOO_JSON_FORMAT'
            )
            PATTERN = '.*product/load_date=.*\\.jsonl'
            ON_ERROR = 'ABORT_STATEMENT'
        """)

        print("Product COPY completed.")

    finally:
        conn.close()


if __name__ == "__main__":
    load_data()