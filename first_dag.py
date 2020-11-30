from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow import configuration as conf

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 11, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(dag_id='example_kubernetes_pod',
          schedule_interval='@once',
          default_args=default_args)

# This is where we define our desired resources.
compute_resources = \
  {'request_cpu': '100m',
  'request_memory': '1Gi',
  'limit_cpu': '100m',
  'limit_memory': '1Gi'}

with dag:
    k = KubernetesPodOperator(
        namespace="airflow",
        image="hello-world",
        labels={"foo": "bar"},
        name="airflow-test-pod",
        task_id="task-one",
        in_cluster=True,
        config_file=None,
        resources=compute_resources,
        is_delete_operator_pod=True,
        get_logs=True)
