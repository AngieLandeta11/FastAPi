from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
router=APIRouter()


class Drink(BaseModel):
    id:int
    Nombre:str
    Precio:int
    Marca:str

drink_list=[
    Drink(id=1,Nombre="Water",Precio=26,Marca="bonafont"),
    Drink(id=2,Nombre="Soda",Precio=18,Marca="Sprite"),
    Drink(id=3,Nombre="Wine",Precio=256,Marca="Prosecco"),
    Drink(id=3,Nombre="Beer",Precio=63,Marca="XX")
]          
            
@router.get("/drink/",status_code=200)
async def drinkclass():
    return (drink_list)

@router.get("/drink/{id}",status_code=200) #Read
async def drinkclass(id:int):
    drinks=filter(lambda drink:drink.id == id, drink_list)
    try:
        return list(drinks)[0]
    except:
        raise HTTPException(status_code=404,detail="No se ha encontrado el dato")