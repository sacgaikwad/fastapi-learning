from app.database.database import engine
from app.database.base import Base
from app.database.models.user import User


def init_db():
    Base.metadata.create_all(bind=engine)