import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Загрузка переменных из .env
load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRESQL_USER')}:{os.getenv('POSTGRESQL_PASSWORD')}"
    f"@{os.getenv('POSTGRESQL_HOST')}:{os.getenv('POSTGRESQL_PORT')}/{os.getenv('POSTGRESQL_DBNAME')}"
)

# Создание engine и сессии
engine = create_engine(DATABASE_URL, isolation_level="READ COMMITTED")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
Base = declarative_base()


# Модель данных
class Thread(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, nullable=False)
    thread_id = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)


# Контекстный менеджер для автоматического открытия и закрытия сессии
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db  # Возвращаем сессию для использования
    finally:
        db.close()  # Закрываем сессию после использования


# Создание
def create_thread(chat_id: int, thread_id: str):
    with get_db() as db:
        with db.begin():
            db_thread = Thread(chat_id=chat_id, thread_id=thread_id)
            db.add(db_thread)
            db.commit()
            db.refresh(db_thread)
            return db_thread


# Чтение
def get_thread(chat_id: int):
    with get_db() as db:
        with db.begin():
            return db.query(Thread).filter(Thread.chat_id == chat_id).first().thread_id


def get_all_threads():
    with get_db() as db:
        with db.begin():
            return db.query(Thread).all()


# Обновление
def update_thread(thread_id: str, chat_id: int):
    with get_db() as db:
        with db.begin():
            db_thread = db.query(Thread).filter(Thread.thread_id == thread_id).first()
            if db_thread:
                db_thread.chat_id = chat_id
                db.commit()
                db.refresh(db_thread)
            return db_thread


# Удаление
def delete_thread(chat_id: int):
    with get_db() as db:
        with db.begin():
            db_thread = db.query(Thread).filter(Thread.chat_id == chat_id).first()
            if db_thread:
                db.delete(db_thread)
                db.commit()
            return db_thread
