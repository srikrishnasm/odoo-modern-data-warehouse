from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def hello():
    print("Airflow is working successfully!")


with DAG(
    dag_id="odoo_test_dag",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    test_task = PythonOperator(
        task_id="test_airflow",
        python_callable=hello,
    )