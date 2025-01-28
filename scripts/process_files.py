from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import pandas as pd

def process_10_random_lines_json(**kwargs):
    os.makedirs(output_folder, exist_ok=True)
    print(f"Revisando archivos en: {input_folder}")
    for root, _, files in os.walk(input_folder):
        print(f"Explorando carpeta: {root}")
        for file_name in files:
            print(f"Archivo encontrado: {file_name}")
            if file_name.endswith(".json"):
                input_file_path = os.path.join(root, file_name)
                print(f"Procesando archivo: {input_file_path}")
                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                os.makedirs(output_subfolder, exist_ok=True)
                output_file_path = os.path.join(output_subfolder, f"sample_{file_name}")
                try:
                    df = pd.read_json(input_file_path, lines=True)
                    print(f"Archivo leído correctamente: {input_file_path}")
                    df_sample = df.sample(n=min(10, len(df)), random_state=42)
                    df_sample.to_json(output_file_path, orient="records", lines=True)
                    print(f"Archivo procesado y guardado en: {output_file_path}")
                except Exception as e:
                    print(f"Error procesando {file_name}: {e}")
    print("Procesamiento completado.")
