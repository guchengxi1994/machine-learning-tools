import os
import yaml

CONSTANTS_FILE_PATH = "_private/constants.yaml"
STRUCTURE_FILE_PATH = ""
APP_ICON = ""
BACK_ICON = ""
SAVE_ICON = ""
FILE_ICON = ""
FOLDER_ICON = ""
ADD_FILE_ICON = ""
DELETE_ICON = ""
FORMAT_ICON = ""
CREATE_FOLDER_ICON = ""
APP_TITLE = ""


if not os.path.exists(CONSTANTS_FILE_PATH):
    print("constants.yaml not found")
else:
    with open(CONSTANTS_FILE_PATH, "r", encoding="utf-8") as f:
        yamlData = yaml.load(f.read(), Loader=yaml.FullLoader)
        STRUCTURE_FILE_PATH = yamlData["structure"]
        APP_ICON = yamlData["icons"]["app_icon"]
        BACK_ICON = yamlData["icons"]["back"]
        SAVE_ICON = yamlData["icons"]["save"]
        FILE_ICON = yamlData["icons"]["file"]
        FOLDER_ICON = yamlData["icons"]["folder"]
        ADD_FILE_ICON = yamlData["icons"]["add_file"]
        DELETE_ICON = yamlData["icons"]["delete"]
        FORMAT_ICON = yamlData["icons"]["format"]
        CREATE_FOLDER_ICON = yamlData["icons"]["create_folder"]
        APP_TITLE = yamlData["strings"]["app_title"]
