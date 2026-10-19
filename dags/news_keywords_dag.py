from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from src.news_keywords import load_headlines, clean_headlines, count_keywords, save_to_excel

default_args = {
    "owner": "Muskan Jain",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="News_Keywords_Pipeline",
    description="Finds the most common keywords in news headlines and saves them to Excel",
    default_args=default_args,
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
    tags=["news", "lab"],
) as dag:

    load_task = PythonOperator(
        task_id="load_headlines_task",
        python_callable=load_headlines,
    )

    clean_task = PythonOperator(
        task_id="clean_headlines_task",
        python_callable=clean_headlines,
        op_args=[load_task.output],
    )

    count_task = PythonOperator(
        task_id="count_keywords_task",
        python_callable=count_keywords,
        op_args=[clean_task.output],
    )

    save_task = PythonOperator(
        task_id="save_to_excel_task",
        python_callable=save_to_excel,
        op_args=[count_task.output],
    )

    load_task >> clean_task >> count_task >> save_task
