import pandas as pd
import matplotlib.pyplot as plt
import os

#/////////////////////////////////////////////////CARGA DE DATOS/////////////////////////////////////////////////////////////////////////////////

#Cargamos el CSV
csv_path = "open-meteo-52.52N13.42E38m.csv"

df = pd.read_csv(csv_path)

# Normalizar nombres de columnas (según dataset open-meteo)
df = df.rename(columns={
    "time": "Fecha",
    "temperature_2m_min": "Temperatura Mínima",
    "temperature_2m_max": "Temperatura Máxima"
})

#Convertimos la fecha
df["Fecha"] = pd.to_datetime(df["Fecha"])

#/////////////////////////////////////////////ANALISIS BASICO DE DATOS//////////////////////////////////////////////////////////////////////////////////////////////

#Temperatura Media
df["Temperatura_Media"] = (df["Temperatura Mínima"] + df["Temperatura Máxima"]) / 2
df["Mes"] = df["Fecha"].dt.to_period("M")

#Promedios mensuales
promedios_mensuales = df.groupby("Mes")[["Temperatura Mínima","Temperatura Máxima","Temperatura_Media"]].mean()

#Dias extremos
umbral_calor, umbral_frio = 35, 0
dias_extremos = df[(df["Temperatura Máxima"] > umbral_calor) | (df["Temperatura Mínima"] < umbral_frio)]

#Mes mas caluroso y frío
mes_caluroso = promedios_mensuales["Temperatura_Media"].idxmax()
mes_frio = promedios_mensuales["Temperatura_Media"].idxmin

#//////////////////////////////////////////////VISUALIZACION DE DATOS/////////////////////////////////////////////////////////////////////////////////////////////////////////////////

os.makedirs("resultados", exist_ok=True)

#Evolucion de Temperatura Diaria (Grafico)
plt.figure(figsize=(12,6))
plt.plot(df["Fecha"], df["Temperatura_Media"], label="Temperatura Media")
plt.xlabel("Fecha")
plt.ylabel("Temperatura (°C)")
plt.title("Evolución diaria de la temperatura")
plt.legend()
plt.savefig("resultados/evolucion_diaria.png")
plt.show()
plt.close()

#Promedio mensuales de Temperaturas (Grafico)
promedios_mensuales["Temperatura_Media"].plot(kind="bar", figsize=(12,6))
plt.title("Promedio mensual de temperatura")
plt.ylabel("Temperatura (°C)")
plt.savefig("resultados/promedio_mensual.png")
plt.show()
plt.close()

#Informe HTML
with open("resultados/informe.html", "w", encoding="utf-8") as f:
    f.write("<h1>Análisis Climático</h1>")
    f.write("<h2>Mes más caluroso y más frío</h2>")
    f.write(f"<p>Mes más caluroso: {mes_caluroso} ({promedios_mensuales.loc[mes_caluroso,'Temp_Media']:.2f} °C)</p>")
    f.write(f"<p>Mes más frío: {mes_frio} ({promedios_mensuales.loc[mes_frio,'Temp_Media']:.2f} °C)</p>")
    
    f.write("<h2>Promedios Mensuales</h2>")
    f.write(promedios_mensuales.to_html())

    f.write("<h2>Días Extremos</h2>")
    f.write(dias_extremos.to_html(index=False))

    f.write("<h2>Gráficos</h2>")
    f.write('<img src="evolucion_diaria.png" width="600"><br>')
    f.write('<img src="promedio_mensual.png" width="600">')
