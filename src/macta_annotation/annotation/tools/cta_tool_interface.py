"""Implementation of abstract class for an interface to a CTA tool."""

from anndata import AnnData
import pandas as pd

from abc import ABC, abstractmethod


class CTAToolInterface(ABC):
    """Abstract class for tool interfaces"""

    @abstractmethod
    def annotate(self, expr_data: AnnData, ref_data, **kwargs):
        """Runs annotation using tool.

        Arguments:
            expr_data (AnnData): experimental data being analyzed
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

    def run_full(self, expr_data: AnnData, ref_data, convert_to: str, **kwargs):
        """Run `self.annotate`, followed by `self.convert` on a data set

        Arguments:
            expr_data (AnnData): experimental data being analyzed
            ref_data (AnnData): reference/marker data used to analyze
            convert_to (str): format to which `res` will be converted

        Returns:
            results of annotation, in the `convert_to` format
        """

        results = self.annotate(expr_data, ref_data, **kwargs)
        return self.convert(results, convert_to, **kwargs)
