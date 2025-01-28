import os
import pandas as pd
from google.cloud import storage

def process_json_file(data, context):
    """Procesa archivos JSON al ser subidos al bucket."""
    client = storage.Client()
    bucket_name = os.environ['BUCKET_NAME']  # Bucket donde se almacenan los archivos
    processed_folder = "processed/"  # Carpeta de salida en el bucket

    # Obtener detalles del archivo subido
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(data['name'])

    # Descargar y procesar el archivo JSON
    try:
        content = blob.download_as_text()
        df = pd.read_json(content, lines=True)

        # Tomar una muestra de 10 filas
        df_sample = df.sample(n=min(10, len(df)), random_state=42)

        # Guardar el archivo procesado en el bucket
        output_blob = bucket.blob(processed_folder + f"sample_{data['name']}")
        output_blob.upload_from_string(df_sample.to_json(orient="records", lines=True))
        print(f"Archivo procesado y guardado: {processed_folder}sample_{data['name']}")
    except Exception as e:
        print(f"Error procesando el archivo: {e}")
