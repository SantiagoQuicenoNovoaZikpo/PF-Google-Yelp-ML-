import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Función para dibujar tablas
def draw_table(ax, name, x, y, columns, width=2, height_per_column=0.5):
    # Dibujar el rectángulo de la tabla
    height = len(columns) * height_per_column
    table = FancyBboxPatch((x, y - height), width, height, boxstyle="round,pad=0.1", ec="black", fc="lightyellow", zorder=3)
    ax.add_patch(table)

    # Agregar el título de la tabla
    ax.text(x + width / 2, y, name, ha="center", va="bottom", fontsize=10, fontweight="bold", zorder=4)

    # Agregar columnas
    for i, col in enumerate(columns):
        ax.text(x + 0.1, y - (i + 1) * height_per_column + 0.25, col, ha="left", va="center", fontsize=8, zorder=4)

# Coordenadas de las tablas
tables = {
    "restaurants": {"x": 0, "y": 0, "columns": ["restaurant_id", "name", "category_id", "location_id", "avg_rating", "num_of_reviews", "price_level"]},
    "categories": {"x": -5, "y": 3, "columns": ["category_id", "name", "description"]},
    "locations": {"x": 5, "y": 3, "columns": ["location_id", "state", "city", "population", "total_restaurants"]},
    "reviews": {"x": -5, "y": -4, "columns": ["review_id", "restaurant_id", "user_id", "rating", "review_text", "created_at"]},
    "kpis": {"x": 5, "y": -4, "columns": ["kpi_id", "location_id", "dissatisfied_ratio", "category_demand", "restaurants_per_population", "calculated_at"]},
}

# Relaciones entre tablas
relationships = [
    ("restaurants", "categories"),
    ("restaurants", "locations"),
    ("restaurants", "reviews"),
    ("locations", "kpis"),
]

# Crear la figura
fig, ax = plt.subplots(figsize=(12, 8))

# Dibujar las tablas
for table, info in tables.items():
    draw_table(ax, table, info["x"], info["y"], info["columns"])

# Dibujar las relaciones
for start, end in relationships:
    start_x, start_y = tables[start]["x"] + 1, tables[start]["y"] - len(tables[start]["columns"]) * 0.5
    end_x, end_y = tables[end]["x"] + 1, tables[end]["y"] - len(tables[end]["columns"]) * 0.5
    ax.annotate("", xy=(end_x, end_y), xytext=(start_x, start_y),
                arrowprops=dict(arrowstyle="->", color="black"), zorder=2)

# Configuración del gráfico
ax.set_xlim(-7, 7)
ax.set_ylim(-6, 6)
ax.axis("off")
plt.title("Modelo Entidad-Relación (Estrella)", fontsize=14, fontweight="bold")
plt.show()
