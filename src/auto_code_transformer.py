from typing import Optional
from redbaron import RedBaron


class ProcessPythonFile:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self._code_object: Optional[RedBaron] = None

    @property
    def code_object(self) -> RedBaron:
        return self._code_object

    def read_file(self) -> None:
        try:
            with open(self.file_path, "r") as source_code:
                self._code_object = RedBaron(source_code.read())
        except Exception as e:
            raise e

    def write_file(self, code_object: RedBaron) -> None:
        try:
            with open(self.file_path, "w") as source_code:
                source_code.write(code_object.dumps())
        except Exception as e:
            raise e
