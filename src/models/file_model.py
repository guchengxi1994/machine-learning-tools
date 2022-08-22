import hashlib
import os

from utils.db_utils import DATABASE, DBUtils
from PySide6 import QtSql


class File:
    def __init__(self, fileName: str, projectId: int) -> None:
        self.fileName = fileName
        self.md5 = ""
        self.fileSize = 0
        if os.path.exists(self.fileName):
            self.fileSize = os.path.getsize(self.fileName)
            with open(self.fileName, "rb") as f:
                self.md5 = hashlib.md5(f.read()).hexdigest()
        self.projectId = projectId

    def __eq__(self, __o: object) -> bool:
        if type(__o) is not self.__class__:
            return False
        return __o.fileName == self.fileName

    def __hash__(self) -> int:
        return hash(self.fileName)

    def dump(self) -> dict:
        with DBUtils() as db:
            query = QtSql.QSqlQuery(db=DATABASE)
            sql = """
            insert into file(file_md5,file_path,file_size,project_id) values("{}","{}",{},{})
            """.format(
                self.md5, self.fileName, self.fileSize, self.projectId
            )
            query.exec(sql)
        return {"filename": self.fileName, "md5": self.md5}

    @staticmethod
    def fromJson(s: dict):
        return File(fileName=s["filename"], projectId=s["projectId"])
