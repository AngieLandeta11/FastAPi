from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
router=APIRouter()


class Donut(BaseModel):
    id:int
    Nombre:str
    Precio:int
    Toping:str

donuts_list=[
    Donut(id=1,Nombre="Glaseado",Precio=14,Toping="Chispas"),
    Donut(id=2,Nombre="Azucar",Precio=10,Toping="Chocolate"),
    Donut(id=3,Nombre="Chocolate",Precio=18,Toping="Nuez")
]          
            
@router.get("/donut/",status_code=200)
async def donutclass():
    return (donuts_list)

@router.get("/donut/{id}",status_code=200) #Read
async def donutclass(id:int):
    donuts=filter(lambda donut:donut.id == id, donuts_list)
    try:
        return list(donuts)[0]
    except:
        raise HTTPException(status_code=404,detail="No se ha encontrado el dato")