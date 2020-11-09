from typing import List

from db import db


class TableModel(db.Model):
    __tablename__ = "user_tables"

    Id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey("users.Id"), nullable=False)
    table_name = db.Column(db.String(50), nullable=False)
    table = db.Column(db.Text, nullable=False)

    @classmethod
    def find_by_user_id(cls, _id: int) -> "TableModel":
        return cls.query.filter_by(Id=_id).all()

    @classmethod
    def find_by_table_name(cls, name: str) -> "TableModel":
        return cls.query.filter_by(table_name=name).first()

    @classmethod
    def find_all_user_tables_names(cls, user_id: int) -> List:
        return db.session.query(TableModel.table_name).filter(TableModel.userId==user_id).all()

    @classmethod
    def find_by_table_id(cls, _id: int) -> "TableModel":
        return cls.query.filter_by(Id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()