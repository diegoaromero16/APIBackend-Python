from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


#Inicia el servidor: uvicorn users:app --reload


app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id= 1, name = "Diego", surname= "Romero", url="http://Instituto.com.ar",age= 25),
         User(id= 2, name = "Sofia", surname="Gomez", url ="http://Instituto2.com.ar",age = 26),
         User(id= 3, name ="Nicolas", surname="Romero", url= "http://Instituto3.com.ar", age= 23)]


#GETS

@app.get("/users")
async def users():
    return users_list

@app.get("/user/")
async def user(id: int):
    return search_user(id)         
         


#POSTS
@app.post("/user/", status_code=201)

async def new_user(user: User):
    if(type(search_user(user.id))) == User:
        HTTPException(status_code=204, detail="El usuario ya existe")
    else:
        users_list.append(user)
        return user

#PUTS

@app.put("/user/")
async def upd_user(user: User):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return({"Error": "No se ha actualizado el usuario"})
    else:
        return user

#DELETE

@app.delete("/user/{id}")

async def delete_user(id: int):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return {"Error": "No se ha eliminado el usuario"}
    

def search_user(id):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error": "No se ha encontrado el usuario"}
    

