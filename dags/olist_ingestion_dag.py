"""
DAG pour orchestrer l'ingestion des données Olist dans Snowflake.

Ce DAG charge les 9 fichiers CSV du dataset Olist dans la couche RAW
(bronze) de Snowflake. Il s'exécute quotidiennement, avec retries et
alertes en cas d'échec.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
import sys
import os

# Permet d'importer le module d'ingestion depuis /opt/airflow/ingestion
sys.path.insert(0, "/opt/airflow")

default_args = {
    "owner": "achraf",
    "depends_on_past": False,
    "email": ["exemple@exemple.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


def run_ingestion(**context):
    """Wrapper qui appelle la fonction main() du script d'ingestion."""
    from ingestion.load_to_snowflake import main
    main()


with DAG(
    dag_id="olist_ingestion",
    default_args=default_args,
    description="Load Olist CSV data into Snowflake RAW layer",
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["olist", "ingestion", "bronze"],
) as dag:

    start = EmptyOperator(task_id="start")

    ingest_olist_data = PythonOperator(
        task_id="ingest_olist_data",
        python_callable=run_ingestion,
    )

    end = EmptyOperator(task_id="end")

    start >> ingest_olist_data >> end