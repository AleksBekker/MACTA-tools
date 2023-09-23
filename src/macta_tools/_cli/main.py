from pathlib import Path

import scanpy as sc
from pandas.compat.pickle_compat import pkl

from macta_tools import annotate
from macta_tools._cli.parser import parser
from macta_tools.tools import AVAILABLE


def main():
    args = parser().parse_args()

    if args.subparser == 'run':
        expr_data = sc.read_h5ad(args.expr)
        ref_data = sc.read_h5ad(args.ref)

        results = annotate(expr_data, ref_data, **vars(args))

        with Path(args.output).open('wb') as file:
            pkl.dump(results, file)

    elif args.subparser == 'list':
        if args.to_list == 'tools':
            print('\n'.join(AVAILABLE.keys()))
        else:
            raise ValueError(f'{args.to_list} not listable.')

    else:
        raise ValueError(f'{args.subparser} is an invalid subparser')
