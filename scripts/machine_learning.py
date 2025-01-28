from google.cloud import bigquery
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np

# Configuración de cliente BigQuery
client = bigquery.Client()

# Cargar datos desde BigQuery
def load_data():
    query = """
    SELECT
        name,
        category,
        avg_rating,
        num_of_reviews,
        state,
        population
    FROM
        `instant-binder-447716-p6.yelp_google_data.processed_table`
    """
    df = client.query(query).to_dataframe()
    return df

# Preprocesar los datos
def preprocess_data(df):
    # Llenar valores nulos y codificar texto
    df['category'] = df['category'].astype('category').cat.codes
    df.fillna(0, inplace=True)
    return df

# Crear modelo K-Means
def train_model(df, n_clusters=5):
    features = df[['avg_rating', 'num_of_reviews', 'category']]
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(features)
    return df, kmeans

# Obtener recomendaciones
def recommend(df, business_name):
    # Encontrar el cluster del negocio dado
    cluster = df[df['name'] == business_name]['cluster'].values[0]
    # Filtrar negocios en el mismo cluster
    recommendations = df[df['cluster'] == cluster].sort_values(by='avg_rating', ascending=False)
    return recommendations[['name', 'category', 'avg_rating']].head(5)

# Ejecución principal
if __name__ == "__main__":
    # Cargar datos desde BigQuery
    print("Cargando datos desde BigQuery...")
    df = load_data()

    # Preprocesar datos
    print("Preprocesando datos...")
    df = preprocess_data(df)

    # Entrenar modelo
    print("Entrenando modelo K-Means...")
    df, model = train_model(df, n_clusters=5)

    # Ejemplo de recomendación
    business_name = "Ejemplo Business Name"  # Cambia esto por un negocio existente en los datos
    print(f"Recomendaciones para '{business_name}':")
    recommendations = recommend(df, business_name)
    print(recommendations)
