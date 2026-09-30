from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_DIR = "/home/pc/Documents/odoo-data-extractor"
PROJECT_PYTHON = f"{PROJECT_DIR}/airflow_venv/bin/python"
DBT_PATH = f"{PROJECT_DIR}/dbt/.venv/bin/dbt"


default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}


with DAG(
    dag_id="odoo_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["odoo", "data-engineering"],
) as dag:

    extract_customers = BashOperator(
        task_id="extract_customers",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            f"{PROJECT_PYTHON} -m scripts.run_extraction"
        ),
    )

    extract_sale_orders = BashOperator(
        task_id="extract_sale_orders",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            f"{PROJECT_PYTHON} -m scripts.run_sale_order_extraction"
        ),
    )

    extract_sale_order_lines = BashOperator(
        task_id="extract_sale_order_lines",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            f"{PROJECT_PYTHON} -m scripts.run_sale_order_line_extraction"
        ),
    )

    extract_products = BashOperator(
        task_id="extract_products",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            f"{PROJECT_PYTHON} -m scripts.run_product_extraction"
        ),
    )

    load_snowflake = BashOperator(
        task_id="load_snowflake",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            f"{PROJECT_PYTHON} scripts/load_snowflake.py"
        ),
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            f"cd {PROJECT_DIR}/dbt/odoo_analytics && "
            f"{DBT_PATH} run"
        ),
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            f"cd {PROJECT_DIR}/dbt/odoo_analytics && "
            f"{DBT_PATH} test"
        ),
    )

    extract_customers >> extract_sale_orders >> extract_sale_order_lines >> extract_products >> load_snowflake >> dbt_run >> dbt_test