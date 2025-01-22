from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import pandas as pd
import os
from sqlalchemy import create_engine

# Configuración de base de datos
db_path = "etl_database.db"
engine = create_engine(f"sqlite:///{db_path}")

# Ruta de datos
processed_folder = r"C:\Users\carda\Downloads\Data Science Henry DataFt25\PF Henry\data\Google Maps\output"

# Función para enviar notificaciones a Slack
def send_slack_notification(message):
    client = WebClient(token="YOUR_SLACK_BOT_TOKEN")
    try:
        response = client.chat_postMessage(channel="#etl-notifications", text=message)
        print("Notificación enviada:", response["message"]["text"])
    except SlackApiError as e:
        print(f"Error al enviar mensaje a Slack: {e.response['error']}")

# Función para extraer datos
def extract_data(**kwargs):
    processed_files = [os.path.join(processed_folder, f) for f in os.listdir(processed_folder) if f.endswith('.csv')]
    dataframes = []
    for file_path in processed_files:
        df = pd.read_csv(file_path)
        dataframes.append(df)
    combined_df = pd.concat(dataframes, ignore_index=True)
    kwargs['ti'].xcom_push(key='extracted_data', value=combined_df.to_json())  # Pasar datos como JSON

# Función para transformar datos
def transform_data(**kwargs):
    extracted_data = kwargs['ti'].xcom_pull(key='extracted_data')
    df = pd.read_json(extracted_data)
    df.dropna(inplace=True)
    if 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'], errors='coerce')
    kwargs['ti'].xcom_push(key='transformed_data', value=df.to_json())

# Función para cargar datos
def load_data(**kwargs):
    transformed_data = kwargs['ti'].xcom_pull(key='transformed_data')
    df = pd.read_json(transformed_data)
    table_name = "business_data"
    existing_data = pd.read_sql(f"SELECT * FROM {table_name}", con=engine) if engine.dialect.has_table(engine, table_name) else pd.DataFrame()
    new_data = df[~df['gmap_id'].isin(existing_data['gmap_id'])] if not existing_data.empty else df
    if not new_data.empty:
        new_data.to_sql(table_name, con=engine, if_exists='append', index=False)
        send_slack_notification(f"{len(new_data)} registros nuevos cargados.")
    else:
        send_slack_notification("No hay datos nuevos para cargar.")

# Configuración del DAG
default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2025, 1, 21),
}

with DAG(
    dag_id="etl_pipeline",
    default_args=default_args,
    schedule="0 * * * *",  # Cada hora
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data,
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
    )

    load_task = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
    )

    extract_task >> transform_task >> load_task