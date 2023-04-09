"""Implements abstract class for an interface to a CTA tool.

This file creates an abstraction for an automatic cell type annotation (CTA) tool. You can import
`macta.tools.CTAToolInterface` and simply implement the `annotate`, `convert`, and `requirements` methods, and
optionally the `preprocess_expr`, and `preprocess_ref` methods to define most if not all CTA tools' behavior. After
these methods are defined, you can run the tool using the `run_full` method.

Typical usage example:

    Refer to the `_celltypeist_interface` method in the same directory as this file.
"""

# TODO #18 define typical usage in the above comment

from abc import ABC, abstractmethod
from anndata import AnnData
import pandas as pd
from typing import Any, Dict, Optional

from macta.utils import requirements as rqs

# #20 test this:
# ExpressionType = TypeVar('ExpressionType')
# ReferenceType = TypeVar('ReferenceType')


class CTAToolInterface(ABC):
    """Abstraction for a python interface to a cell type annotation (CTA) tool.

    Defines the logic surrounding running a CTA tool, while abstracting away the actual logic of the specific CTA code.
    A subclass of `CTAToolInterface` has to set the `requirements` property, implement the `annotate` and `convert`
    methods, and optionally also implement the `preprocess_expr` and `preprocess_ref` methods. Then, you can run the new
    class's `run_full` method to perform its cell type annotation analysis.

    Attributes:
        requirements (RequirementList): a requirement list that dictates how some of the arguments passed to this CTA
            tool should appear/behave.
    """

    __requirements: Optional[rqs.RequirementList] = None

    # region Class Property Methods

    # TODO #19 make the requirements getter abstract and delete the setter

    @property
    def requirements(self) -> rqs.RequirementList:
        """Gets the list of requirements to run this CTATool.

        Retrieves the requirements from `self.__requirements`. These requirements determine if this CTA tool is
        appropriate for the given call.

        Returns:
            A `RequirementList`. This can be treated as a dict[str, Requirement], where the key is the associated
            key work for a `run_full` parameter.

        Raises:
            ValueError: if `self.__requirements` remains not implemented in a subclass
        """

        if self.__requirements is None:
            raise TypeError('Abstract field `__requirements` has not been set during class creation')
        return self.__requirements

    @requirements.setter
    def requirements(self, value: Dict[str, rqs.Requirement]) -> None:
        """Sets this CTA tool's list of requirements

        Arguments:
            value (Dict[str, Requirement]): A `dict` mapping `run_full` parameter names to their respective
                requirements. `self.__requirements` gets replaced by the `RequirementList` created using this value.

        Raises:
            ValueError: if `value` is not a `dict[str, Requirement]`
        """
        try:
            assert isinstance(value, dict)
            assert rqs.IsInstanceRequirement(str).are_compatible_with(*value.keys())
            assert rqs.IsInstanceRequirement(rqs.Requirement).are_compatible_with(*value.values())
        except AssertionError as e:
            raise ValueError('`CTAToolInterface.requirements must be a dictionary of `str` -> `Requirement`') from e

    # endregion

    # TODO #19 make the rest of the methods in this class static methods

    # region Abstract methods

    @abstractmethod
    def annotate(self, expr_data: AnnData, ref_data, **kwargs):
        """Runs annotation using tool.

        Arguments:
            expr_data (AnnData): expression data being analyzed
            ref_data (AnnData): reference/marker data used to analyze

        Returns:
            results of annotation using the tool in question
        """

    @abstractmethod
    def convert(self, results, convert_to: str, **kwargs) -> pd.Series:
        """Converts results to standardized format

        Arguments:
            results: tool results
            convert_to (str): format to which `res` will be converted

        Returns:
            `pandas.Series` object containing data in the `convert_to` format
        """

    # endregion

    # region Pre-processing methods

    def preprocess_expr(self, expr_data: AnnData, **kwargs):
        """Pre-process expr_data for use in a specific algorithm.

        Arguments:
            expr_data (AnnData): expression data being analyzed

        Returns:
            Expression data in a format that `annotate` will accept
        """
        return expr_data

    def preprocess_ref(self, ref_data, **kwargs):
        """Pre-process expr_data for use in a specific algorithm.

        Arguments:
            ref_data (AnnData): reference/marker data used to analyze

        Returns:
            Reference/marker data in a format that `annotate` will accept
        """
        return ref_data

    # endregion

    # region Other class methods for annotation

    def run_full(self, expr_data: AnnData, ref_data, convert_to: str, **kwargs) -> pd.Series:
        """Run `self.annotate`, followed by `self.convert` on a data set.

        Arguments:
            expr_data (AnnData): expression data being analyzed
            ref_data: reference/marker data used to analyze
            convert_to (str): format to which `res` will be converted

        Returns:
            `pandas.Series` object containing the results of annotation, in the
            `convert_to` format
        """

        expr_data_prepped = self.preprocess_expr(expr_data, **kwargs)
        ref_data_prepped = self.preprocess_ref(ref_data, **kwargs)

        results = self.annotate(expr_data_prepped, ref_data_prepped, **kwargs)
        return self.convert(results, convert_to, **kwargs)

    # endregion

    # region Class methods for requirement validation

    def is_compatible_with(self, values: Optional[Dict[str, Any]] = None, **kwargs) -> bool:
        """Check if a set of other values is compatible with this annotation tool interface

        Arguments:
            other_values (Dict[str, any]): A dictionary of `requirement_name` -> `other_value`

        Returns:
            `True` if all of the `other_values` are compatible with this `RequirementList`'s requirements
        """
        if values is None:
            values = {}

        return self.requirements.is_compatible_with(**{**values, **kwargs})

    # endregion
