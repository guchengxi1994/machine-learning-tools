from PySide6 import QtSql
from constants import CONSTANTS_DB_PATH

DATABASE = QtSql.QSqlDatabase("QSQLITE")
if not DATABASE.contains("QSQLITE"):
    DATABASE = QtSql.QSqlDatabase().addDatabase("QSQLITE")


class DBUtils:
    def __init__(self) -> None:
        # self.database = QtSql.QSqlDatabase("QSQLITE")
        # if not self.database.contains("QSQLITE"):
        #     self.database = QtSql.QSqlDatabase().addDatabase("QSQLITE")
        DATABASE.setDatabaseName(CONSTANTS_DB_PATH)
        DATABASE.open()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        DATABASE.close()
        print("关闭数据库连接")
