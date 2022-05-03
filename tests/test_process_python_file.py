from redbaron.redbaron import RedBaron

from src.process_file import ProcessPythonFile

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
