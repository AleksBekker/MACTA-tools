from argparse import ArgumentParser, FileType, Namespace
from pathlib import Path

import scanpy as sc
from pandas.compat.pickle_compat import pkl

from macta_tools import annotate


def parse_args() -> Namespace:

    parser = ArgumentParser('MACTA-tools', description='Tools for cell-type annotation in Python')

    parser.add_argument(
        'expr',
        # dest='expr_data',
        type=FileType(),
    )

    parser.add_argument(
        'ref',
        # dest='ref_data',
        type=FileType(),
    )

    parser.add_argument(
        'annot_type',
        choices=['marker', 'ref']
    )

    parser.add_argument(
        'convert_to',
        choices=['labels', 'scores'],
    )

    parser.add_argument(
        'output',
        # dest='output_path',
        type=FileType(),
    )

    parser.add_argument(
        '-t', '--tools',
        nargs='+',
    )

    # Tool kwargs

    parser.add_argument(
        '--force_update',
        type=bool,
    )

    parser.add_argument(
        '--update_models',
        type=bool,
    )

    parser.add_argument('--batch_col')
    parser.add_argument('--cell_type_col')

    return parser.parse_args()


# def read_file(path_name: bytes) -> Union[AnnData, pd.DataFrame, None]:
#
#     path = Path(str(path_name))
#     ext = path.suffix
#
#     if ext == 'csv':
#         return pd.read_csv(path)
#
#     if ext == 'tsv':
#         return pd.read_csv(path, delimiter='\t')
#
#     if ext == 'pkl':
#         with path.open('rb') as file:
#             return pkl.load(file)
#
#     if ext == 'h5ad':
#         return sc.read_h5ad(path)
#
#     return None


def main():
    args = parse_args()

    # print('\nARGUMENTS')
    # from pprint import pprint
    # pprint(vars(args))
    # print()

    expr_data = sc.read_h5ad(args.expr)
    ref_data = sc.read_h5ad(args.ref)

    results = annotate(expr_data, ref_data, **vars(args))

    with Path(args.output).open('wb') as file:
        pkl.dump(results, file)
