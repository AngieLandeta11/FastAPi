from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
router=APIRouter()

class Idioma(BaseModel):
    id:int
    Nombre:str
    Dificultad:str
    Pais:str

idioms_list=[
    Idioma(id=1,Nombre="Ingles",Dificultad="Media",Pais="Estados Unidos"),
    Idioma(id=2,Nombre="Chino",Dificultad="Alta",Pais="China"),
    Idioma(id=3,Nombre="Frances",Dificultad="Media",Pais="Francia")
]          
            
@router.get("/idioms/",status_code=200)
async def idiomsclass():
    return (idioms_list)

@router.get("/idioms/{id}",status_code=200) #Read
async def idiomsclass(id:int):
    idioms=filter(lambda idiom:idiom.id == id, idioms_list)
    try:
        return list(idioms)[0]
    except:
        raise HTTPException(status_code=404,detail="No se ha encontrado el dato")