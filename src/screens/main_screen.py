import sys

sys.path.append("..")
from typing import List

from components.custom_button import CustomButton
from components.file_management_widget import FileManagementWidget
from components.toaster import QToaster
from constants import *
from models import *
from PySide6 import QtCore
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QInputDialog,
)
from utils.new_project import create_new_project

from screens.project_management_screen import ProjectManagementScreen
from screens.sub_folder_screen import SubFolderScreen


class MainScreen(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        ## 读取结构
        self.__loading_folder()
        ## 记录访问过的Folder
        self.folderList: List[Folder] = []
        self.folderList.append(self.folder)

        ## 在这里写`show()` 方法，主要是因为在main函数里写的话任务栏图标会丢失
        self.show()
        self.setWindowTitle(APP_TITLE)
        self.setWindowIcon(QIcon(APP_ICON))
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        layout = QHBoxLayout()

        self.__build_menubar()
        self.__build_left_side_toolbar()

        stackLayout = QStackedLayout()
        self.fileManagementWidget = FileManagementWidget(self, canNavigate=True)
        self.fileManagementWidget.navigateSingal.connect(self.__handle_navigate)
        stackLayout.addWidget(self.fileManagementWidget)

        layout.addLayout(self.leftSideToolbar)
        layout.addLayout(stackLayout)
        layout.setAlignment(QtCore.Qt.AlignTop)

        ## 窗口主体
        mainWidget = QWidget()
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

    def __loading_folder(self):
        self.folder = load_structure_file(STRUCTURE_FILE_PATH)

    def __build_left_side_toolbar(self):
        self.leftSideToolbar = QVBoxLayout()
        self.openFileButton = CustomButton("Add File", ADD_FILE_ICON)
        self.openFileButton.clicked.connect(self.__open_file_func)

        self.backButton = CustomButton("Back", BACK_ICON)
        self.backButton.clicked.connect(self.__prev_func)

        self.saveButton = CustomButton("Save", SAVE_ICON)
        self.saveButton.clicked.connect(self.__save_file)

        self.leftSideToolbar.addWidget(self.openFileButton)
        self.leftSideToolbar.addWidget(self.backButton)
        self.leftSideToolbar.addWidget(self.saveButton)
        self.leftSideToolbar.setAlignment(QtCore.Qt.AlignTop)

    def __prev_func(self):
        if len(self.folderList) == 1:
            return
        else:
            self.folderList.pop()
            # self.folder = self.folderList[-1]
            self.fileManagementWidget.repaintByParent()

    def __open_file_func(self):
        filename, _ = QFileDialog.getOpenFileName(self, "选择文件", "./")
        if filename != "":
            self.folderList[-1].append(File(filename))
            self.fileManagementWidget.repaintByParent()

    def __save_file(self):
        d = self.folder.dump()
        # print(d)
        with open(STRUCTURE_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=" ")

        QToaster.showMessage(
            self,
            "保存成功",
            timeout=1000,
            windowWidth=self.width(),
            windowHeight=self.height(),
        )

    def __build_menubar(self):
        menubar = self.menuBar()
        sysMenu = menubar.addMenu("&System")

        ## 创建新项目功能
        createProjectAction = QAction("New Project", self)
        createProjectAction.setStatusTip("Create a new project")
        createProjectAction.triggered.connect(self.__create_new_project)
        sysMenu.addAction(createProjectAction)

        ## 管理所有项目功能
        manageProjectAction = QAction("Project Management", self)
        manageProjectAction.setStatusTip("Manage all projects")
        manageProjectAction.triggered.connect(self.__open_project_management_screen)
        sysMenu.addAction(manageProjectAction)

        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exit application")
        exitAction.triggered.connect(self.close)
        sysMenu.addAction(exitAction)

    def __open_project_management_screen(self):
        d = ProjectManagementScreen()
        d.exec()
        print(d.nextStructurePath)

        if d.nextStructurePath != "":
            with open(CONSTANTS_LAST_EDIT_PROJECT, "w") as f:
                f.write(d.nextStructurePath)
            self.folder = load_structure_file(d.nextStructurePath)
            self.folderList.clear()
            self.folderList.append(self.folder)
            self.fileManagementWidget.repaintByParent()

    def __handle_navigate(self, info: Folder):
        # print(info)
        s = SubFolderScreen(info)
        s.show()

    def __create_new_project(self):
        text, ok = QInputDialog.getText(self, "输入项目名称", "输入")
        if ok and text is not None and text != "":
            create_new_project(text)
