Antes de ejecutar el comando:
Docker-compose up --build

Hay que instalar:
pip install mysql-connector-python


En Postman se ejecuta como un Post:
http://localhost:8001/sumar

Y en la opción raw se pasan los datos:
{
"a":15,
"b":17
}

Y el resultado en json es 32.