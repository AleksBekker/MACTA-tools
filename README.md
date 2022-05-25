# MACTA_py (Multi-tool Automated Cell Type Annotation in Python)

The goal of this code is to assemble multiple python-based cell type annotation tools into one *in silico* pipeline.

## Auto-Annotation Tools Currently Implemented:
- [celltypist](https://github.com/Teichlab/celltypist)

## Installation for Development

```bash
git clone https://github.com/AleksBekker/MACTA_py
cd MACTA_py
# conda create -n macta_py python=3.7
pip install -e .
```

## Citations

### Anndata

> Isaac Virshup, Sergei Rybakov, Fabian J. Theis, Philipp Angerer, F. Alexander Wolf
> bioRxiv 2021.12.16.473007; 
> doi: https://doi.org/10.1101/2021.12.16.473007

### Cellassign

> Zhang, A.W., O’Flanagan, C., Chavez, E.A. et al. 
> Probabilistic cell-type assignment of single-cell RNA-seq for tumor microenvironment profiling. 
> Nat Methods 16, 1007–1015 (2019). 
> https://doi.org/10.1038/s41592-019-0529-1

### Celltypist

> Cross-tissue immune cell analysis reveals tissue-specific adaptations and clonal architecture in humans. 
> bioRxiv, 2021.2004.2028.441762 (2021). 
> https://www.biorxiv.org/content/10.1101/2021.04.28.441762v2

### Scanpy

> Wolf, F., Angerer, P. & Theis, F. 
> SCANPY: large-scale single-cell gene expression data analysis. Genome Biol 19, 15 (2018). 
> https://doi.org/10.1186/s13059-017-1382-0

### SCVI

> Romain Lopez, Jeffrey Regier, Michael B Cole, Michael Jordan, Nir Yosef. 
> "Bayesian Inference for a Generative Model of Transcriptome Profiles from Single-cell RNA Sequencing." 
> In submission. Preprint available at https://www.biorxiv.org/content/early/2018/03/30/292037

### SCVI-Tools

> Gayoso, Adam, et al. 
> “A Python Library for Probabilistic Analysis of Single-Cell Omics Data.”
> Nature Biotechnology, Feb. 2022, 
> https://doi.org/10.1038/s41587-021-01206-w.

### Other Packages

Please refer to the repo's dependency tree (github.com/AleksBekker/MACTA_py/network/dependencies) 
for information on all other packages used, including: 

- Autopep8
- Pandas


