"""Wrapper code for `celltypist`."""

import celltypist

from anndata import AnnData
from celltypist import AnnotationResult, models
import pandas as pd

from . import CTAToolInterface
from ...utils import requirements as rqs

import logging
from typing import Union

# Disable `celltypist`'s trivial output logs
logging.getLogger(celltypist.__name__).setLevel(logging.ERROR)


class CelltypistInterface(CTAToolInterface):
    """Class for interfacing with the `celltypist` tool"""

    # TODO: do this through `super.requirements` property,
    # possibly using self.__post_init__()
    _requirements = rqs.RequirementList(annot_type=rqs.StrictRequirement('ref'))

    def annotate(self, expr_data: AnnData, ref_data: Union[AnnData, str], **kwargs) -> AnnotationResult:
        """Runs annotation using `celltypist`.

        Arguments:
            expr_data (AnnData): experimental data being analyzed
            ref_data (AnnData): reference/marker data used to analyze (NOT the model)

        Returns:
            `AnnotationResult` object containing the results of annotation using
            celltypist
        """
        return celltypist.annotate(expr_data, model=ref_data, majority_voting=True)

    def convert(self, results: AnnotationResult, convert_to: str, **kwargs) -> pd.Series:
        """Converts `celltypist` results to standardized format.

        Arguments:
            results (AnnotationResult): celltypist results
            convert_to (str): format to which `res` will be converted

        Returns:
            `pandas.Series` object containing data in the `convert_to` format
        """

        if convert_to == 'labels':
            return results.predicted_labels.majority_voting

        raise ValueError(f'{convert_to} is an invalid option for `convert_to`')

    def preprocess_ref(self, ref_data: Union[AnnData, str], **kwargs) -> models.Model:

        kwargs = {
            'update_models': True,
            'force_update': True,
            **kwargs
        }

        if isinstance(ref_data, str):
            if kwargs['update_models']:
                models.download_models(force_update=kwargs['force_update'])
            return models.Model.load(model=ref_data)

        elif isinstance(ref_data, AnnData):
            return celltypist.train(ref_data, labels=kwargs['labels'], check_expression=False)

        raise ValueError(f'{type(ref_data)} is an unsupported data type for `ref_data`')
