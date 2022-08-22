import json
import uuid

from utils.db_utils import DATABASE, DBUtils
from PySide6 import QtSql


def create_new_project(projectName: str):
    randomUUID = uuid.uuid4()
    filename = str(randomUUID) + ".json"
    filepath = "_private/" + filename

    with open(filepath, "w") as f:
        json.dump({}, f)

    with DBUtils() as db:
        query = QtSql.QSqlQuery(db=DATABASE)
        # print(db.database.isOpen())
        select_sql = """
        select project_id,project_name from project where project_name = "{}"
        """.format(
            projectName
        )
        result = 0
        query.prepare(select_sql)
        query.exec()

        while query.next():
            result += 1

        if result == 0:
            query.exec(
                """
                insert into project(project_name,project_file_path) values("{}","{}")
                """.format(
                    projectName, filepath
                )
            )
