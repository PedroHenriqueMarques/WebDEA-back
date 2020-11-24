
from pandas import read_csv, read_excel

from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request, json
from flask_jwt_extended import jwt_required, get_jwt_identity

from libs import file_helper
from models.tables import TableModel
from models.users import UserModel
from schemas.table import TableSchema
from schemas.tableUpload import FileTableSchema

FILE_UPLOADED = "File '{}' uploaded."
FILE_ILLEGAL_EXTENSION = "Extension '{}' is not allowed."
TABLENAME_ALREADY_EXISTS = "A Table with name '{}' already exists."


table_schema = TableSchema()
file_table_schema = FileTableSchema()

class TableUpload(Resource):
    @jwt_required
    def post(self):
        """
        Used to upload a table file.
        It (should) uses JWT to retrieve user information and then saves 
        the table to the user's folder.
        If there is a filename conflict, it appends a number to the end.
        """
        data = file_table_schema.load(request.files) # {"table": FileStorage}
        user_id = get_jwt_identity()
        #folder = f"user_{user_id}" #static/tables/user_1
        table_name = file_helper.get_filename(data["table"])

        if TableModel.find_by_table_name(table_name):
            return {"message": TABLENAME_ALREADY_EXISTS.format(table_name)}, 400
        
        if file_helper.get_extension(data["table"]) == '.csv':
            data_df = read_csv(data["table"])
        else:
            data_df = read_excel(data["table"])
        
        table_json = data_df.to_json()

        table_data = {}
        table_data["table_name"] = table_name
        table_data["userId"] = user_id
        table_data["table"] = json.dumps(table_json)

        table = table_schema.load(table_data)

        try:
            table.save_to_db()
            #table_path = file_helper.save_table(data["table"], folder=folder)
            #basename = file_helper.get_basename(table_path)
            #return {"message": FILE_UPLOADED.format(basename)}, 201
            return table_schema.dump(table)
        
        except UploadNotAllowed:
            extension = file_helper.get_extension(data["table"])
            return {"message": FILE_ILLEGAL_EXTENSION.format(extension)}, 400
            