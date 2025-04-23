# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 21:37:45 2025

@author: goess
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Cargar archivo .env desde la ruta absoluta (más seguro)
load_dotenv(dotenv_path=".env")

# Obtener la clave
api_key = os.getenv("OPENAI_API_KEY")
print("API KEY:", api_key)  # Solo para pruebas, debería imprimir la clave

# Si está funcionando, puedes seguir con la llamada a OpenAI
if api_key:
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hola, ¿qué sabes hacer?"}]
    )

    print(response.choices[0].message.content)
else:
    print("❌ No se cargó la API key. Revisa el archivo .env.")
