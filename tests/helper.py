from typing import Optional

from redbaron.redbaron import RedBaron

import pytest
from src.process_file import ProcessPythonFileBase


def get_stub_process_python_file(expected):
    """
    Helper method to inject expected results into stub of ProcessPythonFile
    """

    class StubProcessPythonFile(ProcessPythonFileBase):
        def __init__(self, file_path: str) -> None:
            super().__init__(file_path)
            self._red_baron_object: Optional[RedBaron] = None

        @property
        def red_baron_object(self) -> Optional[RedBaron]:
            return super().red_baron_object

        def read_file(self) -> None:
            return super().read_file()

        def write_file(self, code_object: RedBaron) -> None:
            # Replace write_file functionality with transformation validation,
            # as saving back to the file would require additional cleanup to
            # restore changes made.
            transformation_type = expected.get("transformation_type")
            if transformation_type and transformation_type == "assignment":
                assert str(code_object.assignment.value) == str(
                    expected.get("redbaron_object").assignment.value
                )
            elif transformation_type and transformation_type == "kwargs":
                ...

    return StubProcessPythonFile


def check_exception(expected, func):
    """
    Check that an exception is raised when passed in through parametrized pytest
    run
    """
    if type(expected) == type and issubclass(expected, Exception):
        # Verify
        with pytest.raises(expected):
            func()
    else:
        func()
