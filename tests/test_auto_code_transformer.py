from click.testing import CliRunner
from redbaron.redbaron import RedBaron

import pytest
from src import cli
from src.exceptions import AssignmentValueNotFound
from src.process_file import ProcessPythonFile
from src.transformer import AssignmentValueTransformer

PRE_TRANSFORM_FILE_PATH = "./staticdata/example.py"
POST_TRANSFORM_FILE_PATH = "./staticdata/post_transform.py"


def test_read_python_file():
    py_file = ProcessPythonFile(file_path=PRE_TRANSFORM_FILE_PATH)
    py_file.read_file()
    assert py_file.red_baron_object
    assert isinstance(py_file.red_baron_object, RedBaron)


def test_write_python_file_transform_func_docstring_value():
    # Setup
    ALTERED_VALUE = '"4, 5, 6"'
    ORIGINAL_VALUE = (
        '"""TODO: Docstring for main.\n\n    :arg1: TODO\n    :returns: TODO\n\n    """'
    )

    # Exercise
    py_file_pre = ProcessPythonFile(file_path=PRE_TRANSFORM_FILE_PATH)
    py_file_pre.read_file()
    pre_transform_code_object = py_file_pre.red_baron_object
    pre_transform_code_object[0].string.value = ALTERED_VALUE
    py_file_pre.write_file(pre_transform_code_object)

    # Verify
    py_file_post = ProcessPythonFile(file_path=PRE_TRANSFORM_FILE_PATH)
    py_file_post.read_file()
    post_transform_code_object = py_file_post.red_baron_object
    assert post_transform_code_object[0].string.value == ALTERED_VALUE

    # Cleanup
    post_transform_code_object[0].string.value = ORIGINAL_VALUE
    py_file_post.write_file(post_transform_code_object)


@pytest.mark.parametrize(
    "values,file_path,expected",
    [
        (
            {"": ""},
            "./staticdata/assignments.py",
            AssignmentValueNotFound,
        )
    ],
)
def test_assignment_value_transformer(values, file_path, expected):
    # TODO:
    # mock ProcessPythonFile and replace red_baron_object
    # with test version
    # read_file() will set the object
    # write_file() does nothing
    # Setup
    py_file_processor = ProcessPythonFile(file_path=file_path)
    assignment_value_transformer = AssignmentValueTransformer(
        processor=py_file_processor,
        values=values,
    )
    # Exercise
    if type(expected) == type and issubclass(expected, Exception):
        # Verify
        with pytest.raises(expected):
            assignment_value_transformer.run()
    else:
        assignment_value_transformer.run()


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "auto_code_transformer.cli.main" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
