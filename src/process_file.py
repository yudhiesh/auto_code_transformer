from typing import Optional
from redbaron import RedBaron


class ProcessPythonFile:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self._red_baron_object: Optional[RedBaron] = None

    @property
    def red_baron_object(self) -> RedBaron:
        if self._red_baron_object:
            return self._red_baron_object
        else:
            raise AttributeError(
                "Run read_file() first before accessing red_baron_object"
            )

    def read_file(self) -> None:
        try:
            with open(self.file_path, "r") as source_code:
                self._red_baron_object = RedBaron(source_code.read())
        except Exception as e:
            raise e

    def write_file(self, code_object: RedBaron) -> None:
        try:
            with open(self.file_path, "w") as source_code:
                source_code.write(code_object.dumps())
        except Exception as e:
            raise e
