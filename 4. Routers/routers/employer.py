from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
router=APIRouter()


class Empleado(BaseModel):
    id:int
    Nombre:str
    Salario:int
    Puesto:str

employers_list=[
    Empleado(id=1,Nombre="Luis",Salario=14500,Puesto="Vendedor"),
    Empleado(id=2,Nombre="Fernando",Salario=10000,Puesto="Gerente"),
    Empleado(id=3,Nombre="Laura",Salario=22400,Puesto="Empresario")
]          
            
@router.get("/employer/",status_code=200)
async def employersclass():
    return (employers_list)

@router.get("/employer/{id}",status_code=200) #Read
async def employerclass(id:int):
    employers=filter(lambda employer:employer.id == id, employers_list)
    try:
        return list(employers)[0]
    except:
        raise HTTPException(status_code=404,detail="No se ha encontrado el dato")