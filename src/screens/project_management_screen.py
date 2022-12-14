from PySide6.QtWidgets import QDialog, QVBoxLayout
from PySide6 import QtSql
from PySide6.QtGui import QIcon
from components.table_widget import ProjectTableWidget

from constants import APP_ICON, PROJECT_MANAGEMENT
from utils.db_utils import DATABASE, DBUtils


class ProjectManagementScreen(QDialog):
    def __init__(self) -> None:
        super().__init__()
        __result = self.__load_data()
        self.setWindowTitle(PROJECT_MANAGEMENT)
        self.setWindowIcon(QIcon(APP_ICON))
        self.setMinimumWidth(1000)
        self.setMinimumHeight(600)
        # print(__result)
        content = ProjectTableWidget(__result)
        content.closeSignal.connect(self.__handle_open_project)
        __layout = QVBoxLayout()
        __layout.addWidget(content)
        self.setLayout(__layout)
        self.nextStructurePath = ""

    def __load_data(self):
        with DBUtils() as db:
            query = QtSql.QSqlQuery(db=DATABASE)
            # select_sql = """
            # select project_id,project_name,project_file_path,update_at,create_at,is_deleted from project
            # """
            select_sql = """
            SELECT
                p.project_id,
                p.project_name,
                p.project_file_path,
                p.create_at,
                p.update_at,
                COUNT( f.file_id ) as file_count,
                SUM( f.file_size ) as size_sum
            FROM
                project AS p
                LEFT JOIN file AS f ON p.project_id == f.project_id 
            WHERE
                p.is_deleted = 0 
                AND f.is_deleted = 0
            """
            result = []
            query.prepare(select_sql)
            query.exec()
            while query.next():
                result.append(
                    [
                        query.value(0),
                        query.value(1),
                        query.value(2),
                        query.value(3),
                        query.value(4),
                        query.value(5),
                        query.value(6),
                    ]
                )
            return result

    def close(self) -> bool:
        return super().close()

    def __handle_open_project(self, info):
        # print(info)
        self.nextStructurePath = info
        self.close()
