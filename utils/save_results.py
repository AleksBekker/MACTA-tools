
def save_labels_results(results, path: str, savefile_type: str) -> None:
    '''Saves `labels` results in a file.

    Arguments:
        results: results to be stored
        path (str): path to save file to
        savefile_type (str): type of file to save to
    '''


default_save_methods = {
    'labels': save_labels_results,
}


def save_results(results, path: str, results_type: str, savefile_type: str,
                 save_methods=default_save_methods) -> None:
    '''Saves results into a file.

    Arguments:
        results: results to be saved
        path (str): path to save file to
        results_type (str): type of results currently being stored
        savefile_type (str): type of file to save to

    Keyword Arguments:
        save_methods: dictionary of `results_type` -> method to save it
    '''

    save_methods[results_type](results, path, savefile_type)
