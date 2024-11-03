from fastapi import FastAPI, HTTPException, status
from models.db import db
from models.models import Sheep

app = FastAPI()

@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    return db.get_sheep(id)

@app.post("/sheep/", response_model=Sheep, status_code=status.HTTP_201_CREATED)
def add_sheep(sheep: Sheep):
    if sheep.id in db.data:
        raise HTTPException(status_code=400, detail="Sheep with this ID already exists")

    # Add the new sheep to the database
    db.data[sheep.id] = sheep
    return sheep

@app.delete("/sheep/{id}", response_model=Sheep, status_code=status.HTTP_200_OK)
def delete_sheep(id: int):
    db_sheep = db.get_sheep(id)
    if db_sheep is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Sheep not found")
    db_sheep.delete()
    db_sheep.commit()
    return "Deleted"

@app.put("/sheep/{id}", response_model=Sheep, status_code=status.HTTP_200_OK)
def update_sheep(sheep: Sheep, id: int):
    db_sheep = db.get_sheep(id)
    if db_sheep.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Sheep not found")
    if sheep.id in db.data:
        db.data[id] = sheep
        db.commit()
        return sheep
