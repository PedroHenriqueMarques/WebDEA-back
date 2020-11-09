from ma import ma
from models.users import UserModel
from models.tables import TableModel
from schemas.table import TableSchema

class UserSchema(ma.SQLAlchemyAutoSchema):
    tables = ma.Nested(TableSchema, many=True)

    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        load_instance = True
