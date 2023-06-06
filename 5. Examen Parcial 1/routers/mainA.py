from typing import Union
from fastapi import FastAPI, HTTPException, APIRouter 
from pydantic import BaseModel
router=APIRouter()

class Country(BaseModel):
    id:int
    continent:str
    
CountryList=[
    Country(id = 1,continent="North America"),
    Country(id = 2,continent="South America"),
    Country(id = 3,continent="Antartica"),
    Country(id = 4,continent="Africa"),
    Country(id = 5,continent="Asia"),
    Country(id = 6,continent="Europa"),
    Country(id = 7,continent="Oceania")
  ]

@router.get("/continent/",status_code=200)
async def continents():
    return (CountryList)

@router.get("/continent/{id}",status_code=200) #Read
async def continents(id:int):
    continents=filter(lambda continente:continente.id == id, CountryList)
    try:
        return list(continents)[0]
    except:
        raise HTTPException(status_code=404,detail="No se ha encontrado la informacion")

        
#"No se ha encontrado la informacion"
@router.post("/continent/",status_code=201) #Create
async def continents(continent:Country):

    for index, guardar in enumerate(CountryList):
        if guardar.id == continent.id:
            raise HTTPException(status_code=404,detail="Los datos ya existe")
    else:
        CountryList.append(continent)
        return {
            "id=": continent.id,
            "continent=" : continent.continent
        }

@router.put("/continent/",status_code=204) #Update
async def continents(continent:Country):
    
    found=False      
    
    for index, saved in enumerate(CountryList):
        if saved.id == continent.id:
           CountryList[index] = continent  
           found=True
           
    if not found:
        raise HTTPException(status_code=404,detail="No se ha actualizado los datos")
    else:
        return continent

@router.delete("/continent/{id}",status_code=204) #Delete
async def continents(id:int):
    
    found=False      
    
    for index, saved in enumerate(CountryList):
        if saved.id ==id:  
           del CountryList[index] 
           found=True
           return "El registro se ha eliminado"
       
    if not found:
        raise HTTPException(status_code=404,detail="No se ha eliminado el usuario")