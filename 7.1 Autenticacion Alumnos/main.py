#Intalamos la libreria de criptografía para encriptar token
#pip install python-jose[cryptography]

#Intalamos libreria que contiene el algoritmo de encriptacion
#pip install passlib[bcrypt]

#Importamos el framework fastapi a nuestro entorno de trabajo
from fastapi import FastAPI, Depends, HTTPException, status, Response
from pydantic import BaseModel

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#Importamos libreria jwt
from jose import jwt, JWTError
#Importamos librería passlib (algoritmo de encriptación)
from passlib.context import CryptContext
#Importamos la librería de fechas para la expiración del token
from datetime import datetime, timedelta

#Importamos la libreria de archivos estáticos
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

#from fastapi.responses import Redirect

#Implementamos algoritmo de haseo para encriptar contraseña
ALGORITHM = "HS256"
#Duración de autenticación (en minutos)
ACCESS_TOKEN_DURATION= 1
#Creamos un secret
SECRET="123456789"

app = FastAPI()

#Autenticación por contraseña para eso:
#Creamos un endpoint llamado "login"
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

#Creamos contexto de encriptcación, para eso importamos la librería passlib
# y elegimos algoritmo de encriptación "bcrypt"
#Utilizamos bcrypt generator para encriptar nuestras contraseñas.
crypt = CryptContext(schemes="bcrypt")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

#Definimos la clase para el usuario de base de datos
#Aquí estamos herendando de la clase "User"
class UserDB(User):
    password: str
#La razón de crear esta segunda clase que hereda de User es porque
#al comparar la contraseña usamos la clase que contiene la contraseña "UserDB"
#Pero al devolver los datos devolvemos desde la clase "User", la cual no contiene la contraseña


