#!/usr/bin/sh

conda install mamba -c conda-forge
mamba install --file requirements.txt -c bioconda -c conda-forge
pip install -e .
