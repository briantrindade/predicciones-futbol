import streamlit as st
import pandas as pd
import requests

# Reemplaza con tu clave API
api_key = "2580147fe536ec7ebeefaf9564b5fe85"

# Endpoint de probabilidades de fútbol
url = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds/?regions=eu&markets=h2h,totals&apiKey=" + api_key

# Función para obtener datos de la API
def obtener_datos():
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al obtener los datos de la API.")
        return None

# Título de la aplicación
st.title("Predicciones de Fútbol")

# Botón para cargar los datos
if st.button("Cargar Datos"):
    datos = obtener_datos()

    if datos:
        df = pd.DataFrame(datos)

        # Mostrar los datos obtenidos
        st.write(df[['home_team', 'away_team', 'bookmakers']])

        # Mostrar las probabilidades
        for index, row in df.iterrows():
            cuotas_equipo1 = row['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
            cuotas_equipo2 = row['bookmakers'][0]['markets'][0]['outcomes'][1]['price']

            prob_equipo1 = 1 / cuotas_equipo1 * 100
            prob_equipo2 = 1 / cuotas_equipo2 * 100

            st.write(f"Probabilidad de ganar {row['home_team']}: {prob_equipo1:.2f}%")
            st.write(f"Probabilidad de ganar {row['away_team']}: {prob_equipo2:.2f}%")
