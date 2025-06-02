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

#def get_db_connection():
#    return mysql.connector.connect(
#        host="mysql",
#        user="myuser",
#        password="mypassword123",
#        database="resultados_db",
#    )


def get_db_connection():
 
   return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        user=os.getenv("MYSQL_USER", "myuser"),
        password=os.getenv("MYSQL_PASSWORD", "mypassword123"),
        database=os.getenv("MYSQL_DATABASE", "resultados_db")
    )



@app.post("/resolver")
def resolver(valores: Input):
    print("Entra a resolver")
    try:
        suma_resp = requests.post("http://suma:8000/sumar", json={"a": valores.a, "b": valores.b}, timeout=5)
        suma_resp.raise_for_status()
        resta_resp = requests.post("http://resta:8000/restar", json={"c": valores.c, "d": valores.d}, timeout=5)
        resta_resp.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error al comunicarse con suma/resta: {e}")

    print("Entra a segundo try")
    try:
        suma = suma_resp.json().get("resultado")
        resta = resta_resp.json().get("resultado")
        if suma is None or resta is None:
            raise HTTPException(status_code=502, detail="Respuesta inválida de suma/resta")
    except Exception:
        raise HTTPException(status_code=502, detail="Error procesando la respuesta JSON de suma/resta")

    resultado = suma * resta
    print ("resultado -->", resultado)
    try:
        db = get_db_connection()

        host=os.getenv("MYSQL_HOST", "mysql"),
        user=os.getenv("MYSQL_USER", "myuser"),
        password=os.getenv("MYSQL_PASSWORD", "mypassword123"),
        database=os.getenv("MYSQL_DATABASE", "resultados_db")

        print("HOST:", host)
        print("USER:", user)
        print("PASS :", password)
        print("DB  :", database)

        cursor = db.cursor()

        query = "INSERT INTO resultados (a, b, c, d, resultado) VALUES (%s, %s, %s, %s, %s)"
        valores = (valores.a, valores.b, valores.c, valores.d, resultado)
        cursor.execute(query, valores)
        db.commit()    

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error en base de datos: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals() and db.is_connected():
            db.close()

    return {"resultado": resultado}


@app.get("/historial")
def historial():
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)
        
        query = "SELECT * FROM resultados ORDER BY id DESC LIMIT 10"
        cursor.execute(query)
        
        resultados = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        
        return {"historial": resultados}
    except Exception as e:
        return {"error": f"Error al obtener el historial: {str(e)}"}
