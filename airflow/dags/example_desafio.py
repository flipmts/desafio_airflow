from airflow.utils.edgemodifier import Label
from datetime import datetime, timedelta
from textwrap import dedent
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow import DAG
from airflow.models import Variable
import sqlite3
import pandas as pd

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


## Do not change the code below this line ---------------------!!#
def export_final_answer():
    import base64

    # Import count
    with open('count.txt') as f:
        count = f.readlines()[0]

    my_email = Variable.get("my_email")
    message = my_email+count
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    with open("final_output.txt","w") as f:
        f.write(base64_message)
    return None
## Do not change the code above this line-----------------------##

def extract_order():
    con = sqlite3.connect('/home/felipe/airflow_tooltorial/data/Northwind_small.sqlite')
    df = pd.read_sql_query('select * from "Order";', con)
    df.to_csv('/home/felipe/airflow_tooltorial/data/output_orders.csv')
    con.close()
    
def export_count():
    con = sqlite3.connect("/home/felipe/airflow_tooltorial/data/Northwind_small.sqlite")
    order_detail = pd.read_sql_query("select * from OrderDetail;", con)
    orders = pd.read_csv("/home/felipe/airflow_tooltorial/data/output_orders.csv")
    df = pd.merge(order_detail, orders, how="inner", left_on="OrderId", right_on="Id")
    filtered_df = df.query('ShipCity == "Rio de Janeiro"')
    count = str(filtered_df["Quantity"].sum())
    with open("count.txt", 'w') as f:
        f.write(count)
    con.close()

with DAG(
    'DesafioAirflow',
    default_args=default_args,
    description='Desafio de Airflow da Indicium',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:
    dag.doc_md = """
        Esse é o desafio de Airflow da Indicium.
    """
   
    export_final_output = PythonOperator(
        task_id='export_final_output',
        python_callable=export_final_answer,
        provide_context=True
    )
    
    export_order_csv = PythonOperator(
        task_id='extract_order_csv',
        python_callable=extract_order,
        provide_context=True
    )
        
    export_count_csv = PythonOperator(
        task_id='export_count_csv',
        python_callable=export_count,
        provide_context=True
    )

export_order_csv >> export_count_csv >> export_final_output