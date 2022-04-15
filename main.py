'''Run MACTA_py using CLI arguments'''

import argparse


def _parse_annotation_args() -> argparse.Namespace:
    '''Parse command-line arguments.

    Returns:
        argparse.Namespace: contains all parsed arguments and their values
    '''

    # Set up parser
    parser = argparse.ArgumentParser()

    # region OPTIONAL ARGUMENTS

    # Tests to perform
    parser.add_argument(
        '--tools',
        type=str,
        default='*',
        help='list of tools to be used in analysis, delimited by `,`s, "*" for all',
    )

    # Output folder argument
    # parser.add_argument(
    #     '-o', '--output',
    #     type=str,
    #     help='path to output file',
    # )

    # # Output file type
    # parser.add_argument(
    #     '--output_type',
    #     type=str,
    #     choices=['csv', 'tsv', ],
    #     default='csv',
    #     help='type of file used for output',
    # )

    # # Use stdout to output results
    # parser.add_argument(
    #     '-s', '--stdout',
    #     action='store_true',
    #     help='when this argument is included, the results will be outputted to stdout, disregarding the --output option'
    # )

    # endregion

    # region REQUIRED NAMED ARGUMENTS

    required_named = parser.add_argument_group('required named arguments')

    # Experimental data argument
    required_named.add_argument(
        '-e', '--expr_path',
        type=str,
        help='path to experiment data in h5 seurat file',
        required=True,
    )

    # Reference data argument
    required_named.add_argument(
        '-r', '--ref_path',
        type=str,
        help='path to reference/marker data in h5 seurat file',
        required=True,
    )

    # Test type argument
    required_named.add_argument(
        '-t', '--type',
        type=str,
        choices=['marker', 'ref'],
        help='type of test to perform',
        required=True,
    )

    # Result type
    required_named.add_argument(
        '--result_type',
        type=str,
        choices=['labels'],
        help='type of output to be generated by the pipeline',
        required=True,
    )

    required_named.add_argument(
        '-l', '--labels_col',
        type=str,
        help='string name of column in `ref_data`',
        required=True,
    )
    # Output folder argument
    required_named.add_argument(
        '-o', '--output',
        type=str,
        help='path to output file',
        required=True,
    )

    # endregion

    # Run argument parser
    return parser.parse_args()


def main() -> None:
    '''Run the annotation method from CLI.'''

    raw_args = _parse_annotation_args()

    import scanpy as sc
    expr_data = sc.read(raw_args.expr_path)
    ref_data = sc.read(raw_args.ref_path)
    labels_col = raw_args.labels_col

    annot_type = raw_args.type
    annot_tools = '*' if raw_args.tools == '*' else raw_args.tools.split(',')
    result_type = raw_args.result_type

    unnecessary_kwargs = {
        'expr_path',
        'labels_col',
        'output',
        # 'output_type',
        'ref_path',
        'result_type',
        'tools',
        'type',
    }

    annotation_kwargs = {k: v for k, v in vars(raw_args).items()
                         if k not in unnecessary_kwargs}

    from annotate import annotate
    annotation_results = annotate(expr_data, ref_data, labels_col,
                                  annot_type, annot_tools=annot_tools,
                                  result_type=result_type,
                                  **annotation_kwargs)

    annotation_results.to_csv(raw_args.output)


if __name__ == '__main__':
    main()
