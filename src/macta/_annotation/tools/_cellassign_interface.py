"""Implementation of an interface for the `cellassign` tool."""

from anndata import AnnData
import pandas as pd
from scvi.external import CellAssign

from .utils import CTAToolInterface
from ...utils import requirements as rqs


class CellassignInterface(CTAToolInterface):

    __requirements = rqs.RequirementList(
        annot_type='marker'
    )

    def annotate(expr_data: AnnData, ref_data: pd.DataFrame, **kwargs):
        """Runs annotation using `cellassign`.

        Arguments:
            expr_data (AnnData): expression data being analyzed
            ref_data (pd.DataFrame): reference/marker data used to analyze

        Returns:
            results of annotation using the tool in question
        """

        args = {'size_factor_key': 'size_factor', **kwargs}

        CellAssign.setup_anndata(expr_data, size_factor_key=args['size_factor_key'])
        return CellAssign(expr_data, ref_data).train().predict()

    def convert(self, results, convert_to: str, **kwargs) -> pd.Series:
        """Converts `cellassign` results to standardized format.

        Arguments:
            results: celltypist results
            convert_to (str): format to which `res` will be converted

        Returns:
            `pandas.Series` object containing data in the `convert_to` format
        """
        return super().convert(results, convert_to, **kwargs)
