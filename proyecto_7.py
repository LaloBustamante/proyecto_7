'''
# Descripción del proyecto

Estás trabajando como analista para Zuber, una nueva empresa de viajes compartidos que se está lanzando en Chicago. Tu tarea es encontrar patrones en la información disponible. Quieres comprender las preferencias de los pasajeros y el impacto de los factores externos en los viajes.

Al trabajar con una base de datos, analizarás los datos de los competidores y probarás una hipótesis sobre el impacto del clima en la frecuencia de los viajes.

Instrucciones para completar el proyecto
Paso 1. Escribe un código para analizar los datos sobre el clima en Chicago en noviembre de 2017 desde el sitio web:

https://practicum-content.s3.us-west-1.amazonaws.com/data-analyst-eng/moved_chicago_weather_2017.html

Paso 2. Análisis exploratorio de datos

Encuentra el número de viajes en taxi para cada empresa de taxis del 15 al 16 de noviembre de 2017. Nombra el campo resultante trips_amount y muéstralo junto con el campo company_name. Ordena los resultados por el campo trips_amount en orden descendente.

Encuentra la cantidad de viajes para cada empresa de taxis cuyo nombre contenga las palabras "Yellow" o "Blue" del 1 al 7 de noviembre de 2017. Nombra la variable resultante trips_amount. Agrupa los resultados por el campo company_name.

En noviembre de 2017 las empresas de taxis más populares fueron Flash Cab y Taxi Affiliation Services. Encuentra el número de viajes de estas dos empresas y asigna a la variable resultante el nombre trips_amount. Junta los viajes de todas las demás empresas en el grupo "Other". Agrupa los datos por nombres de empresas de taxis. Nombra el campo con nombres de empresas de taxis company. Ordena el resultado en orden descendente por trips_amount.

Paso 3. Prueba la hipótesis de que la duración de los viajes desde el Loop hasta el Aeropuerto Internacional O'Hare cambia los sábados lluviosos.

Recupera los identificadores de los barrios de O'Hare y Loop de la tabla neighborhoods.

Para cada hora recupera los registros de condiciones meteorológicas de la tabla weather_records. Usando el operador CASE, divide todas las horas en dos grupos: "Bad" si el campo description contiene las palabras "rain" o "storm" y "Good" para los demás. Nombra el campo resultante weather_conditions. La tabla final debe incluir dos campos: fecha y hora (ts) y weather_conditions.

Recupera de la tabla trips todos los viajes que comenzaron en el Loop (neighborhood_id: 50) y finalizaron en O'Hare (neighborhood_id: 63) un sábado. Obtén las condiciones climáticas para cada viaje. Utiliza el método que aplicaste en la tarea anterior. Recupera también la duración de cada viaje.
Ignora los viajes para los que no hay datos disponibles sobre las condiciones climáticas.

Paso 4. Análisis exploratorio de datos (Python)

Además de los datos que recuperaste en las tareas anteriores te han dado un segundo archivo. Ahora tienes estos dos CSV:

project_sql_result_01.csv. Contiene los siguientes datos:

company_name: nombre de la empresa de taxis
trips_amount: el número de viajes de cada compañía de taxis el 15 y 16 de noviembre de 2017.
project_sql_result_04.csv. Contiene los siguientes datos:

dropoff_location_name: barrios de Chicago donde finalizaron los viajes
average_trips: el promedio de viajes que terminaron en cada barrio en noviembre de 2017.
Para estos dos datasets ahora necesitas:

importar los archivos
estudiar los datos que contienen
asegurarte de que los tipos de datos sean correctos
identificar los 10 principales barrios en términos de finalización
hacer gráficos: empresas de taxis y número de viajes, los 10 barrios principales por número de finalizaciones
sacar conclusiones basadas en cada gráfico y explicar los resultados

Paso 5. Prueba de hipótesis (Python)

project_sql_result_07.csv: el resultado de la última consulta. Contiene datos sobre viajes desde el Loop hasta el Aeropuerto Internacional O'Hare. Recuerda, estos son los valores de campo de la tabla:

start_ts: fecha y hora de recogida
weather_conditions: condiciones climáticas en el momento en el que comenzó el viaje
duration_seconds: duración del viaje en segundos
Prueba la hipótesis:
"La duración promedio de los viajes desde el Loop hasta el Aeropuerto Internacional O'Hare cambia los sábados lluviosos".

Establece el valor del nivel de significación (alfa) por tu cuenta.

Explica:

cómo planteaste las hipótesis nula y alternativa
qué criterio usaste para probar las hipótesis y por qué
'''
#Importar bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import tkinter as tk

