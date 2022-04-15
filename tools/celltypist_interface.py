
import scanpy as sc
import celltypist

from .cta_tool_interface import CTAToolInterface

# TODO: customize function docstrings specifically for the `celltypist` tool


class CelltypistInterface(CTAToolInterface):
    '''Class for interfacing with the `celltypist` tool'''

    def annotate(expr_data, ref_data, labels_col: str, **kwargs):
        '''Runs annotation using tool.

        Arguments:
            expr_data: experimental data being analyzed
            ref_data: reference/marker data used to analyze
            labels_col: column of `ref_data` that contains annotation labels

        Returns:
            results of annotation using the tool in question
        '''

        model = celltypist.train(ref_data, labels=labels_col)
        predictions = celltypist.annotate(
            expr_data, model=model, majority_voting=True)
        return predictions

    def convert(res, convert_to: str, **kwargs):
        '''Converts results to standardized format

        Arguments:
            res: tool results
            convert_to (str): format to which `res` will be converted

        Returns: 
            data structure containing data in proper format
        '''

        if convert_to == 'labels':
            return res.predicted_labels.majority_voting
        else:
            raise ValueError('Invalid option for `covert_to`')
