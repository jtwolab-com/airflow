import json

import pendulum

from airflow.decorators import dag, task
@dag(
    schedule_interval=None,
    start_date=pendulum.datetime(2022, 8, 1, tz="UTC"),
    catchup=False,
    tags=['example'],
)
def tutorial_taskflow_api_etl():
    """
    ### TaskFlow API Tutorial Documentation
    This is a simple ETL data pipeline example which demonstrates the use of
    the TaskFlow API using three simple tasks for Extract, Transform, and Load.
    Documentation that goes along with the Airflow TaskFlow API tutorial is
    located
    [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
    """
    @task()
    def extract():
        """
        #### Extract task
        A simple Extract task to get data ready for the rest of the data
        pipeline. In this case, getting data is simulated by reading from a
        hardcoded JSON string.
        """
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'

        order_data_dict = json.loads(data_string)
        return order_data_dict
    @task(multiple_outputs=True)
    def transform(order_data_dict: dict):
        """
        #### Transform task
        A simple Transform task which takes in the collection of order data and
        computes the total order value.
        """
        total_order_value = 0

        for value in order_data_dict.values():
            total_order_value += value

        return {"total_order_value": total_order_value}
    @task()
    def load(total_order_value: float):
        """
        #### Load task
        A simple Load task which takes in the result of the Transform task and
        instead of saving it to end user review, just prints it out.
        """

        print(f"Total order value is: {total_order_value:.2f}")
    order_data = extract()
    order_summary = transform(order_data)
    load(order_summary["total_order_value"])
tutorial_etl_dag = tutorial_taskflow_api_etl()


"""
import datetime

from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

dag = DAG(
    dag_id='test_example_bash_operator',
    default_args={'owner': 'airflow', 'retries': 3, 'start_date': datetime.datetime(2022, 8, 1)},
    schedule='@once',
)

cmd = 'ls -l'
run_this_last = EmptyOperator(task_id='run_this_last', dag=dag)

run_this = BashOperator(task_id='run_after_loop', bash_command='echo 1', dag=dag)
run_this.set_downstream(run_this_last)

for i in range(3):
    task = BashOperator(
        task_id='runme_' + str(i), bash_command='echo "{{ task_instance_key_str }}" && sleep 1', dag=dag
    )
    task.set_downstream(run_this)

task = BashOperator(
    task_id='also_run_this', bash_command='echo "run_id={{ run_id }} | dag_run={{ dag_run }}"', dag=dag
)
task.set_downstream(run_this_last)

if __name__ == "__main__":
    dag.cli()
"""

