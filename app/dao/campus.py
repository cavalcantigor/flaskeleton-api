from ..models.campus import Campus
from . import DAO


class CampusDAO(DAO):
    def __init__(self, campus: Campus = None):
        super().__init__(campus)

    def get_all(self) -> list or Campus:
        return self.session.query(Campus).all()

    def get(self) -> list or Campus:
        self.obj = (
            self.session.query(Campus)
            .filter_by(codigo=self.obj.codigo)
            .first()
        )
        return self.obj
