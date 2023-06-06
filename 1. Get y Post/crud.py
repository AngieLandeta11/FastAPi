#importamos el framework fastapina clase
from fastapi import FastAPI
from pydantic import BaseModel
app= FastAPI()

class User(BaseModel):
    id:int
    Survived:int
    Pclass:int
    Name:str
    sex:str
    age:int

users_list=[User(id=1,Survived=0,Pclass=3,Name="Braund, Mr. Owen Harris",sex="male  ", age=22),  
User(id=2,Survived=1,Pclass=1,Name="Cumings, Mrs. John Brad",sex="female", age=38),  
User(id=3,Survived=1,Pclass=3,Name="Heikkinen, Miss. Laina ",sex="female", age=26),  
User(id=4,Survived=1,Pclass=1,Name="Futrelle, Mrs. Jacques ",sex="female", age=35), 
User(id=5,Survived=0,Pclass=3,Name="Allen, Mr. William Henr",sex="male  ", age=35),
User(id=6,Survived=0,Pclass=3,Name="Moran, Mr. James       ",sex="male  ", age=45),
User(id=7,Survived=0,Pclass=1,Name="McCarthy, Mr. Timothy J",sex= "male ", age=54),  
User(id=8,Survived=0,Pclass=3,Name="Palsson, Master. Gosta ",sex="male  ", age=2 ),   
User(id=9,Survived=1,Pclass=3,Name="Johnson, Mrs. Oscar W  ",sex="female", age=27),
User(id=1,Survived=0  ,Pclass=1   ,Name="    Nasser, Mrs. Nicholas "  ,sex="female" ,age= 14),
User(id=11,Survived=  1,Pclass=   3,Name="   Sandstrom, Miss. Margue" ,sex="female" ,age= 4 ),
User(id=12,Survived=  1,Pclass=   1,Name="   Bonnell, Miss. Elizabet" ,sex="male  " ,age= 58),  
User(id=13,Survived=  0,Pclass=   3,Name="   Saundercock, Mr. Willia" ,sex="male  " ,age= 20), 
User(id=14,Survived=  0,Pclass=   3,Name="   Andersson, Mr. Anders J" ,sex="male 3" ,age= 9 ), 
User(id=15,Survived=  0,Pclass=   3,Name="   Vestrom, Miss. Hulda Am" ,sex="female",age=14),
User(id=16,Survived=  1,Pclass=   2,Name="   Hewlett, Mrs. (Mary D K" ,sex="female"  ,age=7),
User(id=17,Survived=  0,Pclass=   3,Name="   Rice, Master. Eugene   " ,sex="male 2" ,age= 43),
User(id=18,Survived=  1,Pclass=   2,Name="   Williams, Mr. Charles E" ,sex="male  " ,age= 34),
User(id=19,Survived=  0,Pclass=   3,Name="   Vander Planke, Mrs. Jul" ,sex="female" ,age= 12), 
User(id=20,Survived=  1,Pclass=   3,Name="   Masselmani, Mrs. Fatima" ,sex="male 4" ,age= 3),
User(id=21,Survived=  0,Pclass=   2,Name="   Fynney, Mr. Joseph J   " ,sex="female" ,age= 45),
User(id=22,Survived=  1,Pclass=   2,Name="   Beesley, Mr. Lawrence  " ,sex="male  " ,age= 8),
User(id=23,Survived=  1,Pclass=   3,Name="   McGowan, Miss. Anna An"  ,sex="male  " ,age= 15),
User(id=24,Survived=  1,Pclass=   1,Name="   Sloper, Mr. William Tho" ,sex="male  " ,age= 28),
User(id=25,Survived=  0,Pclass=   3,Name="   Palsson, Miss. Torborg " ,sex="female" ,age= 8 )]           
            
@app.get("/usersclass/")
async def usersclass():
    return (users_list)

@app.get("/usersclass/{id}")
async def usersclass(id:int):
    users=filter(lambda user:user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return{"error":"No se ha encontrado el usuario"} 

@app.post("/usersclass/")
async def usersclass(user:User):

    for index, guardar_usuario in enumerate(users_list):
        if guardar_usuario.id == user.id:
            return {"errror":"el usuario ya existe"}
    else:
        users_list.append(user)
        return user

