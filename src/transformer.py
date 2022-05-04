from abc import ABC, abstractmethod
from typing import Dict, Union

from redbaron.nodes import AssignmentNode, CallArgumentNode
from redbaron.redbaron import RedBaron

from src.exceptions import (
    AssignmentValueNotFound,
    AssignmentValueUpdateError,
    KwargsValueUpdateError,
    ParentNotFound,
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
        redbaron_object: RedBaron,
        find: str,
        change_to: str,
    ) -> None:
        """
        Transforms a value within the RedBaron object
        Args:
            redbaron_object: RedBaron object which code transformations is
            done to
            find: Value to find within the Python code
            change_to: Value to update the found value to
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
        redbaron_object: RedBaron = self.processor.red_baron_object
        for key, value in self.values.items():
            self._transform_value(
                redbaron_object=redbaron_object,
                to_find=key,
                change_to=value,
            )
        self.processor.write_file(redbaron_object)

    def _transform_value(
        self,
        redbaron_object: RedBaron,
        to_find: str,
        change_to: Union[str, int],
    ) -> None:
        assignment = self.__find_value(
            redbaron_object=redbaron_object,
            to_find=to_find,
        )
        try:
            if isinstance(change_to, str):
                assignment.value = f"'{change_to}'"
            elif isinstance(change_to, int):
                assignment.value = f"{change_to}"
            else:
                # TODO:
                # Cleanup handling of different instance types
                raise NotImplementedError(
                    "Altering other types of values is not yet supported"
                )
        except Exception:
            raise AssignmentValueUpdateError("Error setting assignment value")

    def __find_value(
        self,
        redbaron_object: RedBaron,
        to_find: str,
    ) -> AssignmentNode:
        try:
            assignment: AssignmentNode = redbaron_object.find(
                "assignment",
                target=lambda x: x.dumps() == to_find,
            )
            return assignment
        except Exception:
            raise AssignmentValueNotFound(f"Unable to find {to_find}!")


class KwargsValueTransformer(ValueTransformerBase):
    def __init__(
        self,
        processor: ProcessPythonFileBase,
        values: Dict[str, str],
    ) -> None:
        super().__init__(processor, values)

    def run(self) -> None:
        self.processor.read_file()
        redbaron_object: RedBaron = self.processor.red_baron_object
        for key, value in self.values.items():
            self._transform_value(
                redbaron_object=redbaron_object,
                to_find=key,
                change_to=value,
            )
        self.processor.write_file(redbaron_object)

    def _transform_value(
        self,
        redbaron_object: RedBaron,
        to_find: str,
        change_to: Union[str, int],
    ) -> None:
        parent = self.__get_kwarg_parent(
            redbaron_object=redbaron_object,
            to_find=to_find,
        )
        try:
            if isinstance(change_to, str):
                parent.value = f"'{change_to}'"
            elif isinstance(change_to, int):
                parent.value = f"{change_to}"
            else:
                raise NotImplementedError(
                    "Altering other types of values is not yet supported"
                )
        except Exception:
            raise KwargsValueUpdateError("Error setting assignment value")

    def __get_kwarg_parent(
        self,
        redbaron_object: RedBaron,
        to_find: Union[str, int],
    ) -> CallArgumentNode:
        try:
            # God this is bad, but its the only way I could get it to work with
            # multiple cases of the kwarg key existing in the same file.

            # If you know for sure that there is just a single kwarg with the
            # key to_change in the entire file then:
            # parent = red_object.find("name",value=to_change).parent
            # would be sufficient
            for node in redbaron_object.find_all("name", to_find):
                if call_arg := node.parent.call_argument:
                    if call_arg_str := call_arg.string:
                        if call_arg_parent := call_arg_str.parent:
                            return call_arg_parent
        except AttributeError:
            raise ParentNotFound(f"Parent of {to_find} was not found")
