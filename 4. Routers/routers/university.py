from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
router=APIRouter()

class Universidad(BaseModel):
    id:int
    Nombre:str
    Estado:str
    Mascota:str

university_list=[
    Universidad(id=1,Nombre="Buap",Estado="Puebla",Mascota="Lobo"),
    Universidad(id=2,Nombre="Tec de Monterrey",Estado="CDMX",Mascota="Borrego"),
    Universidad(id=3,Nombre="UV",Estado="Veracruz",Mascota="Halcon"),
    Universidad(id=4,Nombre="UNAM",Estado="CDMX",Mascota="Puma")
]          
            
@router.get("/universities/",status_code=200)
async def universitiesclass():
    return (university_list)

@router.get("/universities/{id}",status_code=200) #Read
async def universitiesclass(id:int):
    universities=filter(lambda university:university.id == id, university_list)
    try:
        return list(universities)[0]
    except:
        raise HTTPException(status_code=404,detail="No se ha encontrado el dato")