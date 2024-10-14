# app.py

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
        # Crear un DataFrame a partir de los datos obtenidos
        df = pd.DataFrame(datos)

        # Mostrar los datos de los partidos
        for index, row in df.iterrows():
            home_team = row['home_team']
            away_team = row['away_team']
            bookmakers = row['bookmakers']

            # Acceder al primer bookmaker (casa de apuestas)
            if len(bookmakers) > 0:
                markets = bookmakers[0]['markets']  # Extraer los mercados de apuestas

                # Head-to-head (h2h): equipo 1 gana, empate, equipo 2 gana
                if markets[0]['key'] == 'h2h':
                    outcomes = markets[0]['outcomes']

                    # Extraemos las probabilidades de ganador, empate y perdedor
                    cuotas_equipo1 = outcomes[0]['price']  # Cuota del equipo 1
                    cuotas_empate = outcomes[1]['price']  # Cuota del empate
                    cuotas_equipo2 = outcomes[2]['price']  # Cuota del equipo 2

                    # Calcular las probabilidades implícitas
                    prob_equipo1 = 1 / cuotas_equipo1 * 100
                    prob_empate = 1 / cuotas_empate * 100
                    prob_equipo2 = 1 / cuotas_equipo2 * 100

                    # Mostrar los resultados en la aplicación Streamlit
                    st.subheader(f"Partido: {home_team} vs {away_team}")
                    st.write(f"Probabilidad de ganar {home_team}: {prob_equipo1:.2f}%")
                    st.write(f"Probabilidad de Empate: {prob_empate:.2f}%")
                    st.write(f"Probabilidad de ganar {away_team}: {prob_equipo2:.2f}%")

                # Totales (goles over/under)
                if markets[1]['key'] == 'totals':
                    totals = markets[1]['outcomes']

                    # Extraemos las probabilidades del over/under de goles
                    total_goles_over = totals[0]['price']  # Cuota de más de X goles
                    total_goles_under = totals[1]['price']  # Cuota de menos de X goles

                    # Mostrar las probabilidades de goles en la aplicación
                    st.write(f"Probabilidad de que haya más de {totals[0]['name']} goles: {total_goles_over * 100:.2f}%")
                    st.write(f"Probabilidad de que haya menos de {totals[1]['name']} goles: {total_goles_under * 100:.2f}%")
            else:
                st.write("No hay datos disponibles para los bookmakers.")
    else:
        st.write("No hay datos de partidos disponibles.")
