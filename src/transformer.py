from abc import ABC, abstractmethod
from typing import Dict

from redbaron.redbaron import RedBaron

from src.exceptions import (
    AssignmentValueNotFound,
    AssignmentValueUpdateError,
    TransformationFailed,
)
from src.process_file import ProcessPythonFileBase


class ValueTransformerBase(ABC):
    """Base class for performing code transformations using RedBaron"""

    def __init__(
        self,
        processor: ProcessPythonFileBase,
        values: Dict[str, str],
    ) -> None:
        self.processor = processor
        self.values = values

    @abstractmethod
    def run(self) -> None:
        """
        Main function to run the entire transformation
        """

    @abstractmethod
    def _transform_value(
        self,
        red_object: RedBaron,
        find: str,
        change_to: str,
    ) -> None:
        """
        Transforms a value within the RedBaron object
        Args:
            red_object: RedBaron object which code transformations is
            done to
            find: Value to find within the Python code
            to_change: Value to update the found value to
        """

    @abstractmethod
    def _is_transformation_valid(self) -> bool:
        """
        Validate transformation done by _transform_value()
        """


class AssignmentValueTransformer(ValueTransformerBase):
    """
    Transforms assignments value within a file_name
    """

    def __init__(
        self,
        processor: ProcessPythonFileBase,
        values: Dict[str, str],
    ) -> None:
        super().__init__(
            processor,
            values,
        )

    def run(self):
        self.processor.read_file()
        redbaron_object = self.processor.red_baron_object
        for key, value in self.values.items():
            self._transform_value(
                redbaron_object=redbaron_object,
                find=key,
                to_change=value,
            )
            if not self._is_transformation_valid():
                raise TransformationFailed(f"Transforming {key=} to {value=}")
        self.processor.write_file(redbaron_object)

    def _transform_value(
        self,
        redbaron_object: RedBaron,
        find: str,
        to_change: str,
    ) -> None:
        assignment = redbaron_object.find(
            "assignment",
            target=lambda x: x.dumps() == find,
        )
        if not assignment:
            raise AssignmentValueNotFound(f"Unable to find {to_change}!")
        try:
            assignment.value = f"'{to_change}'"
        except Exception:
            raise AssignmentValueUpdateError("Error setting assignment value")

    def _is_transformation_valid(self) -> bool:
        return True
