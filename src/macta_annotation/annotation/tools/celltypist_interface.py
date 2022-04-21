"""Wrapper code for `celltypist`."""

import celltypist

from anndata import AnnData
from celltypist import AnnotationResult
import pandas as pd

from .cta_tool_interface import CTAToolInterface

import logging

# Disable `celltypist`'s drivial output logs
logging.getLogger(celltypist.__name__).setLevel(logging.ERROR)


class CelltypistInterface(CTAToolInterface):
    """Class for interfacing with the `celltypist` tool"""

    def annotate(
        self, expr_data: AnnData, ref_data: AnnData, **kwargs
    ) -> AnnotationResult:
        """Runs annotation using `celltypist`.

        Arguments:
            expr_data (AnnData): experimental data being analyzed
            ref_data (AnnData): reference/marker data used to analyze (NOT the model)
            labels_col: column of `ref_data` that contains annotation labels

        Returns:
            `AnnotationResult` object containing the results of annotation using `celltypist`
        """

        model = celltypist.train(ref_data, labels=kwargs['labels'])
        predictions = celltypist.annotate(expr_data, model=model, majority_voting=True)
        return predictions

    def convert(
        self, results: AnnotationResult, convert_to: str, **kwargs
    ) -> pd.Series:
        """Converts `celltypist` results to standardized format.

        Arguments:
            results (AnnotationResult): celltypist results
            convert_to (str): format to which `res` will be converted

        Returns:
            `pandas.Series` object containing data in the `convert_to` format
        """

        if convert_to == 'labels':
            return results.predicted_labels.majority_voting
        else:
            raise ValueError('Invalid option for `covert_to`')
