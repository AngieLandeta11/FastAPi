class Continent(BaseModel):
    ID: int
    name : str

continent_list = [
    Continent(ID = 1,name="North America"),
    Continent(D = 2,name="South America"),
    Continent(ID = 3,name="Antartica"),
    Continent(ID = 4,name="Africa"),
    Continent(ID = 5,name="Asia"),
    Continent(ID = 6,name="Europa"),
    Continent(ID = 7,name="Oceania")
]