from sqlmodel import (
    SQLModel,
    create_engine,
    Session,
    Field,
    select,
)
from typing import Optional


database_file_name = "database.sqlite3"
engine = create_engine(f"sqlite:///{database_file_name}")


class Notes(SQLModel,table=True):
    id : Optional[int] = Field(primary_key=True,default=None,nullable=False)
    title : str = Field(nullable=False)
    note : str = Field(nullable=False)

    def add(self,title,note):
        new_note = Notes(title=title,note=note)
        with Session(engine) as session:
            session.add(new_note)
            session.commit()
            return True

    def update(self,id,title,note):
        with Session(engine) as session:
            statement = select(Notes).where(Notes.id == id)
            results = session.exec(statement)
            old_note = results.one()
            old_note.title = title
            old_note.note = note
            session.add(old_note)
            session.commit()
            return True

    def get_all(self):
        with Session(engine) as session:
            statement = select(Notes)
            results = session.exec(statement)
            return results.all()

    def get_by_id(self,id):
        with Session(engine) as session:
            statement = select(Notes).where(Notes.id == id)
            results = session.exec(statement)
            return results.first()

    def delete(self,id):
        with Session(engine) as session:
            statement = select(Notes).where(Notes.id == id)
            results = session.exec(statement).first()
            session.delete(results)
            session.commit()
            return True



def create_tables():
    SQLModel.metadata.create_all(engine)
