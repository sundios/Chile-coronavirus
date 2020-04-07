
#### This files is a DAG that should be run on Apache Airflow
### This checks if the minsal changed the data by comparing the last row of the main DF to the current row.
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


PARENT_DAG_NAME = 'COVID19_Chile'

def branch_func(**kwargs):
    ti = kwargs['ti']
    #return value fromm minsal check that we wanna validate
    xcom_value = ti.xcom_pull("minsal_check")
    #If this value is True then we can proceed with the rest of our pipeline
    if xcom_value == 'did Minsal updated the data? Yes! they have. So now we should run all our scripts.':
        return 'continue_task'
    else:
        time.sleep(600) #This sleeps for 600 seconds, which is 10 minutes.
        return 'minsal_check'


dag = DAG(dag_id=PARENT_DAG_NAME, default_args=default_args, schedule_interval='10 10 * * *',start_date=datetime(2020, 4, 8))

# task1
task1 = BashOperator(task_id="minsal_check",
 bash_command="python  ~/dags/minsal_check.py",
 xcom_push=True, 
 dag=dag)

# pull_task = BashOperator(task_id="pull_task",
#   bash_command='echo {{  ti.xcom_pull("minsal_check") }}',
#   provide_context=True,
#   xcom_value=True,
#   dag=dag)

branch_op = BranchPythonOperator(
    task_id='branch_task',
    provide_context=True,
    python_callable=branch_func,
    dag=dag)



#Here we define the pipline
#Here we get data for Totals,Scorecard and Regiones worksheets
continue_op = BashOperator(task_id="continue_task",
 bash_command="python ~/dags/corona.py",
 dag=dag)


continue_op2 = BashOperator(task_id="Scrape_Regiones_data",
 bash_command="python ~/dags/regiones.py",
 dag=dag)


continue_op3 = BashOperator(task_id="Scrape_Paises_data",
 bash_command="python ~/dags/Paises.py",
 dag=dag)


# This task is not being used at all :/
stop_op = BashOperator(task_id="stop_task",
 bash_command="echo task is stopped.",
 xcom_push=True, 
 dag=dag)

task1 >> branch_op >> [continue_op , stop_op] 
continue_op >> continue_op2 >> continue_op3







