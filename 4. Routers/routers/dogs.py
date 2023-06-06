from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
router=APIRouter()

class Perro(BaseModel):
    id:int
    Nombre:str
    Raza:str
    Edad:int
    Color:str

dogs_list=[
    Perro(id=1,Nombre="Harry",Raza="Pug",Edad=2,Color="Cervato"),
    Perro(id=2,Nombre="Miky",Raza="Bulldog Ingles",Edad=3,Color="Blanco"),
    Perro(id=3,Nombre="Balam",Raza="Boxer",Edad=6,Color="Cafe Claro")
]          
            
@router.get("/dogs/",status_code=200)
async def dogsclass():
    return (dogs_list)

@router.get("/dogs/{id}",status_code=200) #Read
async def dogsclass(id:int):
    dogs=filter(lambda dog:dog.id == id, dogs_list)
    try:
        return list(dogs)[0]
    except:
        raise HTTPException(status_code=404,detail="No se ha encontrado el dato")