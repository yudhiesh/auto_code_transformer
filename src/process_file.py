from abc import ABC, abstractmethod
from typing import Optional

from redbaron import RedBaron


class ProcessPythonFileBase(ABC):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self._red_baron_object: Optional[RedBaron] = None

    @property
    @abstractmethod
    def red_baron_object(self) -> Optional[RedBaron]:
        """
        Returns the red baron object property
        """
        if self._red_baron_object:
            return self._red_baron_object
        raise AttributeError("Run read_file() first before accessing red_baron_object")

    @abstractmethod
    def read_file(self) -> None:
        """
        Reads the file and sets the Red Baron object
        """
        try:
            with open(self.file_path, "r") as source_code:
                self._red_baron_object = RedBaron(source_code.read())
        except Exception as e:
            raise e

    @abstractmethod
    def write_file(self, code_object: RedBaron) -> None:
        """
        Writes the file with the updated Red Baron object
        """
        try:
            with open(self.file_path, "w") as source_code:
                source_code.write(code_object.dumps())
        except Exception as e:
            raise e


class ProcessPythonFile(ProcessPythonFileBase):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._red_baron_object: Optional[RedBaron] = None

    @property
    def red_baron_object(self) -> Optional[RedBaron]:
        return super().red_baron_object

    def read_file(self) -> None:
        return super().read_file()

    def write_file(self, code_object: RedBaron) -> None:
        return super().write_file(code_object)
