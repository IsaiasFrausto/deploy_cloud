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
    # Conexión a MySQL en este caso para Railway
    conexion = mysql.connector.connect(
        host=os.getenv("MYSQLHOST", "mysql.railway.internal"),
        user=os.getenv("MYSQLUSER", "root"),
        password=os.getenv("MYSQLPASSWORD", "OspIzOrOktOwkIRvstyvUxKgxYAtPbBj"),
        database=os.getenv("MYSQL_DATABASE", "railway")
    )

    print("-- En Almacenar --")
    print("HOST:", os.getenv("MYSQLHOST"))
    print("USER:", os.getenv("MYSQLUSER"))
    print("PWD :", os.getenv("MYSQLPASSWORD"))
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
