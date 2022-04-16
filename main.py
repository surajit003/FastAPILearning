from typing import List

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, status, HTTPException, Response

import exceptions
import models
import crud
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.post("/items/",status_code=status.HTTP_201_CREATED)
def create_item(
        item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    try:
        item = crud.create_item(db=db, item=item)
    except exceptions.ItemAlreadyExistException as exc:
        raise HTTPException(status_code=200, detail=str(exc))
    return item


@app.put("/items/{item_id}/", response_model=schemas.Item)
def update_item(item_id, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    item = crud.update_item(db=db, item=item, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"item with id {item_id} not found")
    return item


@app.delete("/items/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id, db: Session = Depends(get_db)):
    item = crud.delete_item(db=db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"item with id {item_id} not found")
    else:
        return {"status": "successful"}


@app.patch("/items/{item_id}/", response_model=schemas.Item)
def patch_item(item_id, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    item = crud.patch_item(db=db, item_id=item_id, item=item)
    if not item:
        raise HTTPException(status_code=404, detail=f"item with id {item_id} not found")
    else:
        return item
