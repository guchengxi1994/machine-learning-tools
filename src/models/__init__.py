import json
import os

from PySide6 import QtSql
from .file_model import File
from .folder_model import Folder
from constants import CONSTANTS_DB_PATH


def init_DB():
    if not os.path.exists(CONSTANTS_DB_PATH):
        database = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        database.setDatabaseName(CONSTANTS_DB_PATH)
        database.open()
        query = QtSql.QSqlQuery()
        query.exec(
            """
        CREATE TABLE "project" (
            "project_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "project_name" TEXT,
            "project_file_path" TEXT,
            "update_at" TEXT DEFAULT CURRENT_TIMESTAMP,
            "create_at" TEXT DEFAULT CURRENT_TIMESTAMP,
            "is_deleted" integer DEFAULT 0
        )
        """
        )
        query.exec(
            """
            insert into project(project_name,project_file_path) values("测试项目","_private/structure.json")
            """
        )
        database.close()


def load_structure_file(filePath: str) -> Folder:
    if os.path.exists(filePath):
        jsonStructure = json.load(open(filePath, "r", encoding="utf-8"))
    else:
        jsonStructure = {}
    # print(jsonStructure)
    if jsonStructure == {}:
        return Folder("root", [])
    else:
        # return Folder("root", [])
        return Folder.fromJson(jsonStructure)
