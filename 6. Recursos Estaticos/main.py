from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles
app= FastAPI()

app.mount("/static", StaticFiles(directory="img"), name="static")
# http://127.0.0.1:8000/static/leopardo.jpg


#Documentación con Swagger:  http://127.0.0.1:8000/docs
#Documentación con Redocly:  http://127.0.0.1:8000/redoc