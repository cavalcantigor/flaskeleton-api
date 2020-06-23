from .db import ma


class ManagedSchema(ma.SQLAlchemySchema):
    def update(self, obj, data):
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))
