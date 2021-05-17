# Prueba técnica para Aimo.co

Para cumplir con todas las funcionalidades requeridas tome la decisión
de empezar con un modelo entidad relacion donde un Usuario esta relacionado
con una Nota y también un Usuario se relacion con un token.
![Modelo](https://raw.githubusercontent.com/NicolasRondon/test_aimo/main/entidad-relacion.PNG)
En la funcionalidad de autenticación se solicito usar el paquete JWT para
identificar el usuario, tome la decisión de considerar el **ID** del usuario
como un dato sensible, por lo cual en ningún momento es expuesto en la API,
gracias a la ayuda de mi modelo **UserToken** el cual al momento de hacer 
un login  usa la lbireria interna de python **binascii** para crear un token
aleatorio el cual será la llave para las peticiones en el sistema a su vez,
este token se genera con una fecha de expiración, otro punto a considerar,
es que la contraseña del usuario al momento de registrarse se encripta gracias
a la libreria interna de python  hashlib.


Al momento del desarrollo se hizo uso de distintos patrones de diseño que facilitaron la ejecución del mismo,
entre ellos el patrón, bridge, facade y builder.

## Flujo en Git
Mi flujo de trabajo en git fue de la siguiente manera, por cada funcionalidad a realizar
agregue una rama, cuando el trabajo de esa rama finalizaba se hace merge con la rama develop,
para luego continuar hacia la rama test, ejecutar los test y finalmente migrar a la rama master

![GitFlow](https://raw.githubusercontent.com/NicolasRondon/test_aimo/main/gitflow.PNG)


## Documentacion api

#### http://localhost:8000/api/v1/users
[**POST**] Se crean los usuarios es necesario enviar un json con las llaves: username y passsword
```
{
    "username": "usuario",
    "password": "password"
}
```
#### http://localhost:8000/api/v1/users/login
[**POST**] Este servicio  responde un token con un tiempo de vida de 9 horas, 
es necesario enviar un json con las llaves: username y passsword

#### http://localhost:8000/api/v1/users/refresh
[**POST**]  En caso de que el token ya haya cumplido su tiempo de vida, puedes
usar este servicio el cual retornaun token actualizado, es necesario enviar el
token en el header Authorization
```
{
    "token": "Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MjEyMjMwMzEsInRva2VuIjoiMzdlNTQ5YTliZWE2YjFkODJhOTYwODIzYjRhMzYxNmY4N2I3N2MyZCJ9.SWnFDOksbKAqokdDzRrBO4t1OL9fki8QoZTYCUGXYgU"
}
```

### http://localhost:8000/api/v1/notes
[**POST**] Este servicio se usa para crear notas asociadas a un usuario usando el token de autorización
en el header Authorization, a su ves  es necesario enviar en el body un json con las llaves title, body
```
{
    "title": "Nota de Usuario,
    "body": "Cuerpo de la nota"
}
```

### http://localhost:8000/api/v1/notes
[**GET**] Este servicio lista todas las notas asociadas a un usuario, es necesario enviar el token en
el header Authorization

#Retos
Al momento de realizar el api, me enfrente a diferentes factores, uno fue salir de mi zona del confort
al usar herramientas que no conocia, por lo mismo realizar tests en bottle fue un poco dificil para mi
y seguramente hay mejores soluciones a la que yo decidi usar, de tener que correr el server y luego si 
ejecutar los test, otro reto  es la integración del back con el front debido a mi falta de practica 
en tecnologías javascript y el desconocimiento de la herramienta bottle tengo incovenientes en los cors, los cuales me impidieron avanzar.