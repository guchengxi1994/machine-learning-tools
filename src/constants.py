import os
import yaml

CONSTANTS_FILE_PATH = "_private/constants.yaml"
CONSTANTS_DB_PATH = "_private/db.db"
CONSTANTS_DB_NAME = "db.db"
CONSTANTS_LAST_EDIT_PROJECT = "_private/LASTEDITPROJECT"
STRUCTURE_FILE_PATH = ""
APP_ICON = ""
BACK_ICON = ""
SAVE_ICON = ""
FILE_ICON = ""
FILE_SELECTED_ICON = ""
FOLDER_ICON = ""
FOLDER_SELECTED_ICON = ""
ADD_FILE_ICON = ""
NAVIGATE_ICON = ""
DELETE_ICON = ""
FORMAT_ICON = ""
SECOND_MENU_ICON = ""
TXT_ICON = ""
VSCODE_ICON = ""
TYPORA_ICON = ""
CREATE_FOLDER_ICON = ""
APP_TITLE = ""
PROJECT_MANAGEMENT = "Project management"


if not os.path.exists(CONSTANTS_FILE_PATH):
    print("constants.yaml not found")
else:
    with open(CONSTANTS_FILE_PATH, "r", encoding="utf-8") as f:
        yamlData = yaml.load(f.read(), Loader=yaml.FullLoader)
        _lastEditPath = yamlData["structure"]
        with open(_lastEditPath, "r") as l:
            r = l.readlines()[0]
        STRUCTURE_FILE_PATH = r

        APP_ICON = yamlData["icons"]["app_icon"]
        BACK_ICON = yamlData["icons"]["back"]
        SAVE_ICON = yamlData["icons"]["save"]
        FILE_ICON = yamlData["icons"]["file"]
        FILE_SELECTED_ICON = yamlData["icons"]["file_selected"]
        FOLDER_ICON = yamlData["icons"]["folder"]
        FOLDER_SELECTED_ICON = yamlData["icons"]["folder_selected"]
        ADD_FILE_ICON = yamlData["icons"]["add_file"]
        DELETE_ICON = yamlData["icons"]["delete"]
        FORMAT_ICON = yamlData["icons"]["format"]
        NAVIGATE_ICON = yamlData["icons"]["navigate"]
        SECOND_MENU_ICON = yamlData["icons"]["second"]
        TXT_ICON = yamlData["icons"]["txt"]
        VSCODE_ICON = yamlData["icons"]["vscode"]
        TYPORA_ICON = yamlData["icons"]["typora"]
        CREATE_FOLDER_ICON = yamlData["icons"]["create_folder"]
        APP_TITLE = yamlData["strings"]["app_title"]
