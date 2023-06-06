from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
router=APIRouter()

class Cat(BaseModel):
    id:int
    Nombre:str
    Raza:str
    Edad:int
    Color:str

cats_list=[
    Cat(id=1,Nombre="Eddy",Raza="Mestizo",Edad=2,Color="Gris"),
    Cat(id=2,Nombre="Tony",Raza="Persa",Edad=3,Color="Blanco"),
    Cat(id=3,Nombre="Luna",Raza="Bengali",Edad=1,Color="Naranja")
]          
            
@router.get("/cats/",status_code=200)
async def catsclass():
    return (cats_list)

@router.get("/cats/{id}",status_code=200) #Read
async def catsclass(id:int):
    cats=filter(lambda cat:cat.id == id, cats_list)
    try:
        return list(cats)[0]
    except:
        raise HTTPException(status_code=404,detail="No se ha encontrado el dato")