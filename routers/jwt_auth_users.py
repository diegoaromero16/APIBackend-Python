from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
crypt = CryptContext(schemes=["bcrypt"])

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl= "login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "dromero": {"username": "dromero",
                "full_name": "Diego Romero",
                "email": "diegoaromero16@gmail.com",
                "disabled": False,
                "password": "$2y$12$JKjTKLHhJ4fzF7aW3pF/6uqdeFJkXdwXiFGXMUjUFEs1dHdx0ImP6"
    },
    "dromero2": {"username": "dromero2",
                "full_name": "Diego Romero2",
                "email": "diegoaromero162@gmail.com",
                "disabled": True,
                "password": "$2y$12$M2W2exjzrE4DwbWcufNjZefMcfL9/tKLv5R9SxeWpkivdDfkP3A1C"
    }
}


def search_userDB(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                            detail="Credenciales de autenticacion invalidas",
                            headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except JWTError:
       raise exception
    
    return search_user(username)
         
async def current_user(user: User = Depends(auth_user)): 
    if user.disabled:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, 
                            detail="Usuario Inactivo")
    return user

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not users_db:
        raise HTTPException(status_code=400, detail="El Usuario no es correcto")
    user = search_userDB(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")
    
    access_token = {"sub": user.username, 
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    }

    return {"access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM), "token_type": "bearer"}


@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user