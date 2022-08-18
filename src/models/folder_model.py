from typing import List

from .file_model import File


class Folder:
    def __init__(self, folderName: str, children: List[object]) -> None:
        self.folderName = folderName
        self.children = children

    def __eq__(self, __o: object) -> bool:
        if type(__o) is not self.__class__:
            return False
        return __o.folderName == self.folderName

    def __hash__(self) -> int:
        return hash(self.folderName)

    def append(self, f: object):
        if type(f) is File or type(f) is self.__class__:
            if f not in self.children:
                self.children.append(f)
