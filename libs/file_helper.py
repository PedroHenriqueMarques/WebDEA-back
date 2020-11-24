import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet

TABLES = tuple('csv xls xlsx'.split())

FILE_SET = UploadSet("tables", TABLES) # set name and allowed extensions


def save_table(table: FileStorage, folder: str=None, name: str=None) -> str:
    """Takes FileStorage and saves it to a folder."""
    return FILE_SET.save(table, folder, name)

def get_path(filename: str=None, folder: str=None) -> str:
    """Take table name and folder and return full path."""
    return FILE_SET.path(filename, folder)

def find_table_any_format(filename: str, folder: str) -> Union[str, None]:
    """Takes a filename and returns a table on any of the accepted formats."""
    for _format in TABLES:
        table = f"{filename}.{_format}"
        table_path = FILE_SET.path(filename=table, folder=folder)
        if os.path.isfile(table_path):
            return table_path
    return None

def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    """Take FileStorage and returns file name.
    Allows our functions to call this with both file names 
    and FileStorages and always gets back a file name.
    """
    if isinstance(file, FileStorage):
        return file.filename
    return file

def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    """Check our regex and return whether the string matches or not."""
    filename = _retrieve_filename(file)
    allowed_format = "|".join(TABLES) # xls|xlsx|csv
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None

def get_basename(file: Union[str, FileStorage]) -> str:
    """Return full name of table in the path
    get_basename("some/folder/table.xlsx") returns 'table.xlsx'
    """
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]

def get_filename(file: Union[str, FileStorage]) -> str:
    """Return file extension
    get_extension('table.xls') returns 'table'
    """
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[0]

def get_extension(file: Union[str, FileStorage]) -> str:
    """Return file extension
    get_extension('table.xls') returns '.xls'
    """
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]