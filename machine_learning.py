import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset combinado
# Asegúrate de que 'combined_df' tenga las columnas: 'state', 'category', 'avg_rating', 'num_of_reviews', 'population'
df = combined_df.copy()

# Eliminar valores nulos
df.dropna(subset=['avg_rating', 'num_of_reviews', 'state', 'category'], inplace=True)

# Identificar los 3 mejores estados con mayor proporción de locales/población
state_analysis = df.groupby('state').agg(
    total_restaurants=('state', 'count'),
    total_reviews=('num_of_reviews', 'sum'),
    avg_rating=('avg_rating', 'mean'),
    population=('population', 'max')  # Supongamos que tienes una columna con población por estado
).reset_index()
state_analysis['restaurants_per_population'] = state_analysis['total_restaurants'] / state_analysis['population']
top_states = state_analysis.nlargest(3, 'restaurants_per_population')['state'].tolist()

# Filtrar los datos para los 3 mejores estados
filtered_df = df[df['state'].isin(top_states)]

# Usar Isolation Forest para detectar outliers en las reseñas
iso = IsolationForest(contamination=0.05, random_state=42)
filtered_df['outlier'] = iso.fit_predict(filtered_df[['num_of_reviews', 'avg_rating']])

# Eliminar outliers
cleaned_df = filtered_df[filtered_df['outlier'] == 1]

# Categorías con alta demanda por estado
high_demand_categories = cleaned_df.groupby(['state', 'category']).size().reset_index(name='count')
top_categories = high_demand_categories.groupby('state').apply(
    lambda x: x.nlargest(5, 'count')
).reset_index(drop=True)

# Gráfica de categorías con alta demanda
plt.figure(figsize=(12, 6))
sns.barplot(data=top_categories, x='category', y='count', hue='state', palette='Set2')
plt.title("Categorías con Alta Demanda en los Mejores Estados", fontsize=16)
plt.xlabel("Categoría", fontsize=12)
plt.ylabel("Demanda", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Guardar datos procesados
cleaned_df.to_csv("processed_data.csv", index=False)
