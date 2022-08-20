import sys
from screens.main_screen import MainScreen
from PySide6.QtWidgets import QApplication
from models import init_DB

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.addLibraryPath("./plugins")
    init_DB()
    mainScreen = MainScreen()
    # mainScreen.show()

    sys.exit(app.exec())
