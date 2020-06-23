from ..models.db import db


class DAO:
    def __init__(self, obj: object):
        self.obj = obj
        self.session = db.session

    def get(self) -> object:
        pass

    def update(self) -> object:
        try:
            self.session.add(self.obj)
            self.session.commit()
            return self.obj
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self) -> bool:
        try:
            self.session.delete(self.obj)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e

    def insert(self) -> object:
        try:
            self.session.add(self.obj)
            self.session.commit()
            return self.obj
        except Exception as e:
            self.session.rollback()
            raise e
