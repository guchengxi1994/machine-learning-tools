from PySide6.QtWidgets import QDialog, QVBoxLayout
from PySide6 import QtSql
from PySide6.QtGui import QIcon
from components.table_widget import ProjectTableWidget

from constants import APP_ICON, PROJECT_MANAGEMENT, CONSTANTS_DB_PATH


class ProjectManagementScreen(QDialog):
    def __init__(self,) -> None:
        super().__init__()
        self.database = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName(CONSTANTS_DB_PATH)
        self.database.open()
        __result = self.__load_data()
        self.setWindowTitle(PROJECT_MANAGEMENT)
        self.setWindowIcon(QIcon(APP_ICON))
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        # print(__result)
        content = ProjectTableWidget(__result)
        __layout = QVBoxLayout()
        __layout.addWidget(content)
        self.setLayout(__layout)

    def __load_data(self):
        query = QtSql.QSqlQuery()
        select_sql = """
        select project_id,project_name,project_file_path,update_at,create_at,is_deleted from project
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
                ]
            )
        return result

    def close(self) -> bool:
        self.database.close()
        return super().close()
