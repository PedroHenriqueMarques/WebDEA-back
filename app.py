# app.py
# Author: Pedro Henrique Resende Marques
import os
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from flask_uploads import configure_uploads, patch_request_class
#from dotenv import load_dotenv


from db import db
from ma import ma
from blacklist import BLACKLIST

from resources.users import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from resources.tables import Table, UserTables
from resources.tableUpload import TableUpload
from libs.file_helper import FILE_SET

app = Flask(__name__)
cors = CORS(app)

app.config["CORS_HEADERS"] = "Content-Type"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]  # allow blacklisting for access and refresh tokens
app.secret_key = "Pedro"  # could do app.config['JWT_SECRET_KEY'] if we prefer
app.config["UPLOADED_TABLES_DEST"] = os.path.join("static", "tables")
patch_request_class(app, 10 * 1024 * 1024) #10MB max size upload
configure_uploads(app, FILE_SET)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):  # except ValidationError as err:
    return jsonify(err.messages), 400


jwt = JWTManager(app)

# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(Table, "/table/<string:name>")
api.add_resource(UserTables, "/tables/<string:user>")
api.add_resource(TableUpload, "/upload/table")


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)