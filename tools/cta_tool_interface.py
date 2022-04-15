
from abc import ABC, abstractmethod


class CTAToolInterface(ABC):
    '''Abstract class for tool interfaces'''

    @abstractmethod
    def annotate(expr_data, ref_data, labels_col, **kwargs):
        '''Runs annotation using tool.

        Arguments:
            expr_data: experimental data being analyzed
            ref_data: reference/marker data used to analyze
            labels_col: column of `ref_data` that contains annotation labels

        Returns:
            results of annotation using the tool in question
        '''
        pass

    @abstractmethod
    def convert(res, convert_to: str):
        '''Converts results to standardized format

        Arguments:
            res: tool results
            convert_to (str): format to which `res` will be converted

        Returns: 
            data structure containing data in proper format
        '''
        pass
