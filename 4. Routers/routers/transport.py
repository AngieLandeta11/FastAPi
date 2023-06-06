from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
router=APIRouter()

class Trasporte(BaseModel):
    id:int
    Tipo:str
    Marca:str
    Color:str

transport_list=[
    Trasporte(id=1,Tipo="Moto",Marca="Harley Davidson",Color="Negro"),
    Trasporte(id=2,Tipo="Automovil",Marca="Chevrolet",Color="Blanco"),
    Trasporte(id=3,Tipo="Bicicleta",Marca="Aurum",Color="Naranja"),
    Trasporte(id=4,Tipo="Avion",Marca="Lockheed Martin",Color="Blanco")
]          
            
@router.get("/transports/",status_code=200)
async def transportsclass():
    return (transport_list)

@router.get("/transports/{id}",status_code=200) #Read
async def utransportsclass(id:int):
    transports=filter(lambda transport:transport.id == id, transport_list)
    try:
        return list(transports)[0]
    except:
        raise HTTPException(status_code=404,detail="No se ha encontrado el dato")