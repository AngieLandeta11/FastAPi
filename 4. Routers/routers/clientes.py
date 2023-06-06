from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
router=APIRouter()


class Cliente(BaseModel):
    id:int
    Nombre:str
    Apellido:str
    Edad:int
    Estatura:int

clientes_list=[
    Cliente(id=1,Nombre="Sigrid",Apellido="Mannock",Edad=27,Estatura=160),
    Cliente(id=2,Nombre="Joe",Apellido="Hinners",Edad=31,Estatura=171),
    Cliente(id=3,Nombre="Theodoric",Apellido="Rivers",Edad=36,Estatura=164)
]          
            
@router.get("/clientes/",status_code=200)
async def clientesclass():
    return (clientes_list)

@router.get("/clientes/{id}",status_code=200) #Read
async def clientesclass(id:int):
    clientes=filter(lambda cliente:cliente.id == id, clientes_list)
    try:
        return list(clientes)[0]
    except:
        raise HTTPException(status_code=404,detail="No se ha encontrado el cliente")