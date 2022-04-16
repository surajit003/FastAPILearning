import sqlalchemy.exc
from sqlalchemy.orm import Session

import models
import schemas
from exceptions import ItemAlreadyExistException


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_item_by_title(db: Session, item_title):
    db_item = db.query(models.Item).filter_by(title=item_title).first()
    return db_item


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    try:
        db.add(db_item)
        db.commit()
    except sqlalchemy.exc.IntegrityError as exc:
        raise ItemAlreadyExistException(exc.__cause__)
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id, item: schemas.ItemUpdate):
    db_item = db.query(models.Item).get(item_id)
    if db_item:
        item = item.dict()
        db_item.title = item["title"]
        db_item.description = item["description"]
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_item(db, item_id):
    db_item = db.query(models.Item).get(item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    else:
        return None


def patch_item(db, item_id, item):
    db_item = db.query(models.Item).filter_by(id=item_id).first()
    if db_item:
        item = item.dict(exclude_unset=True)
        for key, value in item.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item
