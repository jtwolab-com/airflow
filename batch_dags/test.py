from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.empty import EmptyOperator

DEFAULT_DATE = datetime(2022, 8, 1)

# DAG tests backfill with pooled tasks
# Previously backfill would queue the task but never run it
dag1 = DAG(dag_id='test_start_date_scheduling', start_date=datetime.utcnow() + timedelta(days=1))
dag1_task1 = EmptyOperator(task_id='dummy', dag=dag1, owner='airflow')

dag2 = DAG(dag_id='test_task_start_date_scheduling', start_date=DEFAULT_DATE)
dag2_task1 = EmptyOperator(
    task_id='dummy1', dag=dag2, owner='airflow', start_date=DEFAULT_DATE + timedelta(days=3)
)
dag2_task2 = EmptyOperator(task_id='dummy2', dag=dag2, owner='airflow')