import json
from flask import request
from flask_restful import Resource
from libs.DEAmodels.ioccr import solveIoccr
from models.tables import TableModel
from schemas.table import TableSchema

TABLE_NOT_FOUND = "Table not found."
FAILED_TO_SOLVE_IOCCR = "Failed to solve table {} with IOCCR."

table_schema = TableSchema()


class DeaIoccr(Resource):
    @classmethod
    def get(cls, tableName: str):
        table = TableModel.find_by_table_name(tableName)
        if not table:
            return {"message": TABLE_NOT_FOUND}, 404
        table_json = table_schema.dump(table)
        #table_json = json.loads(table_json['table'])
        tb = json.loads(json.loads(table_json['table']))
        table_json['table'] = tb
        #return table_json
        sol = solveIoccr(table_json)
        #return x,y
        if sol['status'] == 'Success':
            return sol, 200
        elif sol['status'] == 'Failed':
            return {"message": FAILED_TO_SOLVE_IOCCR.format(tableName)}, 200
        else:
            return {"message": "error unknown."}, 500

    @classmethod
    def post(cls, tableName: str):
        pass