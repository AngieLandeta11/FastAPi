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
    "Freddy":{
    "username":"Freddy",
    "full_name": "Freddy García",
    "email": "alfredo.garcias@alumno.buap.mx",
    "disabled": False,
    "password": "$2a$12$Px4/G9Onxs4m6QxjAwsbtOmqf4BFxkLUvn3F5PFPbWmhWLYEyGObG" #1234
    },
    "Romi":{
    "username":"Romi",
    "full_name": "Romi Vargas Romero",
    "email":"romi08@gmail.com",
    "disabled": False,
    "password":"$2a$12$1rrX9oGw1BKMjNz6BPrNouphZD8EywduGUxGfLe1zwnsPqxIFU3My" #08081
  },
  "Angie":{
    "username": "Angie",
    "full_name": "Angie Landeta",
    "email": "angie21lan@yahoo.com",
    "disabled": False,
    "password": "$2a$12$ARsGgITxtfAEUYY9sHRBTehQxATfoOkY/40lrkH802/Q3g4x0XZm2" #21041
  },
  "Darrell":{
    "username": "Darrell",
    "full_name": "Darrell Anderson",
    "email": "rachel_weisz@yahoo.com",
    "disabled": False,
    "password": "$2a$12$H7kUGOgPm1MpPBapkihJNugggZ2B.xTRenWPNiPR40TyZzUHwRY5m" #12345
  },
  "Nicole":{
    "username": "Nicole",
    "full_name": "Nicole Powell",
    "email": "winford_kerr@hotmail.com",
    "disabled": False,
    "password": "$2a$12$6v6OzlqiDf0Adrk9zdYpHufZHfLKKpzr3WHp4Vk.vtsybKYKx5ZkS" #67890
  },
  "Timothe":{
    "username": "Timothe",
    "full_name": "Timothe Holmes",
    "email": "wesley_hobbs@outlook.com",
    "disabled": True,
    "password": "$2a$12$DimaGnACO65tFAsBg4QGCONb3bvSsOUrNFun3BgMCWMqNq.HCNfFG" #98761
  },
  "Lance":{
    "username": "Lance",
    "full_name": "Lance Singh",
    "email": "jesica_jamieson@gmail.com",
    "disabled": False,
    "password": "$2a$12$nn0itt5at4lTPLvPSHtoBe.N92JJpsHfltfHNnXSV47ztBOpHU39u" #65432
  },
  "Kaitlyn":{
    "username": "Kaitlyn",
    "full_name": "Kaitlyn Mitchell",
    "email": "lorette_ali@zohomail.com",
    "disabled": True,
    "password": "$2a$12$kb6hF4O9QdqQ46H113tV.OwCps84c5mMGWUGjkL9ta.2A6NsRupzC" #21234
  },
  "Michel":{
    "username": "Michel",
    "full_name": "Michel Edwards",
    "email": "ashlie_bowman@mail.com",
    "disabled": True,
    "password": "$2a$12$2Bp5NROgXOT4D7hOnq78ju3i6upG0l8itXlfZ64Oz2CJ8XRgk0ucG" #45678
  },
  "Joss":{
    "username": "Joss",
    "full_name": "Joss Brown DDS",
    "email": "noel_knight@yandex.com",
    "disabled": False,
    "password": "$2a$12$eLFDAYQv1r3RRd1C4zLlzO0Xf6lh5VYiwnmpABvaKcsFBDsg15d6u" #89098
  },
  "Scott":{
    "username": "Scott",
    "full_name": "Scott Smith",
    "email": "vincent_miller@aol.com",
    "disabled": False,
    "password": "$2a$12$pgsNU86gCC7qUo.eC9ms4OO.Ejv7gk1cKkfsBwWv/TWDlnbWA0v6O" #87654
  },
  "Amy":{
    "username": "Amy",
    "full_name": "Amy Rhodes",
    "email": "desirae_healy@yahoo.com",
    "disabled": True,
    "password": "$2a$12$HirBRkzjIzhLBOY9dy3VLeOcwP3a846m5T0p0zAvPmkZ0HjGBQPKC" #43212
  },
  "Sherry":{
    "username": "Sherry",
    "full_name": "Sherry Anderson",
    "email": "kacie_cassidy@gmail.com",
    "disabled": False,
    "password": "$2a$12$mA2bJdyBIJuKJThauBzw9O1OHFkh35XSauuY2uDhpOmNSlmOgJxOS" #23456
  },
  "Mary":{
    "username": "Mary",
    "full_name": "Mary Riley",
    "email": "kenneth_heaton@gmail.com",
    "disabled": True,
    "password": "$2a$12$Hoait/K71h.XdKfJfRt33.AfndhDeUOrqk2zLkDKu7FtoieZNpHvK" #78909
  },
  "Stacy":{
    "username": "Stacy",
    "full_name": "Stacy Harvey",
    "email": "nannette_lamb@yandex.com",
    "disabled": True,
    "password": "$2a$12$A0mXttZYzsXmQJaIAATaYuR8e8ZqyAYjGfr4gUNdVSxeWOK1sTYE." #24680
  },
  "Jasmine":{
    "username": "Jasmine",
    "full_name": "Jasmine Jones",
    "email": "retha_feeney@yandex.com",
    "disabled": False,
    "password": "$2a$12$HtMhr2.oZGby4FjQopn0mettxINaEbD6USsr7eDiXLdhD8j9mORbO" #46808
  },
  "Alyssa":{
    "username": "Alyssa",
    "full_name": "Alyssa Burns",
    "email": "verla_allan@protonmail.com",
    "disabled": False,
    "password": "$2a$12$txBhmfZjm3wl/zKfC0US0.JNrjsIzsHeJz8Pm803EI5yc/AyaTtRW" #28667
  },
  "Andy":{
    "username": "Andy",
    "full_name": "Andy Williams",
    "email": "soila_newman@yahoo.com",
    "disabled": True,
    "password": "$2a$12$4snanEyJ6sLImIwnHz3sBuZOClqlu7YTE9aZzz9.zPJwFsFDfxnv2" #13579
  },
  "Mathew":{
    "username": "Mathew",
    "full_name": "Mathew Brooks",
    "email": "tawnya_read@mail.com",
    "disabled": False,
    "password": "$2a$12$Y6aXr7A6L1yfiRMqOoj/7eV25DewNFayC6JufZso1pIV/jEkHDx8m" #75313
  },
  "Charly":{
    "username": "Charly",
    "full_name": "Charly Craig",
    "email": "marth_charles@gmail.com",
    "disabled": True,
    "password": "$2a$12$nKX/XKnh0OI/6gaMsXrzguHfLXDigG0CkEtH3CwhSX4pmm2VysN5m" #35790
  },
  "Mark":{
    "username": "Mark",
    "full_name": "Mark Barnes",
    "email": "jed_boyce@yahoo.com",
    "disabled": True,
    "password": "$2a$12$QQqXQQMjnyZ38FbhWEV3i./bCTFszQkUIvxxsFrJySa6VwGy3uVde" #21345
  },
  "Daniel":{
    "username": "Daniel",
    "full_name": "Daniel Matthews",
    "email": "inez_poole@zohomail.com",
    "disabled": False,
    "password": "$2a$12$EspvGsVbdnKBngRq6jKphus4fkk4UE1.06qZoh66otNXk5m7.hgdy" #89786
  },
  "Bambi":{
    "username": "Bambi",
    "full_name": "Bambi Bennett",
    "email": "ken_watanabe@zohomail.com",
    "disabled": False,
    "password": "$2a$12$KX9/BDWHSZAJv/sfSSgE/e8PF8h3ULBEP6j/KfWEAkbEBKPtaz9kW" #43565
  },
  "Cole":{
    "username": "Cole",
    "full_name": "Cole Green MD",
    "email": "vera_farmiga@yahoo.com",
    "disabled": True,
    "password": "$2a$12$FPrviasjrXEoED9o7k2xOubIp0GSnRnP9padCHUi4o00fNgh0MhPa" #71235
  },
  "Eric":{
    "username": "Eric",
    "full_name": "Eric Petty",
    "email": "hayden_panettiere@mail.com",
    "disabled": False,
    "password": "$2a$12$fSqw6CnrBvdqvVvwdsMcYOMQJJOD647LxfZ7z6eT1aCEjzSyxImGy" #83654
  },
  "Denise":{
    "username": "Denise",
    "full_name": "Denise Sanchez",
    "email": "alyssa_veniece@zohomail.com",
    "disabled": True,
    "password": "$2a$12$FI/nr6IeB/IQ0a2xGNw4aub3Ds/00VreFrCeOil9H3zWap3HZHgQ2" #14890
  },
  "Willi":{
    "username": "Willi",
    "full_name": "Willi Williams",
    "email": "logan_lerman@hotmail.com",
    "disabled": True,
    "password": "$2a$12$pkpRes2DSKvamuKBNIFEue8XAyfnMyGOKhsjxjLD8xETzHUjJgHuy" #98765
  },
  "Madeline":{
    "username": "Madeline",
    "full_name": "Madeline Morgan",
    "email": "melanie_lynskey@zohomail.com",
    "disabled": False,
    "password": "$2a$12$T2jst8qVHE.uvh1gG1bIsu2lOuPHaTndVlKVLl60N40q8NusZID1K" #26542
  },
  "Antonia":{
    "username": "Antonia",
    "full_name": "Antonia Jackson",
    "email": "gabriella_wilde@aol.com",
    "disabled": False,
    "password": "$2a$12$LWOSZEIZ7Q.lzQRBcv.onezh0nmYYUeAExzVXJUXcSItZu37XUXEG" #54899
  },
  "Nadia":{
    "username": "Nadia",
    "full_name": "Nadia Cooper",
    "email": "mathias_nader93@hotmail.com",
    "disabled": False,
    "password": "$2a$12$N7pdy6FCLKUblbpuiuyZZuipcPLeFHpo6nYXUJjePF8k2peP/bTZ." #98742
  },
  "Elizabeth":{
    "username": "Elizabeth",
    "full_name": "Elizabeth Nelson",
    "email": "piper.kessler@hotmail.com",
    "disabled": True,
    "password": "$2a$12$WdHlokopQsZR5Z52P3spG.dcsEzWDfe5vWA8H3w4orlVQmkPS8kg6" #19826
  },
  "Thomas":{
    "username": "Thomas",
    "full_name": "Thomas Gomez",
    "email": "mitchel_kohler89@gmail.com",
    "disabled": False,
    "password": "$2a$12$WmP4ppiN23WVSOc3QuaFJO3R4lwCyAIF4719piaIjk7Mgak70vi9e" #01547
  },
  "Aline":{
    "username": "Aline",
    "full_name": "Aline Harrison",
    "email": "alene_hettinger13@gmail.com",
    "disabled": True,
    "password": "$2a$12$2HjVlXp24bCQMDlQHOoKt.MY2FzjipR/Yu.rieR/rGHi/ia03hzr." #16452
  },
  "Jacob":{
    "username": "Jacob",
    "full_name": "Jacob Parker",
    "email": "elisha_bahringer@gmail.com",
    "disabled": False,
    "password": "$2a$12$4iGt4yWWuC1HyfKH.93DpeXDCg5cUYA7COcco/WbhxWlqW7PSfGRC" #74517
  },
  "Kiara":{
    "username": "Kiara",
    "full_name": "Kiara Burke",
    "email": "santiago_braun@hotmail.com",
    "disabled": True,
    "password": "$2a$12$LjZ7hpbNRGYKg5Nu1Def1OUzmajFOt7r88PFX8vwIWfnqbnPBg.0O" #62259
  },
  "Zachary":{
    "username": "Zachary",
    "full_name": "Zachary Allen",
    "email": "corene_mueller66@gmail.com",
    "disabled": True,
    "password": "$2a$12$e5IJvSz5Mm4luJG1ba3t8ORjBHK85xZfzcTZXRodpSJwBe/sXkbRi" #88162
  },
  "Carrie":{
    "username": "Carrie",
    "full_name": "Carrie Carroll",
    "email": "carrie.moen28@gmail.com",
    "disabled": False,
    "password": "$2a$12$GXOUZ/dJ2ui7sus7MGx/ae9C7VpMR8R6Tpuic/26pGfskzDrnseqm" #70154
  },
  "Joseph":{
    "username": "Joseph",
    "full_name": "Joseph Williams",
    "email": "melvin.johnston@hotmail.com",
    "disabled": True,
    "password": "$2a$12$tvpRC4ZuAHupNkS0DjZLO.RCS/7IdCElr628zFxKN8bSdqRt.e1Gi" #25433
  },
  "Steven":{
    "username": "Steven",
    "full_name": "Steven Wheeler",
    "email": "ramona40@yahoo.com",
    "disabled": True,
    "password": "$2a$12$9ZfIgkRAuYCYIWet8dXu.eqgD6khMrbumFQv0SF.gNgiLV2ho9skq" #17432
  },
  "Jonath":{
    "username": "Jonath",
    "full_name": "Jonath Jones",
    "email": "tiara80@hotmail.com",
    "disabled": False,
    "password": "$2a$12$eKL3KNFGqa2fZyyR/uzwvO8ky9GtwqvIo1X38YQ8M7kR22jNpb2F2" #96409
  },
  "Heath":{
    "username": "Heath",
    "full_name": "Heath Lopez",
    "email": "henriette.rolfson11@yahoo.com",
    "disabled": True,
    "password": "$2a$12$n2KWpjj.WFFVKVgM6pF7y.Ah9pf5s/RM3lFVALu/QJ.o4UoXyUBVu" #80578
  },
  "Ethan":{
    "username": "Ethan",
    "full_name": "Ethan Williams",
    "email": "pink31@gmail.com",
    "disabled": True,
    "password": "$2a$12$pCHLXUot.8xNav5SfOWTDu7JDnd1CLaqti9cKwNNWyQcC44bPPYbm" #37566
  },
  "Micha":{
    "username": "Micha",
    "full_name": "Micha Cole",
    "email": "elva38@hotmail.com",
    "disabled": False,
    "password": "$2a$12$QnhJkk1mmADPvuYSK.D2tuGyBi0BHm6jDd/ThaSOlrqCxsraQWaK2" #70065
  },
  "Gregory":{
    "username": "Gregory",
    "full_name": "Gregory Carroll",
    "email": "toni_kutch@hotmail.com",
    "disabled": True,
    "password": "$2a$12$6kOwXA/.uXjKaAJai3YxbeJypQgim4yPsN7c7ZOuf/83UYfFkgdqK" #01566
  },
  "Brent":{
    "username": "Brent",
    "full_name": "Brent Bailey",
    "email": "brook1@yahoo.com",
    "disabled": True,
    "password": "$2a$12$mHcOobHoHqAbqaSE3aUd3OJpJeU5zV/9p3oeTMOhOiCfFXTjbU4Vu" #27665
  },
  "Travis":{
    "username": "Travis",
    "full_name": "Travis Morse",
    "email": "jefferey_dubuque70@hotmail.com",
    "disabled": True,
    "password": "$2a$12$1TMmfm/gg5iLNq6CTzRbjO6ynyVAYDdqc/D.yHxddrlTOo23sXpry" #99165
  },
  "Jennifer":{
    "username": "Jennifer",
    "full_name": "Jennifer Palmer",
    "email": "kenton4@gmail.com",
    "disabled": False,
    "password": "$2a$12$6Q7c1Lw3LE.k0WrVxwELze.t79ZrK0DeXogMRTjVb82BdKfGlmdgy" #76765
  },
  "Rya":{
    "username": "Rya",
    "full_name": "Rya Smith",
    "email": "annetta.casper60@hotmail.com",
    "disabled": True,
    "password": "$2a$12$6rNO1SbSn5RFrE3t3QG4LOiSQ4FBkIemK83nJf/vy.nraQySW0yTq" #27662
  },
  "Kevi":{
    "username": "Kevi",
    "full_name": "Kevi Myers",
    "email": "roscoe68@gmail.com",
    "disabled": False,
    "password": "$2a$12$gRWz4gUtuRlP6jHDjoVRIOat0F.1OqmH3gm2ovu36qXG39L4ZgneS" #65509
  },
  "Mya":{
    "username": "Mya",
    "full_name": "Mya Riley",
    "email": "mya_kovacek@gmail.com",
    "disabled": True,
    "password": "$2a$12$CdirF0VcloQYJhdjnjMGxeOkOljdfJBcGojKfnWTUgh5RFBPrym9G" #91654
  },
  "Benjami":{
    "username": "Benjami",
    "full_name": "Benjami Olsen",
    "email": "trace.bosco@hotmail.com",
    "disabled": True,
    "password": "$2a$12$jh7X5BBoOxbq1CoKuF7gz..8WxftEGyVxP8EnzN5aCxPZ3FMM1deO" #29912
  },
  "Justin":{
    "username": "Justin",
    "full_name": "Justin Baker MD",
    "email": "yasmine.schmitt81@gmail.com",
    "disabled": False,
    "password": "$2a$12$a2PaXaxgcdq3qk/H/BryIeTsyUgXJlTMgCR9VAdzmoWgGB.exCs9K" #20054
  },
  "Timothy":{
    "username": "Timothy",
    "full_name": "Timothy Gonzalez",
    "email": "rollin.will@hotmail.com",
    "disabled": True,
    "password": "$2a$12$rpg.BJ0X7LqUPHbIyCCV0efxJdPJqgF5iCMWjlAtktwZaFBVvcGOa" #74434
  },
  "Melissa":{
    "username": "Melissa",
    "full_name": "Melissa Taylor",
    "email": "herminia93@hotmail.com",
    "disabled": False,
    "password": "$2a$12$2Qnu0BqOKFYRsL3S0Zrlaev2t6J3oOfAy.CErGgTvp.BpVKSwsSmG" #91699
  },
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
    if user.username == "Freddy":
        ruta="static/Incendio.jpg"
        return FileResponse(ruta)
    elif user.username == "Romi":#08081
        ruta="templates/index.html"
        return FileResponse(ruta)
    elif user.username == "Angie":#21041
        ruta="static/paisaje.jpg"
        return FileResponse(ruta)
    else:
        return user

#http://127.0.0.1:8000/login/

#username:Freddy
#password:1234

#http://127.0.0.1:8000/users/me/

#uvicorn 7_jwt_auth_users:app --reload