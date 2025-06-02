from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import mysql.connector
import os

app = FastAPI()

class Input(BaseModel):
    a: float
    b: float
    c: float
    d: float

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        user=os.getenv("MYSQL_USER", "root"),
        # password=os.getenv("MYSQL_PASSWORD", "MySQL1969$"),
        database=os.getenv("MYSQL_DATABASE", "ecuaciones_db")
    )

@app.post("/resolver")
def resolver(valores: Input):
    # 1. Llamadas a los otros microservicios
    suma_resp = requests.post("http://suma:8000/sumar", json={"a": valores.a, "b": valores.b})
    resta_resp = requests.post("http://resta:8000/restar", json={"c": valores.c, "d": valores.d})

    if suma_resp.status_code != 200 or resta_resp.status_code != 200:
        raise HTTPException(status_code=502, detail="Error al comunicarse con suma/resta")

    suma = suma_resp.json()["resultado"]
    resta = resta_resp.json()["resultado"]
    resultado = suma * resta

    # 2. Persistir en MySQL
    try:
    	db = get_db_connection()
    	cursor = db.cursor()
    	cursor.execute("""
        INSERT INTO resultados (a, b, c, d, resultado)
        VALUES (%s, %s, %s, %s, %s)
    """, (valores.a, valores.b, valores.c, valores.d, resultado))
    	db.commit()

    except mysql.connector.Error as err:
    	raise HTTPException(status_code=500, detail=f"Error en base de datos: {err}")
    finally:
    if 'cursor' in locals():
        cursor.close()
    if 'db' in locals() and db.is_connected():
        db.close()

    return {"resultado": resultado}