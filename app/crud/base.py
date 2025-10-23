from typing import Type, TypeVar, List
from sqlmodel import Session, SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)

class CRUDBase:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_all(self, session: Session) -> List[ModelType]:
        return session.exec(select(self.model)).all()

    def get(self, session: Session, id: int) -> ModelType | None:
        return session.get(self.model, id)

    def create(self, session: Session, obj: ModelType) -> ModelType:
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def delete(self, session: Session, id: int) -> bool:
        db_obj = session.get(self.model, id)
        if db_obj:
            session.delete(db_obj)
            session.commit()
            return True
        return False
