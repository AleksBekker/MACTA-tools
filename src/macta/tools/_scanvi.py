import logging
from typing import Any, Union

import numpy as np
import pandas as pd
import scanpy as sc
from scanpy import AnnData
from scarches.models import SCANVI, SCVI

from macta.tools import CTAToolInterface
from macta.utils.requirements import EqualityRequirement, NotNoneRequirement, RequirementList


class ScanviInterface(CTAToolInterface):
    """Interface for running ScanVI analysis."""

    _requirements = RequirementList(
        annot_type=EqualityRequirement('ref'),
        batch_col=NotNoneRequirement(),
        cell_type_col=NotNoneRequirement(),
    )

    def annotate(self, expr_data: AnnData, ref_data: SCANVI, **kwargs: Any) -> SCANVI:
        """Runs annotation using `SCANVI`.

        Arguments:
            expr_data (AnnData): experimental data to analyse
            ref_data (Path): path to marker list to use

        Returns:
            The `SCANVI` model with all of the cell type predictions
        """

        # needs `ref_data`, so can't be done in preprocess
        model: SCANVI = SCANVI.load_query_data(expr_data, ref_data, freeze_dropout=True)
        model._unlabeled_indices = np.arange(expr_data.n_obs)
        model._labeled_indices = []

        model.train(
            max_epochs=100,
            plan_kwargs=kwargs,
            check_val_every_n_epoch=10,
        )

        return model

    def convert(self, results: SCANVI, convert_to: str, **kwargs: Any) -> Union[pd.DataFrame, pd.Series]:
        """Converts a `SCANVI` model to the standard data types.

        Arguments:
            results (SCANVI): ScanVI model with predictions
            convert_to (str): format to which `results` will be converted

        Returns:
            `pandas` object containing the results of the analysis in the specified format
        """

        if convert_to == 'labels':
            return pd.Series(results.predict())

        if convert_to == 'scores':
            results.predict(soft=False)

        raise ValueError(f'{convert_to} is an invalid option for `convert_to`')

    def preprocess_ref(self, ref_data: AnnData, cell_type_col: str = '', batch_col: str = '', ref_type: str = 'counts',
                       **kwargs: Any) -> SCANVI:
        """Preprocesses the reference data into a `SCANVI` model.

        Arguments:
            ref_data (AnnData): the reference data to process
            cell_type_col (str): the name of the observation column in `ref_data` containing the cell types
            batch_col (str): the name of the observation column in `ref_data` containing the batch IDs
            ref_type (str): the type of the reference

        Returns:
            A trained `SCANVI` model that can be used to predict cell types
        """

        SCVI.setup_anndata(ref_data, layer=ref_type, batch_key='batch')
        vae = SCVI(
            ref_data,
            n_layers=2,
            encode_covariates=True,
            deeply_inject_covariates=False,
            use_layer_norm='both',
            use_batch_norm='none',
        )

        vae.train()

        scanvae = SCANVI.from_scvi_model(vae, unlabeled_category='Unknown')

        scanvae.train(max_epochs=20)

        reference_latent = sc.AnnData(scanvae.get_latent_representation())
        reference_latent['scanvi_cell_type'] = ref_data.obs[cell_type_col].tolist()
        reference_latent['scanvi_batch'] = ref_data.obs[batch_col].tolist()

        reference_latent['scanvi_predictions'] = scanvae.predict()
        logging.info(f'ScanVI: accuracy = {np.mean(reference_latent.obs.scanvi_predictions == reference_latent.obs.cell_type):.4%}')

        return scanvae
