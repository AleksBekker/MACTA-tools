"""Encloses the `annotate` function, which runs all necessary annotation tools."""

from anndata import AnnData
import pandas as pd

from typing import Any, Dict, List, Optional, Set, Tuple, Union

from macta.tools import CTAToolInterface, CelltypistInterface


def annotate(
    expr_data: AnnData,
    ref_data: Union[AnnData, pd.DataFrame],
    annot_type: str,
    result_type: str = 'labels',
    annot_tools: Union[str, List[str], Tuple[str], Set[str]] = '*',
    tool_interfaces: Optional[Dict[str, CTAToolInterface]] = None,
    **kwargs
) -> pd.DataFrame:
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
        tool_interfaces = {'celltypist': CelltypistInterface()}

    if annot_tools == '*':
        annot_tools = list(tool_interfaces.keys())

    requirements: Dict[str, Any] = {'annot_type': annot_type}

    return pd.DataFrame(
        {
            tool_name: tool_interfaces[tool_name].run_full(expr_data, ref_data, result_type, **kwargs)
            for tool_name, interface in tool_interfaces.items()
            if tool_name in annot_tools and interface.is_compatible_with(**requirements)
        }
    )
