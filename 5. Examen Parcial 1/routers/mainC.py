from typing import Union
from fastapi import FastAPI, HTTPException,APIRouter 
from pydantic import BaseModel
router=APIRouter()

class Country(BaseModel):
    id:int
    region:str

CountryList=[
    Country(id=1,region="Australia and New Zealand"),
    Country(id=2,region=    "Southeast Asia"),
    Country(id=3,region=    "Caribbean"),
    Country(id=4,region=    "Micronesia/Caribbean"),
    Country(id=5,region=    "Eastern Africa"),
    Country(id=6,region=    "Northern Africa"),
    Country(id=7,region=    "Southern Europe"),
    Country(id=8,region=    "Central Africa"),
    Country(id=9,region=    "Baltic Countries"),
    Country(id=10,region=    "Eastern Asia"),
    Country(id=11,region=    "Nordic Countries"),
    Country(id=12,region=    "Western Africa"),
    Country(id=13,region=    "Central America"),
    Country(id=14,region=    "Antarctica"),
    Country(id=15,region=    "Eastern Europe"),
    Country(id=16,region=    "Western Europe"),
    Country(id=17,region=    "Southern and Central Asia"),
    Country(id=18,region=    "Melanesia"),
    Country(id=19,region=    "Middle East"),
    Country(id=20,region=    "British Islands"),
    Country(id=21,region=    "South America"),
    Country(id=22,region=    "North America"),
    Country(id=23,region=    "Southern Africa"),
    Country(id=24,region=    "Polynesia"),
    Country(id=25,region=    "Micronesia") 
]
@router.get("/continent/region/",status_code=200)
async def continents():
    return (CountryList)

@router.get("/continent/region/{id}",status_code=200) #Read
async def regions(id:int):
    regions=filter(lambda regiones:regiones.id == id, CountryList)
    try:
        return list(regions)[0]
    except:
        raise HTTPException(status_code=404,detail="No se ha encontrado la informacion")

@router.post("/continent/region/",status_code=201) #Create
async def regions(region:Country):

    for index, guardar in enumerate(CountryList):
        if guardar.id == region.id:
            raise HTTPException(status_code=404,detail="Los datos ya existe")
    else:
        CountryList.append(region)
        return {
            "id=": region.id,
            "region" : region.region
        }


@router.put("/continent/region/",status_code=204) #Update
async def regions(region:Country):
    
    found=False      
    
    for index, saved in enumerate(CountryList):
        if saved.id == region.id:
           CountryList[index] = region
           found=True
           
    if not found:
        raise HTTPException(status_code=404,detail="No se ha actualizado los datos")
    else:
        return region

@router.delete("/continent/region/{id}",status_code=204) #Delete
async def regions(id:int):
    
    found=False      
    
    for index, saved in enumerate(CountryList):
        if saved.id ==id:  
           del CountryList[index] 
           found=True
           return "El registro se ha eliminado"
       
    if not found:
        raise HTTPException(status_code=404,detail="No se ha eliminado el usuario")