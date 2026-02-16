from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

DATABASE_URL = DATABASE_URL = os.getenv("DATABASE_URL")


conn = psycopg2.connect(DATABASE_URL)

@app.get("/")
def home():
    return {"message": "Backend working"}

@app.get("/db")
def db():

    cursor = conn.cursor()

    cursor.execute("SELECT NOW();")

    return cursor.fetchone()
