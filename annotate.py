
import os
import scanpy as sc

from tools.celltypist_interface import CelltypistInterface

tool_info_default = {
    'ref': {
        'celltypist': CelltypistInterface()
    },
    'marker': {

    }
}


def annotate(expr_data, ref_data, annot_type, result_type='labels',
             annot_tools='*', tool_info=tool_info_default, *args, **kwargs):
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
    pass
