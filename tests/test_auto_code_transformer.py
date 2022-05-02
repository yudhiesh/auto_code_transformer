#!/usr/bin/env python

"""Tests for `auto_code_transformer` package."""


from click.testing import CliRunner
from redbaron.redbaron import RedBaron

from src.auto_code_transformer import ProcessPythonFile
from src import cli

PRE_TRANSFORM_FILE_PATH = "./staticdata/example.py"
POST_TRANSFORM_FILE_PATH = "./staticdata/post_transform.py"


def test_read_python_file():
    py_file = ProcessPythonFile(file_path=PRE_TRANSFORM_FILE_PATH)
    py_file.read_file()
    assert py_file.code_object
    assert isinstance(py_file.code_object, RedBaron)


def test_write_python_file_transform_func_docstring_value():
    # Setup
    ALTERED_VALUE = '"4, 5, 6"'
    ORIGINAL_VALUE = (
        '"""TODO: Docstring for main.\n\n    :arg1: TODO\n    :returns: TODO\n\n    """'
    )
    # Exercise
    py_file_pre = ProcessPythonFile(file_path=PRE_TRANSFORM_FILE_PATH)
    py_file_pre.read_file()
    pre_transform_code_object = py_file_pre.code_object
    pre_transform_code_object[0].string.value = ALTERED_VALUE
    py_file_pre.write_file(pre_transform_code_object)

    # Verify
    py_file_post = ProcessPythonFile(file_path=PRE_TRANSFORM_FILE_PATH)
    py_file_post.read_file()
    post_transform_code_object = py_file_post.code_object
    assert post_transform_code_object[0].string.value == ALTERED_VALUE

    # Cleanup
    post_transform_code_object[0].string.value = ORIGINAL_VALUE
    py_file_post.write_file(post_transform_code_object)


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "auto_code_transformer.cli.main" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
