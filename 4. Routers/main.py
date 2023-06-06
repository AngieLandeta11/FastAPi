from fastapi import FastAPI 
from routers import clientes,users,dogs,employer,donuts,drinks,cats,idiomas,university,transport
app= FastAPI()

#routers
app.include_router(clientes.router) 
app.include_router(users.router) 
app.include_router(dogs.router) 
app.include_router(employer.router) 
app.include_router(donuts.router) 
app.include_router(drinks.router) 
app.include_router(cats.router) 
app.include_router(idiomas.router) 
app.include_router(university.router) 
app.include_router(transport.router) 

@app.get("/")

#creamos la función asincrona "imprimir"
async def imprimir():
    return "Hola FastApi"