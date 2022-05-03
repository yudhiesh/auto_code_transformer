from typing import Optional

from redbaron.redbaron import RedBaron

import pytest
from src.exceptions import AssignmentValueNotFound
from src.process_file import ProcessPythonFileBase
from src.transformer import AssignmentValueTransformer


def get_stub_process_python_file(expected):
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
            assert str(code_object.assignment.value) == str(expected.assignment.value)

    return StubProcessPythonFile


def check_exception(expected, func):
    if type(expected) == type and issubclass(expected, Exception):
        # Verify
        with pytest.raises(expected):
            func()
    else:
        func()


@pytest.mark.parametrize(
    "values,file_path,expected",
    [
        (
            {"": ""},
            "./staticdata/assignments.py",
            AssignmentValueNotFound,
        ),
        (
            {"FILE_NAME": "test.py"},
            "./staticdata/assignments.py",
            RedBaron("FILE_NAME = 'test.py'"),
        ),
        (
            {"file_name": "test.py"},
            "./staticdata/assignments.py",
            AssignmentValueNotFound,
        ),
    ],
)
def test_assignment_value_transformer(values, file_path, expected):
    StubProcessPythonFile = get_stub_process_python_file(expected=expected)

    # Setup
    py_file_processor = StubProcessPythonFile(file_path=file_path)
    assignment_value_transformer = AssignmentValueTransformer(
        processor=py_file_processor,
        values=values,
    )
    check_exception(expected, assignment_value_transformer.run)
