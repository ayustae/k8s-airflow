"""
Submit a Spark job into the Kubernetes cluster
"""

# Imports
from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.kubernetes_pod_operator import KubernetesPodOperator

# Get the Airflow variables
k8s_config = Variable("k8s_config")
job_config = Variable("job_config")

# Arguments for the DAG
dag_args = {
        'owner': 'admin',
        'start_date': datetime.today() - timedelta(days = 1),
        'retries': 2,
        'retry_delay': timedelta(minutes = 2)
        }

# spark-submit arguments
spark_configuration = [
        "--master k8s://{}".format(k8s_config["api_endpoint"]),
        "--deploy-mode cluster",
        "--name {}".format(job_config["name"]),
        "--conf spark.executor.instances={}".format(job_config["executors"]),
        "--conf spark.kubernetes.container.image={}".format(k8s_config["image"]),
        "--conf spark.kubernetes.authenticate.driver.serviceAccountName={}".format(k8s_config["service_account"]),
        "--conf spark.kubernetes.namespace={}".format(k8s_config["namespace"]),
        "--packages org.apache.hadoop:hadoop-aws:3.2.2",
        "--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem",
        "--conf spark.jars.ivy=/tmp/.ivy",
        job_config["s3_path"].replace('s3', 's3a')
        ]

# KubernetesPodOperator configuration
_k8s_pod_config = {
        "name": "spark-client",
        "namespace": "spark",
        "image": k8s_config["image"],
        "cmds": ["/bin/spark-submit"],
        "arguments": spark_configuration,
        }

with DAG('submit_spark_job_in_k8s',
        description = 'Submit a Spark job in a Kubernetes cluster.', 
        default_args = dag_args,
        schedule_interval = ''
        ) as dag:

    submit_spark_job = KubernetesPodOperator(
            task_id     = "submit_spark_job",
            dag         = dag,
            **_k8s_pod_config
            )

    submit_spark_job
