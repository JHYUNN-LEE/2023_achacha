from airflow import DAG

# Operators
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# py files
import listDo_2weeks as script1
import detailDo_2weeks as script2
import imageGet_2weeks as script3
from alert import slack_fail_alert

# ETC
from datetime import datetime
import pendulum

# 한국 시간 timezone 설정
kst = pendulum.timezone("Asia/Seoul")

# 기본 설정 변수들
args = {
    'owner': 'airflow',
    'on_failure_callback': slack_fail_alert,
    # 'depends_on_past': True
} 

dag = DAG(
    dag_id = '2weeks',
    start_date = datetime(2023, 2, 5, hour=18, tzinfo=kst),
    # every 4 hours
    schedule_interval ="0 */4 * * *",
    default_args = args

)

listDo = PythonOperator(
    task_id = 'listDo',
    python_callable = script1.listDo,
    dag=dag
)

detailDo = PythonOperator(
    task_id = 'detailDo',
    python_callable = script2.detailDo,
    dag=dag
)

imageGet = PythonOperator(
    task_id = 'imageGet',
    python_callable = script3.imageGet,
    dag=dag
)

listDo >> detailDo >> imageGet
