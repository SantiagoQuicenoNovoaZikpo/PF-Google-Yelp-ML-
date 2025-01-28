def process_all_files(event, context):
    from google.cloud import storage
    import os
    import pandas as pd

    # Configuración del cliente de almacenamiento
    client = storage.Client()
    bucket_name = os.environ["BUCKET_NAME"]
    bucket = client.get_bucket(bucket_name)

    # Información del archivo subido
    file_name = event["name"]
    input_blob = bucket.blob(file_name)

    # Verifica si el archivo es un JSON
    if file_name.endswith(".json"):
        print(f"Procesando archivo: {file_name}")
        local_path = f"/tmp/{file_name.split('/')[-1]}"

        # Descarga el archivo al sistema local (temporal)
        input_blob.download_to_filename(local_path)

        # Procesar el archivo línea por línea
        output_file = f"processed/sample_{file_name}"
        output_blob = bucket.blob(output_file)

        try:
            with open(local_path, "r") as f:
                processed_data = []
                for line in f:
                    # Convierte cada línea a un dict
                    data = pd.read_json(line, lines=True)
                    # Realiza algún procesamiento (ejemplo: tomar solo las 10 primeras líneas)
                    processed_data.append(data)

                # Guarda los datos procesados en la nube
                pd.concat(processed_data).to_json(local_path, orient="records", lines=True)
                output_blob.upload_from_filename(local_path)
                print(f"Archivo procesado guardado en: {output_file}")
        except Exception as e:
            print(f"Error al procesar el archivo: {e}")
