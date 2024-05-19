from sqlalchemy.orm import Session

from models.model_blog import Blog
from models.model_reader import Reader
from models.model_reader_blog import ReaderBlog

def get_user(db: Session, user_id: int):
    return db.query(Reader).filter(Reader.id == user_id).first()


def create_new_user(db: Session, user: Reader):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Reader).offset(skip).limit(limit).all()

def delete_user(db: Session , user_id: int):
    user = db.query(Reader).filter(Reader.id == user_id).first()
    db.delete(user)
    db.commit()
    return user
