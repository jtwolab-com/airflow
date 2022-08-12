import os
from datetime import datetime, timedelta

# [START import_module]
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor

# [END import_module]


# [START instantiate_dag]
ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "spark_pi"

with DAG(
    DAG_ID,
    default_args={'max_active_runs': 1},
    description='submit spark-pi as sparkApplication on kubernetes',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 8, 11),
    catchup=False,
) as dag:
    # [START SparkKubernetesOperator_DAG]
    t1 = SparkKubernetesOperator(
        task_id='spark_pi_submit',
        namespace="default",
        application_file="example_spark_kubernetes_spark_pi.yaml",
        do_xcom_push=True,
        dag=dag,
    )

    t2 = SparkKubernetesSensor(
        task_id='spark_pi_monitor',
        namespace="default",
        application_name="{{ task_instance.xcom_pull(task_ids='spark_pi_submit')['metadata']['name'] }}",
        dag=dag,
    )
    t1 >> t2

    # [END SparkKubernetesOperator_DAG]
    from tests.system.utils.watcher import watcher

    # This test needs watcher in order to properly mark success/failure
    # when "tearDown" task with trigger rule is part of the DAG
    list(dag.tasks) >> watcher()

from tests.system.utils import get_test_run  # noqa: E402

# Needed to run the example DAG with pytest (see: tests/system/README.md#run_via_pytest)
test_run = get_test_run(dag)
