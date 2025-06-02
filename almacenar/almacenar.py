from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import os  # ✅ IMPORTANTE

app = FastAPI()

class ResultadoRequest(BaseModel):
    a: float
    b: float
    c: float
    d: float
    resultado: float

@app.post("/guardar")
def guardar(datos: ResultadoRequest):
    # Conexión a MySQL
    conexion = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        user=os.getenv("MYSQL_USER", "myuser"),
        password=os.getenv("MYSQL_PASSWORD", "mypassword123"),
        database=os.getenv("MYSQL_DATABASE", "resultados_db")
    )

    print("-- En Almacenar --")
    print("HOST:", os.getenv("MYSQL_HOST"))
    print("USER:", os.getenv("MYSQL_USER"))
    print("PWD :", os.getenv("MYSQL_PASSWORD"))
    print("DB  :", os.getenv("MYSQL_DATABASE"))

    cursor = conexion.cursor()

    # Insertar datos
    query = "INSERT INTO resultados (a, b, c, d, resultado) VALUES (%s, %s, %s, %s, %s)"
    valores = (datos.a, datos.b, datos.c, datos.d, datos.resultado)
    cursor.execute(query, valores)
    conexion.commit()

    cursor.close()
    conexion.close()

    return {"mensaje": "Resultado almacenado correctamente"}