plt.switch_backend('TkAgg')

#Importar archivos CSV 
# Importar los datasets
df_companies = pd.read_csv('datasets/project_sql_result_01.csv')
df_neighborhoods = pd.read_csv('datasets/project_sql_result_04.csv')
df_weather = pd.read_csv('datasets/project_sql_result_07.csv')

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

'''
# Observaciones Generales:

Variabilidad y Desigualdad:
Hay una clara desigualdad en las distribuciones tanto de los viajes por empresa como de los viajes finalizados por barrio. Esto puede reflejar 
diferencias en el tamaño, la cobertura y la popularidad de las empresas de taxis, así como en la demanda en diferentes áreas de la ciudad.

Calidad de los Datos:
Todos los datasets parecen estar completos, sin valores nulos, lo cual es positivo para el análisis posterior.

Relevancia de las Condiciones Meteorológicas:
El análisis de las condiciones meteorológicas en relación con la duración de los viajes podría ser interesante, aunque será necesario asegurarse 
de que el dataset contenga suficientes variaciones en las condiciones ("Good" vs "Bad") para poder realizar análisis significativos.
'''

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
# Obtener las 10 principales empresas por número de viajes
top_10_companies = df_companies.nlargest(10, 'trips_amount')

# Gráfico de Empresas de Taxis y Número de Viajes
plt.figure(figsize=(10, 6))
plt.bar(top_10_companies['company_name'], top_10_companies['trips_amount'])
plt.xlabel('Empresa de Taxis')
plt.ylabel('Número de Viajes')
plt.title('Top 10 Empresas de Taxis por Número de Viajes (15 y 16 de Noviembre de 2017)')
plt.xticks(rotation=90)
plt.show()

"""
El gráfico de barras muestra la distribución del número de viajes realizados por diferentes empresas 
de taxis durante un periodo específico (15 y 16 de noviembre de 2017). En el eje Y se representa el número de viajes, 
mientras que en el eje X se listan las distintas empresas de taxis.

A partir de este gráfico, podemos extraer las siguientes conclusiones:

Desigualdad en la demanda: Existe una gran disparidad en el número de viajes realizados por cada empresa. Unas pocas empresas 
concentran la mayor parte de los viajes, mientras que otras tienen una demanda significativamente menor.

Dominancia de algunas empresas: Las primeras empresas en el eje X, según el orden de las barras, son las que tienen una mayor 
participación en el mercado de taxis durante el periodo analizado. Estas empresas podrían considerarse como las principales o líderes en 
el sector.

Nicho de mercado: La larga cola de empresas con un número bajo de viajes sugiere la existencia de un mercado bastante fragmentado, con 
muchas empresas pequeñas compitiendo por una porción más reducida del mercado.

Factores que influyen: La diferencia en el número de viajes entre las empresas puede deberse a varios factores, como:

Tamaño de la flota: Las empresas con flotas más grandes suelen tener un mayor número de viajes.
Área de cobertura: Las empresas que operan en zonas con mayor demanda (centros urbanos, áreas turísticas) tienden a tener más viajes.
Reputación y marketing: Las empresas con una mejor reputación y mayor inversión en marketing suelen atraer más clientes.
Tarifas y promociones: Las empresas que ofrecen tarifas más competitivas o promociones especiales pueden tener un mayor número de viajes.
Tecnología: Las empresas que utilizan tecnología avanzada para gestionar sus operaciones (apps, sistemas de pago) pueden ser más 
eficientes y atraer a más clientes.
"""

