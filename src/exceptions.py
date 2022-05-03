class AssignmentValueNotFound(Exception):
    """Error thrown when the assignment value to update is not found within the Python code"""


class AssignmentValueUpdateError(Exception):
    """Error thrown when updating the assignment value fails"""


class ParentNotFound(Exception):
    """Error thrown when the parent of the kwarg value being updates is not
    found"""


class KwargsValueUpdateError(Exception):
    """Error thrown when updating the kwargs value fails"""
