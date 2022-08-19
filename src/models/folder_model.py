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

    def remove(self, f: object):
        if type(f) is File or type(f) is self.__class__:
            if f in self.children:
                self.children.remove(f)

    def dump(self) -> dict:
        base = {"folderName": self.folderName, "children": []}

        for i in self.children:
            base["children"].append(i.dump())

        return base

    @staticmethod
    def fromJson(s: dict):
        f = Folder(s["folderName"], [])
        for i in s["children"]:
            if i.get("children") is not None:
                f.append(Folder.fromJson(i))
            else:
                f.append(File.fromJson(i))
        return f
