class File:
    def __init__(self, fileName: str) -> None:
        self.fileName = fileName

    def __eq__(self, __o: object) -> bool:
        if type(__o) is not self.__class__:
            return False
        return __o.fileName == self.fileName

    def __hash__(self) -> int:
        return hash(self.fileName)

    def dump(self) -> dict:
        return {"filename": self.fileName}
    
    @staticmethod
    def fromJson(s:dict):
        return File(fileName=s["filename"])