#Creamos una base de datos de usuarios
users_db= {
    "David":{
        "username": "David",
        "full_name": "David Blas Bravo",
        "email": "david.blasb@alumno.buap.mx",
        "disabled": "False",
        "password": "$2a$12$ht2A1cz6ZebcGckXp4.JLesBUUh3Bq9m8FTw1kC0ORXJ2vhFGaeA."#12345
        },
        "Aldo":{
        "username": "Aldo",
        "full_name": "Cordero Teapila Aldo Javier",
        "email": "aldo.cordero@alumno.buap.mx",
        "disabled": "False",
        "password": "$2a$12$OzjEfeYHbk/Ql.HFlg/yz..57I0eueliLUnuG4Bpx637vOjHEGL1C" #abcd
        },
        "Luis":{
        "username": "Gerardo",
        "full_name": "Luis Gerardo Cruz Sosa",
        "email": "luis.cruzso@alumno.buap.mx",
        "disabled": "False",
        "password": "$2a$12$5t6NML7mJXqCrd0DGeXp5O2p74tbvvn3GcG2i6qZOf0jS1AvqGqNK" #6789
        },
        "DavidFernandez":{
        "username": "DavidFernandez",
        "full_name": "David Fernandez Peres",
        "email": "david.fernandezp@alumno.buap.mx",
        "disabled": "False",
        "password": "$2a$12$CbPQS.Xbs9AItLEVz2VlLeRIcIlpmzHBm7YXCv4Brteu8sHAIq2NS" #1a2b
        },
        "Karyme":{
        "username": "Karyme",
        "full_name": "Karyme Susana Gomez Chavez",
        "email": "karyme.gomez@alumno.buap.mx",
        "disabled": "False",
        "password": "$2a$12$xvne4vWLnniwlM70BM8bxO3A.yGWxHl28oPHHzgoaODQJGxfAuLdG" #wxyz
        },
        "Luis":{
        "username": "Luis",
        "full_name": "Luis David Gonzalez Avendaño",
        "email": "luis.gonzalezav@alumno.buap.mx",
        "disabled": "False",
        "password": "$2a$12$FljwsGJtdfABkgb8jhV4hu4CmDyRwtKg6Yj9aqXJX94tfaHkCIv8K" #5678
        },
        "Hugo":{
        "username": "Hugo",
        "full_name": "Gorgonio Hernandez Lugo",
        "email": "hugo.gorgonio@alumno.buap.mx",
        "disabled": "False",
        "password": "$2a$12$q5s2BZ9xtuyVDh602LjUs.IMaQ/7/jTwcY6I/IfNNMGsCPPhTeoQe" #defg
        },
        "Diego":{
        "username": "Diego",
        "full_name":"Luis Diego Gutierres Barranco",
        "email":"luis.gutierres@alumno.buap.mx",
        "disabled": "False",
        "password": "$2a$12$iKz8CMWIdastwQsTiTLeCuW4bRYr/Kwl2VBsWhUNRHxqP5HTNa/cu" #lmno
        },
        "Victor":{
        "username":"Victor",
        "full_name": "Victor Manuel Gutierrez",
        "email":"victor.gutierrezf@alumno.buap.mx",
        "disabled": "False",
        "password":"$2a$12$Ta2A1Mk51Vouvlv3.cKphO7YYox5b7NDhrpu4Sn0fqmWdrIuuN1oK" #quack
        },
        "Edgar":{
        "username":"Edgar",
        "full_name": "Edgar Fernando Herrera",
        "email":"edgar.herrerar@alumno.buap.mx",
        "disabled": "False",
        "password":"$2a$12$Lo2KQNzwzKfWegsY0R.d2ugx4rbOp339Q7ZnLBe4hJagdoHSDTCbG" #pqrs
        },
        "Armando":{
        "username":"Armando",
        "full_name": "Armando Yasser Landa",
        "email":"armando.landa@alumno.buap.mx",
        "disabled": "False",
        "password":"$2a$12$Wgs4QmgbXQj.Q.pvR42M/unBs9pQILLGfdgNhTpJxRz8XxcrtZnKO" #2322
        },
        "Angelica":{
        "username":"Angelica",
        "full_name": "Norma Angelica Landeta",
        "email":"norma.landeta@alumno.buap.mx",
        "disabled": "False",
        "password":"$2a$12$.QRgFRzmNIGbyQkSypVDWeKeAfwhxDJEwyRkC7o21ZHFNo1u.0FhK" #98hs
        },
        "Maricarmen":{
        "username":"Maricarmen",
        "full_name": "Maria Del Carmen Limon",
        "email":"maria.limongar@alumno.buap.mx",
        "disabled": "False",
        "password":"$2a$12$kwwc4eRGZOW8ty4TGqej9ueg21cgdD9vRWGW1Y7xBXLL8FxNGxPsq" #78fg
        },
        "Jafet":{
        "username":"Jafet",
        "full_name": "Jafet Maravilla",
        "email":"jafet.maravilla@alumno.buap.mx",
        "disabled": "False",
        "password":"$2a$12$BNjWRnym.hwo6A8qa1ToEezFJCOrcwR11.uALXCMleoPU6OSAvOVC" #25ks
        },
        "Miguel":{
        "username":"Miguel",
        "full_name": "Miguel Angel Marie",
        "email":"miguel.marie@alumno.buap.mx",
        "disabled": "False",
        "password":"$2a$12$lBQLgdtmgChueq7bQaxMcOqTrV1WrJFVBL8GY/kJc1KQnWobX0FzW" #wr67
        },
        "Ricardo":{
        "username":"Ricardo",
        "full_name": "Ricardo Arturo Marrufo",
        "email":"ricardo.marrufop@alumno.buap.mx",
        "disabled": "False",
        "password":"$2a$12$hrtZZsOLTm6JebT06JSgfeF3AdwZssZ3Q3FouhGORJV8W4aJs1IF2" #qs53
        },
        "Eunice":{
        "username":"Eunice",
        "full_name": "Martinez Barrales Eunice",
        "email":"eunice.martinez@alumno.buap.mx",
        "disabled": "False",
        "password": "$2a$12$QtoHDbNhQ40pkei9We1mju.KNvMhcgtsK.tDRprzNDU1ZI1phHAZS" #74gs
        },
        "Abdiel":{
        "username":"Abdiel",
        "full_name":"PEREZ BALCON ABDIEL JONATHAN",
        "email":"abdiel.perezb@alumno.buap.mx",
        "disabled":"False",
        "password":"$2a$12$nMfre6cMGqA/v/ANQM4y7.lo18y280qcnK3MyoD/dbvyYT0m7TcGC" #tp46
        },
        "Jordy":{
        "username":"Jordy",
        "full_name":"RAMIREZ HERNANDEZ JORDY",
        "email":"jordy.ramirez@alumno.buap.mx",
        "disabled":"False",
        "password":"$2a$12$Uo.SkTGSnRvtms9.ShzuIeYfX/aVIFUiXV8MNbNva2M2frY1Np66O" #42mb
        },
        "Rodrigo":{
        "username":"Rodrigo",
        "full_name":"SANTOS DE JESUS RODRIGO",
        "email":"rodrigo.santosdej@alumno.buap.mx",
        "disabled":"False",
        "password":"$2a$12$XRlUV/L0tAFZdZYFQkxfduLNEh873nQnaps4mztGeblBxTG3c0KeO" #ft54
        },
        "Leonardo":{
        "username":"Leonardo",
        "full_name":"SEDANO JIMENEZ LEONARDO NOE",
        "email":"leonardo.sedanoji@alumno.buap.mx",
        "disabled":"False",
        "password":"$2a$12$/Iw0HeCO88wZr8FYxAvi6O4Q1SDdeIUI/C1Z/A4/ytqFcuY3j5HFu" #med54
        },
        "Tania":{
        "username":"Tania",
        "full_name":"SEVILLA JIMENEZ TANIA",
        "email":"tania.sevilla@alumno.buap.mx",
        "disabled":"False",
        "password":"$2a$12$AG58LRn4SdT3LnztQq36weI60o4tONKggSQic7QsVdYSeIxwY7Wdy" #jklm
        },
        "Ivan":{
        "username":"Ivan",
        "full_name":"SOLANO CARRERA IVAN",
        "email":"ivan.solano@alumno.buap.mx",
        "disabled":"False",
        "password":"$2a$12$SwzYim5to//Sa0aLS1MGIexOYNafoc/Kw0iaXNlXEiM19SGVddKQS" #bv97
        },
        "Eduardo":{
        "username":"Eduardo",
        "full_name":"SUAREZ SALVATIERRA ANGEL EDUARDO",
        "email":"angel.suarezsa@alumno.buap.mx",
        "disabled":"False",
        "password":"$2a$12$yeAZDmB92y/8NeNf8qE3n.bmx5k38GpNDKbQmuV15bDlASss8moe6" #ed23
        },
        "Jesus":{
        "username":"Jesus",
        "full_name":"TLAMANI XOCHIMITL JESUS",
        "email":"jesus.tlamani@alumno.buap.mx",
        "disabled":"False",
        "password":"$2a$12$JiWFZh3vgka5kRf.qjvTe.Mm9cd/ZTHYhsLyEdOLo2Nbb1cyptqkO" #fy13
        }
    
}
#1 Funcion para regresar el usuario completo de la base de datos (users_db)
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) #** devuelve todos los parámetros del usuario que coincida con username, incluye contraseña encriptada

