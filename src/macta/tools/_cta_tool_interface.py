"""Implementation of abstract class for an interface to a CTA tool."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import pandas as pd
import pydantic

from macta.utils import requirements as rqs


class CTAToolInterface(pydantic.BaseModel, ABC):
    """Abstract class for tool interfaces"""

    requirements: Optional[rqs.RequirementList] = None

    # region Abstract methods

    @abstractmethod
    def annotate(self, expr_data: Any, ref_data: Any, **kwargs: Any) -> Any:
        """Runs annotation using tool.

        Arguments:
            expr_data (AnnData): expression data being analyzed
            ref_data (AnnData): reference/marker data used to analyze

        Returns:
            results of annotation using the tool in question
        """

    @abstractmethod
    def convert(self, results: Any, convert_to: str, **kwargs: Any) -> pd.Series:
        """Converts results to standardized format

        Arguments:
            results: tool results
            convert_to (str): format to which `res` will be converted

        Returns:
            `pandas.Series` object containing data in the `convert_to` format
        """

    # endregion

    # region Pre-processing methods

    def preprocess_expr(self, expr_data: Any, **kwargs: Any) -> Any:
        """Pre-process expr_data for use in a specific algorithm.

        Arguments:
            expr_data (AnnData): expression data being analyzed

        Returns:
            Expression data in a format that `annotate` will accept
        """
        return expr_data

    def preprocess_ref(self, ref_data: Any, **kwargs: Any) -> Any:
        """Pre-process expr_data for use in a specific algorithm.

        Arguments:
            ref_data (AnnData): reference/marker data used to analyze

        Returns:
            Reference/marker data in a format that `annotate` will accept
        """
        return ref_data

    # endregion

    # region Other class methods for annotation

    def run_full(self, expr_data: Any, ref_data: Any, convert_to: str, **kwargs: Any) -> pd.Series:
        """Run `self.annotate`, followed by `self.convert` on a data set.

        Arguments:
            expr_data (AnnData): expression data being analyzed
            ref_data: reference/marker data used to analyze
            convert_to (str): format to which `res` will be converted

        Returns:
            `pandas.Series` object containing the results of annotation, in the
            `convert_to` format
        """

        expr_data = self.preprocess_expr(expr_data, **kwargs)
        ref_data = self.preprocess_ref(ref_data, **kwargs)

        results = self.annotate(expr_data, ref_data, **kwargs)
        return self.convert(results, convert_to, **kwargs)

    # endregion

    # region Class methods for requirement validation

    def check_requirements(self, values: Optional[Dict[str, Any]] = None, **kwargs: Any) -> bool:
        """Check if a set of other values is compatible with this annotation tool interface

        Arguments:
            other_values (Dict[str, any]): A dictionary of `requirement_name` -> `other_value`

        Returns:
            `True` if all of the `other_values` are compatible with this `RequirementList`'s requirements
        """
        if self.requirements is None:
            return True

        if values is None:
            values = {}

        return self.requirements.check(**values, **kwargs)

    # endregion
