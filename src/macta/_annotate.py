"""Encloses the `annotate` function, which runs all necessary annotation tools."""

import logging
from typing import Any, Container, Dict, Optional, Union

import pandas as pd
from anndata import AnnData

from macta.tools import AVAILABLE, CTAToolInterface


def annotate(expr_data: AnnData, ref_data: Union[AnnData, pd.DataFrame], annot_type: str, result_type: str = 'labels',
             annot_tools: Union[str, Container[str]] = '*',
             tool_interfaces: Optional[Dict[str, CTAToolInterface]] = None, **kwargs: Any
             ) -> Dict[str, Union[pd.Series, pd.DataFrame]]:
    """Runs MACTA annotation analysis.

    Arguments:
        expr_data (AnnData): experimental data on which the analysis is performed
        ref_data (AnnData/DataFrame): reference/marker data used to analyse `expr_data`
        annot_type (str): type of autoannotation to perform <marker/ref>
        result_type (str): type of results to output <labels>
        annot_tools (str/List[str]): selection of tools to consider using in annotation, '*' to select all tools
        tool_interfaces (Dict): dict of annotation tool name -> `CTAToolInterface`

    Returns:
        results of auto-annotation
    """

    if tool_interfaces is None:
        tool_interfaces = AVAILABLE

    if annot_tools == '*':
        annot_tools = list(tool_interfaces.keys())

    results = {}

    for tool_name, interface in tool_interfaces.items():
        if tool_name not in annot_tools:
            continue

        result = run_tool(tool_name, interface, expr_data, ref_data, annot_type, result_type, **kwargs)
        if result is not None:
            results[tool_name] = result

    return results


def run_tool(tool_name: str, interface: CTAToolInterface, expr_data: AnnData, ref_data: AnnData, annot_type: str,
             result_type: str, **kwargs: Any) -> Optional[pd.Series]:
    """Fully runs the annotation for one tool and handles typical issues and exceptions.

    Arguments:
        tool_name (str): the name of the tool being run, used for logging
        interface (CTAToolInterface): the interface to run
        expr_data (AnnData): expression data for the cells to label
        ref_data (AnnData): reference data for the cells to label
        annot_type (str): annotation type to perform <marker/ref>
        result_type (str): a string representing how the result should be structured
        **kwargs (Any): other key word arguments to pass to the interface functions

    Returns:
        A `pandas.Series` containing the results for each cell type if the run is valid. Otherwise, returns `None`
    """

    if interface._requirements is None:
        logging.warn(f'{tool_name}: no requirements available. Proceeding with run.')
        return None

    if not interface._requirements.check(expr_data=expr_data, ref_data=ref_data, annot_type=annot_type,
                                         result_type=result_type, **kwargs):
        logging.warn(f'{tool_name}: incompatible requirements. Skipping this tool.')
        return None

    try:
        return interface.run_full(expr_data, ref_data, result_type, **kwargs)

    except ImportError:
        # NOTE this should never occur if the tool_interfaces are set according to what can be imported
        logging.error(f'{tool_name}: required packages not imported. Skipping this tool.')

    except Exception as e:
        logging.error(f'{tool_name}: main run encountered unknown error {e}. Skipping this run')

    return None