#4 Funcion final para devolver el usuario a la solicitud del backend (No devuelve la contraseña)
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
#3Esta es la depenencia para buscar al usuario
async def auth_user(token:str=Depends(oauth2)):
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas")
   
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tiempo agotado, vuelve a iniciar sesión")

    return search_user(username) #Esta es la entrega final, usuario sin password

#2 Función para determinar si el usuario esta activo
async def current_user(user:User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user

@app.post("/login/")
async def login(form:OAuth2PasswordRequestForm= Depends()):
    #Busca en la base de datos "users_db" el username que se ingreso en la forma 
    user_db= users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    # Se obtienen los atributos incluyendo password del usuario que coincida el username de la forma 
    user= search_user_db(form.username)    
    
    #user.password es la contraseña encriptada en la base de datos
    #form.password es la contraseña original que viene en formulario
    if not crypt.verify(form.password,user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    #Creamos expiración de 1 min a partir de la hora actual
    access_token_expiration=timedelta(minutes=ACCESS_TOKEN_DURATION)
    #Tiempo de expiración: hora actual mas 1 minuto
    expire=datetime.utcnow()+access_token_expiration
    
    access_token={"sub": user.username,"exp": expire}
    return {"access_token": jwt.encode(access_token, SECRET,algorithm=ALGORITHM), "token_type":"bearer"}

@app.get("/users/me/")
async def me(user:User= Depends (current_user)): #Crea un user de tipo User que depende de la función (current_user)
    if user.username == "David":
        ruta="static/David.jpeg"
        return FileResponse(ruta)
    elif user.username == "Aldo":
        ruta="static/Aldo.jpeg"
        return FileResponse(ruta)
    elif user.username == "DavidFernandez":
        ruta="static/DavidFernandez.jpeg"
        return FileResponse(ruta)
    elif user.username == "Karyme":
        ruta="static/Karyme.jpeg"
        return FileResponse(ruta)
    elif user.username == "Luis":
        ruta="static/Luis.jpeg"
        return FileResponse(ruta)
    elif user.username == "Hugo":
        ruta="static/Hugo.jpeg"
        return FileResponse(ruta)
    elif user.username == "Diego":
        ruta="static/Diego.jpeg"
        return FileResponse(ruta)
    elif user.username == "Victor":
        ruta="static/Victor.jpeg"
        return FileResponse(ruta)
    elif user.username == "Edgar":
        ruta="static/Edgar.jpeg"
        return FileResponse(ruta)
    elif user.username == "Armando":
        ruta="static/Armando.jpeg"
        return FileResponse(ruta)
    elif user.username == "Angelica":
        ruta="static/Angelica.jpeg"
        return FileResponse(ruta)
    elif user.username == "Maricarmen":
        ruta="static/Maricarmen.jpeg"
        return FileResponse(ruta)
    elif user.username == "Jafet":
        ruta="static/Jafet.jpeg"
        return FileResponse(ruta)
    elif user.username == "Miguel":
        ruta="static/Miguel.jpeg"
        return FileResponse(ruta)
    elif user.username == "Ricardo":
        ruta="static/Ricardo.jpeg"
        return FileResponse(ruta)
    elif user.username == "Eunice":
        ruta="static/Eunice.jpeg"
        return FileResponse(ruta)
    elif user.username == "Abdiel":
        ruta="static/Abdiel.jpeg"
        return FileResponse(ruta)
    elif user.username == "Jordy":
        ruta="static/Jordy.jpeg"
        return FileResponse(ruta)
    elif user.username == "Rodrigo":
        ruta="static/Rodrigo.jpeg"
        return FileResponse(ruta)
    elif user.username == "Leonardo":
        ruta="static/Leonardo.jpeg"
        return FileResponse(ruta)
    elif user.username == "Tania":
        ruta="static/Tania.jpeg"
        return FileResponse(ruta)
    elif user.username == "Ivan":
        ruta="static/Ivan.jpeg"
        return FileResponse(ruta)
    elif user.username == "Jesus":
        ruta="static/Eduardo.jpeg"
        return FileResponse(ruta)
    elif user.username == "Eunice":
        ruta="static/Jesus.jpeg"
        return FileResponse(ruta)
    else:
        return user

#http://127.0.0.1:8000/login/

#username:Freddy
#password:1234

#http://127.0.0.1:8000/users/me/

#uvicorn 7_jwt_auth_users:app --reload