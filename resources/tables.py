from flask import request, json
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.tables import TableModel
from models.users import UserModel
from schemas.table import TableSchema

TABLE_NOT_FOUND = "Table not found."
TABLENAME_ALREADY_EXISTS = "A Table with name '{}' already exists."
ERROR_SAVING = "An error has occurred while saving the table."
TABLE_DELETED = "Table deleted."

table_schema = TableSchema()
user_tables_list_schema = TableSchema(many=True)

class Table(Resource):
    @classmethod
    def get(cls, name: str):
        table = TableModel.find_by_table_name(name)
        if not table:
            return {"message": TABLE_NOT_FOUND}, 404

        return table_schema.dump(table), 200
    
    @classmethod
    def post(cls, name: str):
        table_json = request.get_json()
        user_id = UserModel.find_by_username(table_json["username"]).Id

        if TableModel.find_by_table_name(name):
            return {"message": TABLENAME_ALREADY_EXISTS.format(name)}
        
        table_data = {}
        table_data["table_name"] = name
        table_data["userId"] = user_id
        table_data["table"] = json.dumps(table_json["table"])

        table = table_schema.load(table_data)

        try:
            table.save_to_db()
        except:
            return {"message": ERROR_SAVING}, 500

        return table_schema.dump(table)

    @classmethod
    def delete(cls, name: str):
        table = TableModel.find_by_table_name(name)
        
        if table:
            table.delete_from_db()
            return {"message": TABLE_DELETED}, 200
        
        return {"message": TABLE_NOT_FOUND}, 404

    @classmethod
    @jwt_required
    def put(cls, name: str):
        table_json = request.get_json()
        user_id = get_jwt_identity()
        table = TableModel.find_by_table_name(name)

        if table:
            table.table = json.dumps(table_json["table"])

        else:
            table_data = {}
            table_data["table_name"] = name
            table_data["userId"] = user_id
            table_data["table"] = json.dumps(table_json["table"])
            table = table_schema.load(table_data)


        try:
            table.save_to_db()
        except:
            return {"message": ERROR_SAVING}, 500

        return table_schema.dump(table), 200

    
class UserTables(Resource):
    @classmethod
    def get(cls, user: str):
        user_id = UserModel.find_by_username(user).Id
        tables = TableModel.find_all_user_tables_names(user_id)

        for table in range(len(tables)):
            tables[table] = tables[table][0]

        return {"tables": tables}
        