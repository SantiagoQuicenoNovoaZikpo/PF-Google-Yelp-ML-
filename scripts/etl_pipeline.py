import pandas as pd
import os

# Función para extraer datos
def extract_data(processed_folder, **kwargs):
    processed_files = [os.path.join(processed_folder, f) for f in os.listdir(processed_folder) if f.endswith('.json')]
    dataframes = []
    for file_path in processed_files:
        df = pd.read_json(file_path, lines=True)
        if len(df) > 100:
            df = df.sample(n=100, random_state=42)
        dataframes.append(df)
    combined_df = pd.concat(dataframes, ignore_index=True)
    kwargs['ti'].xcom_push(key='extracted_data', value=combined_df.to_json())

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
    output_file = "/opt/airflow/data/processed/loaded_data.json"
    df.to_json(output_file, orient='records', lines=True)
    print(f"Datos cargados en {output_file}")
