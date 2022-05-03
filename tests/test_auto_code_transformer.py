from redbaron.redbaron import RedBaron

import pytest
from src.exceptions import AssignmentValueUpdateError, ParentNotFound
from src.transformer import AssignmentValueTransformer, KwargsValueTransformer
from tests.helper import get_stub_process_python_file, check_exception


@pytest.mark.parametrize(
    "values,file_path,expected",
    [
        (
            {"": ""},
            "./staticdata/assignments.py",
            AssignmentValueUpdateError,
        ),
        (
            {"FILE_NAME": "test.py", "NUM_EPOCHS": 20},
            "./staticdata/assignments.py",
            dict(
                redbaron_object=RedBaron(
                    """FILE_NAME = 'test.py'
                    NUM_EPOCHS = 20
                """
                ),
                transformation_type="assignment",
            ),
        ),
        (
            {"file_name": "test.py", "num_epochs": 20},
            "./staticdata/assignments.py",
            AssignmentValueUpdateError,
        ),
    ],
)
def test_assignment_value_transformer(values, file_path, expected):
    StubProcessPythonFile = get_stub_process_python_file(expected=expected)
    py_file_processor = StubProcessPythonFile(file_path=file_path)
    assignment_value_transformer = AssignmentValueTransformer(
        processor=py_file_processor,
        values=values,
    )
    check_exception(expected, assignment_value_transformer.run)


@pytest.mark.parametrize(
    "values,file_path,expected",
    [
        (
            {"": ""},
            "./staticdata/assignments.py",
            ParentNotFound,
        )
    ],
)
def test_kwargs_value_transformer(values, file_path, expected):
    StubProcessPythonFile = get_stub_process_python_file(expected=expected)
    py_file_processor = StubProcessPythonFile(file_path=file_path)
    kwargs_value_transformer = KwargsValueTransformer(
        processor=py_file_processor,
        values=values,
    )
    check_exception(expected, kwargs_value_transformer.run)
