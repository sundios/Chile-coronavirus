
#### This files is a DAG that shold  be run on Apache Airflow
### The checks if the minsal changed the data by comparing the last row of the main DF to the current row.
### If value is the same then the data has not been changed, so we need to add a time.sleep(10 min or something) so that we can check every 10 min
### If value is different then data has been updated and we can run our Pipeline.
### Work in progress

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
import time


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date":datetime(year=2019, month=11, day=9),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}


PARENT_DAG_NAME = 'COVID19_Chile191'

def branch_func(**kwargs):
    ti = kwargs['ti']
    #return value fromm minsal check that we wanna validate
    xcom_value = ti.xcom_pull("minsal_check")
    #If this value is True then we can proceed with the rest of our pipeline
    if xcom_value == 'did Minsal updated the data? Yes! they have. So now we should run all our scripts.':
        return 'continue_task'
    else:
        return 'minsal_check'


dag = DAG(dag_id=PARENT_DAG_NAME, default_args=default_args, schedule_interval='10 10 * * *',start_date=datetime(2020, 4, 3))

# task1
task1 = BashOperator(task_id="minsal_check",
 bash_command="python  ~/dags/minsal_check.py",
 xcom_push=True, 
 dag=dag)

# pull_task = BashOperator(task_id="pull_task",
# 	bash_command='echo {{  ti.xcom_pull("minsal_check") }}',
# 	provide_context=True,
# 	xcom_value=True,
# 	dag=dag)

branch_op = BranchPythonOperator(
    task_id='branch_task',
    provide_context=True,
    python_callable=branch_func,
    dag=dag)

#Here we define the pipline
continue_op = BashOperator(task_id="continue_task",
 bash_command="echo Now we run all the scripts to get values and push them live",
 dag=dag)


# This task is not being used at all :/
stop_op = BashOperator(task_id="stop_task",
 bash_command="echo task is stopped.",
 xcom_push=True, 
 dag=dag)


task1 >> branch_op >> [continue_op, stop_op]

