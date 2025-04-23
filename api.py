# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 12:25:13 2025

@author: rportatil114
"""
%reset -f
#laapi
import os
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI
import sys

sys.path.append(r"C:\Users\rportatil114\Desktop\REPOSITORIO_DATA_SCIENCE\PROYECTO")
from proyectoguapo import obtener_reseñas

# Cargar variables del entorno
os.chdir(r"C:\Users\rportatil114\Desktop\REPOSITORIO_DATA_SCIENCE\PROYECTO")
load_dotenv(dotenv_path=".env")
api_key = os.getenv("OPENAI_API_KEY")

# Obtener las reseñas
reseñas = obtener_reseñas()

# Crear una conexión a la base de datos SQLite en la ruta deseada
db_path = r"C:\Users\rportatil114\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\SQLite ODBC Driver for Win64\Shells"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crear tabla con tipo DECIMAL explícito
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ReseñasAnalizadas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texto TEXT,
        puntuacion DECIMAL(3,2)
    )
''')

if api_key:
    client = OpenAI(api_key=api_key)

    reseñas_prompt = "\n".join(reseñas)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": f"""Eres un analista de sentimientos experto en evaluar reseñas de usuarios considerando tres elementos: el texto de la reseña, la fecha en que fue escrita y la puntuación en estrellas (de 1 a 5).

Tu tarea es asignar a cada reseña una puntuación emocional entre -1 (muy negativa) y 1 (muy positiva), teniendo en cuenta matices, contexto, antigüedad del comentario y su coherencia con las estrellas asignadas por el usuario.

Solo debes devolver la puntuación emocional numérica de cada reseña, una por línea, sin texto adicional ni explicaciones. 

Lista de reseñas a analizar (una por línea con formato "Texto. Estrellas: X. Fecha: hace x años/meses/dias"):
    {reseñas_prompt}
"""
        }]
    )

    resultados = response.choices[0].message.content.splitlines()

    # Asegurar que haya misma cantidad de reseñas y puntuaciones
    min_length = min(len(reseñas), len(resultados))

    for i in range(min_length):
        try:
            puntuacion = resultados[i].strip()
            puntuacion_float = round(float(puntuacion), 2)
            puntuacion_float = max(-1.0, min(1.0, puntuacion_float))
            puntuacion_str = f"{puntuacion_float:.2f}"

            cursor.execute(
                "INSERT INTO ReseñasAnalizadas (texto, puntuacion) VALUES (?, ?)",
                (reseñas[i], puntuacion_str)
            )

            print(f"✅ Reseña procesada correctamente:")
            print(f"Texto: {reseñas[i]}")
            print(f"Puntuación: {puntuacion_str}")

        except ValueError as e:
            print(f"❌ Error en formato: {resultados[i]} - {str(e)}")
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")

    conn.commit()
    conn.close()

else:
    print("❌ No se cargó la API key. Revisa el archivo .env.")
