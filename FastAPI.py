from fastapi import FastAPI

app = FastAPI()
@app.get("/")
async def root():
    name : str = input() #type: ignore
    age : int = input() #type: ignore

    return name, age
