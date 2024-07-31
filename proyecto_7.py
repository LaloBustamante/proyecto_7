#Importar bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats


#Importar archivos CSV 
# Importar los datasets
df_companies = pd.read_csv('/datasets/project_sql_result_01.csv')
df_neighborhoods = pd.read_csv('/datasets/project_sql_result_04.csv')
df_weather = pd.read_csv('/datasets/project_sql_result_07.csv')

# Mostrar las primeras filas de los datasets
print(df_companies.head())
print(df_neighborhoods.head())
print(df_weather.head())


#Estudiar los Datos
# Información de los datasets
print(df_companies.info())
print(df_neighborhoods.info())
print(df_weather.info())

# Descripción estadística de los datasets
print(df_companies.describe())
print(df_neighborhoods.describe())
print(df_weather.describe())


#Asegurarse de que los Tipos de Datos sean Correctos
# Asegurarse de que los tipos de datos sean correctos
df_companies['trips_amount'] = df_companies['trips_amount'].astype(int)
df_neighborhoods['average_trips'] = df_neighborhoods['average_trips'].astype(float)
# Convertir 'start_ts' a datetime
df_weather['start_ts'] = pd.to_datetime(df_weather['start_ts'])

#Identificar los 10 Principales Barrios en Términos de Finalización del Recorrido
# Identificar los 10 principales barrios
top_10_neighborhoods = df_neighborhoods.nlargest(10, 'average_trips')
print(top_10_neighborhoods)

# Filtrar los sábados
df_weather['day_of_week'] = df_weather['start_ts'].dt.day_name()
saturdays = df_weather[df_weather['day_of_week'] == 'Saturday']

#Hacer Gráficos
# Gráfico de Empresas de Taxis y Número de Viajes
plt.figure(figsize=(10, 6))
plt.bar(df_companies['company_name'], df_companies['trips_amount'])
plt.xlabel('Empresa de Taxis')
plt.ylabel('Número de Viajes')
plt.title('Número de Viajes por Empresa de Taxis (15 y 16 de Noviembre de 2017)')
plt.xticks(rotation=90)
plt.show()

# Gráfico de los 10 Barrios Principales por Número de Finalizaciones
plt.figure(figsize=(10, 6))
plt.bar(top_10_neighborhoods['dropoff_location_name'], top_10_neighborhoods['average_trips'])
plt.xlabel('Barrio')
plt.ylabel('Promedio de Viajes')
plt.title('Top 10 Barrios por Promedio de Finalizaciones de Viajes (Noviembre de 2017)')
plt.xticks(rotation=90)
plt.show()

# Filtrar los días lluviosos y no lluviosos
rainy_saturdays = saturdays[saturdays['weather_conditions'].str.contains('Rain')]
non_rainy_saturdays = saturdays[~saturdays['weather_conditions'].str.contains('Rain')]

# Duraciones de viajes en segundos
rainy_durations = rainy_saturdays['duration_seconds']
non_rainy_durations = non_rainy_saturdays['duration_seconds']

# Prueba t de dos muestras
t_stat, p_value = stats.ttest_ind(rainy_durations, non_rainy_durations, equal_var=False)

print(f'T-statistic: {t_stat}')
print(f'P-value: {p_value}')


#Sacar Conclusiones Basadas en Cada Gráfico y Explicar los Resultados
# Conclusiones basadas en los gráficos

# Conclusión del gráfico de empresas de taxis y número de viajes
print("Conclusión del Gráfico 1:")
print("La empresa de taxis con mayor cantidad de viajes el 15 y 16 de noviembre de 2017 es 'Flash Cab', seguida de 'Taxi Affiliation Services'. Las empresas con menos viajes son las que tienen nombres menos reconocidos.")

# Conclusión del gráfico de los 10 barrios principales por número de finalizaciones
print("Conclusión del Gráfico 2:")
print("El barrio con el mayor promedio de finalizaciones de viajes en noviembre de 2017 es 'Loop',seguido de 'Near North Side' y 'River North'. Estos barrios son conocidos por ser áreas comerciales y turísticas, lo que puede explicar el alto número de finalizaciones de viajes.")

#Interpretar los resultados
alpha = 0.05
if p_value < alpha:
    print("Rechazamos la hipótesis nula. La duración promedio de los viajes cambia los sábados lluviosos.")
else:
    print("No podemos rechazar la hipótesis nula. No hay suficiente evidencia para afirmar que la duración promedio de los viajes cambia los sábados lluviosos.")