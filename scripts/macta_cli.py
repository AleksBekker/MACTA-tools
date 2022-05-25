'''Run MACTA_py using CLI arguments'''

from macta import annotate
from macta.utils import DirectoryCloseMode, TemporaryFolder

import os

from anndata import AnnData
import pandas as pd
import scanpy as sc

import argparse

from typing import Union


def _parse_annotation_args() -> argparse.Namespace:
    '''Parse command-line arguments.

    Returns:
        argparse.Namespace: contains all parsed arguments and their values
    '''

    # Set up parser
    parser = argparse.ArgumentParser()

    # region REQUIRED UNNAMED ARGUMENTS

    # Path to expression data
    parser.add_argument(
        'expr_path',
        type=str,
        help='path to experiment data in an h5ad file',
    )

    # endregion

    # region OPTIONAL ARGUMENTS

    # Tools to use
    parser.add_argument(
        '--annot-tools',
        type=str,
        default='*',
        help='list of tools to be used in analysis, delimited by `,`s, "*" to selec all tools possible in `annot_type`',
    )

    # Name of column for labels in ref_data
    parser.add_argument(
        '-l', '--labels_col',
        type=str,
        help='name of the labels column in the `obs` of the expression AnnData',
    )

    # Path to temporary folder
    parser.add_argument(
        '--tmp',
        type=str,
        default='./tmp',
        help='path to directory into which temporary files will be placed',
    )

    # If selected, does NOT delete temporary folder after program runs
    parser.add_argument(
        '--keep_tmp',
        action='store_true',
        help='if selected, program will NOT delete the temporary file directory specified by --tmp',
    )

    # endregion

    # region REQUIRED NAMED ARGUMENTS

    required_named = parser.add_argument_group('required named arguments')

    # Experimental data argument

    # Path to reference/signature data
    required_named.add_argument(
        '-r', '--ref_path',
        type=str,
        help='path to reference/marker data in an h5ad (ref) or csv (marker) file',
        required=True,
    )

    # Type of automated annotation to perform
    required_named.add_argument(
        '-t', '--annot_type',
        type=str,
        choices=['ref', 'marker'],
        default='ref',
        help='type of annotation to perform. <REF/marker>',
        required=True
    )

    # Path to data output
    required_named.add_argument(
        '-o', '--output-path',
        type=str,
        help='path to output csv file',
        required=True
    )

    # Type of result
    required_named.add_argument(
        '--result_type',
        type=str,
        default='labels',
        choices=['labels'],
        help='type of result the output file will contain <LABELS>'
    )

    # endregion

    # Run argument parser
    return parser.parse_args()


def _load_ref_data(ref_path) -> Union[AnnData, pd.DataFrame]:
    '''Load the reference data, given the reference path.

    Arguments:
        ref_path (str): path to the reference data file

    Returns: 
        `AnnData` or `DataFrame` containing the proper reference data
    '''
    file_suffix = os.path.splitext(ref_path)[1]

    if file_suffix.lower() == '.h5ad':
        return sc.read(ref_path)

    if file_suffix.lower() == '.csv':
        return pd.read_csv(ref_path, index_col=0)

    raise ValueError('Invalid `ref_data` file type')


def main() -> None:
    '''Run the annotation method from CLI.'''

    raw_args = _parse_annotation_args()

    # Load expression and reference data
    expr_data = sc.read(raw_args.expr_path)
    ref_data = _load_ref_data(raw_args.ref_path)

    unnecessary_kwargs = {
        'annot_tools',
        'expr_path',
        'keep_tmp',
        'labels_col',
        'output_path',
        'ref_path',
        'tmp',
    }

    annotation_args = {
        **{k: v for k, v in vars(raw_args).items() if k not in unnecessary_kwargs},
        'annot_tools': '*' if raw_args.annot_tools == '*' else raw_args.annot_tools.split(','),
        'temp_folder': raw_args.tmp,
    }

    if raw_args.labels_col:
        annotation_args['labels'] = ref_data.obs[raw_args.labels_col]

    with TemporaryFolder(
            raw_args.tmp,
            DirectoryCloseMode.KEEP_ALL if raw_args.keep_tmp else DirectoryCloseMode.DELETE_DIRECTORY
    ):
        annotation_results = annotate(
            expr_data=expr_data,
            ref_data=ref_data,
            **annotation_args
        )

    annotation_results.to_csv(raw_args.output_path)


if __name__ == '__main__':
    main()
