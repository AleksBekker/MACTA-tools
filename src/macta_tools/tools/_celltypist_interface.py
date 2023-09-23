"""Wrapper code for `celltypist`."""

import logging
from dataclasses import dataclass
from typing import Any, Union

import celltypist
import pandas as pd
from anndata import AnnData
from celltypist import models
from celltypist.classifier import AnnotationResult

from macta_tools.tools._cta_tool_interface import CTAToolInterface
from macta_tools.utils.requirements import EqualityRequirement, RequirementList

# Disable `celltypist`'s trivial output logs
logging.getLogger(celltypist.__name__).setLevel(logging.ERROR)


class CelltypistInterface(CTAToolInterface):
    """Class for interfacing with the `celltypist` tool"""

    _name = 'celltypist'
    _requirements = RequirementList(
        annot_type=EqualityRequirement('ref'),
    )

    def annotate(self, expr_data: AnnData, ref_data: models.Model, **_: Any) -> AnnotationResult:
        """Runs annotation using `celltypist`.

        Arguments:
            expr_data (AnnData): experimental data being analyzed
            ref_data (AnnData): reference/marker data used to analyze (NOT the model)

        Returns:
            `AnnotationResult` object containing the results of annotation using celltypist
        """
        return celltypist.annotate(expr_data, model=ref_data, majority_voting=True)

    def convert(self, results: AnnotationResult, convert_to: str, **_: Any) -> Union[pd.DataFrame, pd.Series]:
        """Converts `celltypist` results to standardized format.

        Arguments:
            results (AnnotationResult): celltypist results
            convert_to (str): format to which `results` will be converted

        Returns:
            `pandas` object containing data in the `convert_to` format
        """

        if convert_to == 'labels':
            return results.predicted_labels.majority_voting

        if convert_to == 'scores':
            return results.probability_matrix

        raise ValueError(f'{convert_to} is an invalid option for `convert_to`')

    def preprocess_ref(self, ref_data: Union[AnnData, str], update_models: bool = True, force_update: bool = True,
                       **kwargs: Any) -> models.Model:
        """Preprocesses the reference data into a `celltypist.models.Model`.

        Arguments:
            ref_data (Union[AnnData, str]): raw reference data. Can be an `AnnData` on which to train the model or a
                `str` which represents the celltypist model name to load.
            update_models (bool): if `True`, updates the celltypist model cache
            force_update (bool): passed along directly to `celltypist.models.download_models`

        Returns:
            `celltypist.models.Model` to be used for annotation

        Notes:
            - When `ref_data` is a `str`, this function force-updates all celltypist models. This will result in a
                substantial delay while the data is being downloaded
            - TODO add another case of ref_data: loading a trained model from a file
        """

        if isinstance(ref_data, str):
            if update_models:
                models.download_models(force_update=force_update)
            return models.Model.load(model=ref_data)

        elif isinstance(ref_data, AnnData):
            return celltypist.train(ref_data, labels=kwargs['labels'], check_expression=False)

        raise ValueError(f'{type(ref_data)} is an unsupported data type for `ref_data`')
