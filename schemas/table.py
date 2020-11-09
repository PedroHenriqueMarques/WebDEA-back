from ma import ma
from models.tables import TableModel
from models.users import UserModel


class TableSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TableModel
        include_fk = True
        load_instance = True