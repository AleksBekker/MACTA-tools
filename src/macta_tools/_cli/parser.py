from argparse import ArgumentParser, FileType

from macta_tools.tools import AVAILABLE


def parser() -> ArgumentParser:
    parser = ArgumentParser('MACTA-tools', description='Tools for cell-type annotation in Python')

    subparsers = parser.add_subparsers(dest='subparser', help='sub-command help')
    run = subparsers.add_parser('run', help='Runs cell type annotation tools')

    # Required run arguments
    run.add_argument('expr', type=FileType(), help='Expression data')
    run.add_argument('ref', type=FileType(), help='Reference data')
    run.add_argument('annot_type', choices=['marker', 'ref'], help='Type of annotation to perform')
    run.add_argument('convert_to', choices=['labels', 'scores'], help='Output type')
    run.add_argument('output', type=FileType(), help='Output file')
    run.add_argument('-t', '--tools', choices=AVAILABLE.keys(), nargs='+', help='Cell type annotation tools to use')

    # Tool-dependent kwargs

    run.add_argument('--update_models', type=bool, help='Download new models for reference')
    run.add_argument('--force_update', type=bool, help='Force caches to be updated')

    run.add_argument('--batch_col', help='Reference data column name for batch identifiers')
    run.add_argument('--cell_type_col', help='Reference data column name for cell type identifiers')

    # List subcommand

    ls = subparsers.add_parser('list', help='Lists information about environment')
    ls.add_argument('to_list', choices=['tools'], nargs='?', default='tools', help='Which information to list')

    return parser
