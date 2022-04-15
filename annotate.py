''' Encloses the `annotate` function, which runs all necessary annotation tools.'''

import scanpy as sc

from anndata import AnnData
import pandas as pd

from tools.cta_tool_interface import CTAToolInterface
from tools.celltypist_interface import CelltypistInterface


def annotate(expr_data: AnnData, ref_data: AnnData, labels_col,
             annot_type: str, result_type: str = 'labels', annot_tools: str | list[str] = '*',
             tool_interfaces: dict[str, dict[str, CTAToolInterface]] = {
                 'ref': {
                     'celltypist': CelltypistInterface(),
                 },
                 'marker': {

                 }
             }, *args, **kwargs):
    '''Runs MACTA.

    Arguments:
        expr_data: experimental data on which the analysis is performed
        ref_data: reference/marker data used to analyse `expr_data`
        annot_type (str): type of autoannotation to perform <marker/ref>
        result_type (str): type of results to output <labels>
        annot_tools (list[str]): tools to use in annotation, '*' to select all tools
        tool_info: dictionary of `annot_type` -> dict of annotation tool name -> `CTAToolInterface`

    Returns:
        results of auto-annotation
    '''

    # Select all tools if `annot_tools` == '*'
    if isinstance(annot_tools, str) and annot_tools == '*':
        annot_tools = tool_interfaces[annot_type].keys()

    return pd.DataFrame({tool_name:
                         tool_interfaces[annot_type][tool_name].run_full(
                             expr_data, ref_data, labels_col, result_type)
                         for tool_name in annot_tools})
