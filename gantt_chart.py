import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Task details for Gantt chart with inverted activities
tasks = [
    {"Task": "Presentación Final y Entrega del Proyecto (Todo el equipo)", "Start": "2025-01-31", "End": "2025-01-31"},
    {"Task": "Preparación de la Demo 3 y revisión final (Todo el equipo)", "Start": "2025-01-29", "End": "2025-01-30"},
    {"Task": "Modelo de Machine Learning (Santiago)", "Start": "2025-01-26", "End": "2025-01-28"},
    {"Task": "Desarrollo de visualizaciones iniciales (Alfredo)", "Start": "2025-01-25", "End": "2025-01-27"},
    {"Task": "Preparación de la Demo 2 (Todo el equipo)", "Start": "2025-01-23", "End": "2025-01-24"},
    {"Task": "Modelo de datos y diseño ER (Jhon)", "Start": "2025-01-21", "End": "2025-01-23"},
    {"Task": "ETL inicial y validación (Santiago)", "Start": "2025-01-18", "End": "2025-01-23"},
    {"Task": "Preparación de la Demo 1 (Todo el equipo)", "Start": "2025-01-16", "End": "2025-01-17"},
    {"Task": "Selección de stack tecnológico (Jhon)", "Start": "2025-01-16", "End": "2025-01-17"},
    {"Task": "Creación del repositorio GitHub (Santiago)", "Start": "2025-01-15", "End": "2025-01-15"},
    {"Task": "Exploración de datos (EDA) (Alfredo)", "Start": "2025-01-16", "End": "2025-01-19"},
    {"Task": "Definición de objetivos y KPIs (Todo el equipo)", "Start": "2025-01-15", "End": "2025-01-15"},
    {"Task": "Análisis inicial de la temática y datos (Todo el equipo)", "Start": "2025-01-13", "End": "2025-01-14"}
]

# Prepare data for Gantt chart
task_names = [task['Task'] for task in tasks]
start_dates = [datetime.strptime(task['Start'], '%Y-%m-%d') for task in tasks]
end_dates = [datetime.strptime(task['End'], '%Y-%m-%d') for task in tasks]
durations = [(end - start).days + 1 for start, end in zip(start_dates, end_dates)]

# Create Gantt chart
fig, ax = plt.subplots(figsize=(12, 6))

for i, (task, start, duration) in enumerate(zip(task_names, start_dates, durations)):
    ax.barh(i, duration, left=start, color='skyblue', edgecolor='black')

# Customize chart
ax.set_yticks(range(len(task_names)))
ax.set_yticklabels(task_names)
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
plt.xticks(rotation=45)
plt.xlabel('Fecha')
plt.ylabel('Tareas')
plt.title('Cronograma de Actividades')
plt.tight_layout()

# Save the chart as an image
plt.savefig("diagrama_gantt.png")
print("Diagrama guardado como 'diagrama_gantt.png'.")

# Show the chart
plt.show()
