from PySide6 import QtSql

from utils.db_utils import DATABASE, DBUtils


def get_project_path(projectId: int):
    with DBUtils() as db:
        query = QtSql.QSqlQuery(db=DATABASE)
        select_sql = """
            select project_file_path from project where project_id = {} and is_deleted=0
        """.format(
            projectId
        )

        result = []
        query.prepare(select_sql)
        query.exec()

        while query.next():
            result.append(query.value(0))
        # print(result)
        if len(result) == 0:
            return ""
        else:
            return result[0]
