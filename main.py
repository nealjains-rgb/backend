import os
import psycopg2

from fastapi import FastAPI, HTTPException

from passlib.context import CryptContext

from jose import jwt


app = FastAPI()


# database

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)


# password hashing

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


SECRET_KEY = "mysecret"


# Signup API

@app.post("/signup")

def signup(email: str, password: str):

    cur = conn.cursor()

    hashed = pwd_context.hash(password)

    try:

        cur.execute(

            "INSERT INTO users(email,password) VALUES(%s,%s)",

            (email, hashed)

        )

        conn.commit()

        return {"message": "created"}

    except:

        raise HTTPException(

            status_code=400,

            detail="user exists"

        )


# Login API

@app.post("/login")

def login(email: str, password: str):

    cur = conn.cursor()

    cur.execute(

        "SELECT id,password FROM users WHERE email=%s",

        (email,)

    )

    user = cur.fetchone()

    if not user:

        raise HTTPException(

            status_code=401,

            detail="user not found"

        )

    if not pwd_context.verify(

        password,

        user[1]

    ):

        raise HTTPException(

            status_code=401,

            detail="wrong password"

        )


    token = jwt.encode(

        {"user_id": user[0]},

        SECRET_KEY,

        algorithm="HS256"

    )


    return {

        "token": token

    }
