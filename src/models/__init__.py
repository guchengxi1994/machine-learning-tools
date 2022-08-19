import json
import os

from .file_model import File
from .folder_model import Folder


def load_structure_file(filePath: str) -> Folder:
    if os.path.exists(filePath):
        jsonStructure = json.load(open(filePath, "r", encoding="utf-8"))
    else:
        jsonStructure = {}
    # print(jsonStructure)
    if jsonStructure == {}:
        return Folder("root", [])
    else:
        # return Folder("root", [])
        return Folder.fromJson(jsonStructure)

