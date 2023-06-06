from fastapi import APIRouter, Response, status,HTTPException
from config.db import conn
from schemas.user import userEntity, usersEntity
from models.user import User
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

user=APIRouter()

@user.get('/users',response_model=list[User],status_code=200)
def find_all_users():
    return usersEntity(conn.local.user.find());

@user.get('/users/{id}',response_model=User,status_code=200)
def find_user(id:str):
    try:
        return userEntity(conn.local.user.find_one({"_id":ObjectId(id)}))
    except:
        raise HTTPException(status_code=404,detail="No se ha encontrado el usuario")

@user.post('/users',response_model=User,status_code=201)#create
def create_user(user:User):
    new_user=dict(user)
    new_user["password"]=sha256_crypt.encrypt(new_user["password"])
    del new_user["id"]

    id=conn.local.user.insert_one(new_user).inserted_id
    user=conn.local.user.find_one({"_id":id})
    if id==user:
        raise HTTPException(status_code=404,detail="El usuario ya existe")
    else:
        return userEntity(user);


@user.put('/users/{id}',response_model=User)#update
def update_user(id:str,user:User):
    conn.local.user.find_one_and_update({"_id":ObjectId(id)}, {"$set":dict(user)})
    return userEntity(conn.local.user.find_one({"_id":ObjectId(id)}))

@user.delete('/users/{id}',status_code=204)
def delete_user(id:str):
    userEntity(conn.local.user.find_one_and_delete({"_id":ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)