# Gráfico de los 10 Barrios Principales por Número de Finalizaciones
plt.figure(figsize=(10, 6))
plt.bar(top_10_neighborhoods['dropoff_location_name'], top_10_neighborhoods['average_trips'])
plt.xlabel('Barrio')
plt.ylabel('Promedio de Viajes')
plt.title('Top 10 Barrios por Promedio de Finalizaciones de Viajes (Noviembre de 2017)')
plt.xticks(rotation=90)
plt.show()

"""
El gráfico de barras nos muestra el promedio de viajes finalizados en los 10 barrios con mayor demanda durante el mes de 
noviembre de 2017. En el eje Y se representa el número promedio de viajes, mientras que en el eje X se listan los nombres de los barrios.

A partir de este gráfico, podemos extraer las siguientes conclusiones:

Desigualdad en la Demanda: Existe una clara diferencia en la demanda de servicios de transporte entre los diferentes barrios. 
Los primeros puestos concentran un número significativamente mayor de viajes en comparación con los últimos.

Barrios con Mayor Demanda: Los barrios ubicados en las primeras posiciones del gráfico (Loop, North, Riverville) son los que presentan 
una mayor demanda de servicios de transporte. Esto podría indicar que son zonas con mayor densidad poblacional, mayor actividad comercial, 
o que son centros de atracción para actividades de ocio o trabajo.

Potencial de Mercado: Los barrios con un menor número de viajes (como DePaul) podrían representar una oportunidad de crecimiento para las 
empresas de transporte. Al identificar las razones por las cuales la demanda es menor en estos barrios, se podrían implementar estrategias 
para aumentar el número de viajes.

Factores que Influyen en la Demanda: La variación en la demanda entre los barrios puede estar influenciada por diversos factores, como:

Densidad poblacional: Los barrios más poblados suelen tener una mayor demanda de transporte.
Disponibilidad de transporte público: La presencia de estaciones de metro, autobuses o trenes puede afectar la demanda de servicios de 
transporte privado.
Atractivos turísticos o comerciales: Los barrios con atracciones turísticas o centros comerciales suelen tener una mayor demanda, 
especialmente en ciertas horas del día.
Características urbanísticas: La distribución de viviendas, oficinas y espacios públicos puede influir en los patrones de movilidad.
"""

# Filtrar los días lluviosos y no lluviosos
rainy_saturdays = saturdays[saturdays['weather_conditions'].str.contains('Bad')]
non_rainy_saturdays = saturdays[saturdays['weather_conditions'].str.contains('Good')]

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

"""
Para probar estas hipótesis, utilizamos la prueba t de dos muestras independientes (también conocida como prueba t de Student). Este es un 
método estadístico utilizado para determinar si hay una diferencia significativa entre las medias de dos grupos independientes. Los criterios 
y razones para elegir esta prueba son:

Naturaleza de los Datos: Los datos de la duración del viaje son continuos y aproximadamente distribuidos normalmente.
Se comparan dos grupos independientes: viajes en sábados lluviosos y viajes en sábados no lluviosos.

Prueba de Igualdad de Varianzas: Usamos la versión de la prueba t para varianzas desiguales (Welch's t-test), que es una variación de la 
prueba t estándar que no asume que las dos muestras tienen varianzas iguales. Esto es más robusto cuando las varianzas y los tamaños de 
las muestras son diferentes.

Nivel de Significación (Alpha): Establecimos un nivel de significación α de 0.05. Esto significa que aceptaremos una probabilidad de 5% de rechazar la hipótesis nula 
cuando en realidad sea verdadera (error de tipo I).

Cálculo del Estadístico t y P-Valor: Calculamos el estadístico t, que mide el tamaño de la diferencia relativa a la variabilidad de las 
muestras. También calculamos el p-valor, que nos indica la probabilidad de observar una diferencia tan extrema como la que se observa en 
los datos, bajo la suposición de que la hipótesis nula es verdadera.
"""

