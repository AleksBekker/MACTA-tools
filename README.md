# MACTA_py (Multi Automated Cell Type Annotation Using Python Tools)

The goal of this code is to assemble multiple python-based cell type annotation tools into one *in silico* pipeline.

## Auto-Annotation Tools Currently Implemented:
- `celltypist`

# Installation for Development

```bash
git clone https://github.com/AleksBekker/MACTA_py
conda create -n macta_py python=3.7
conda install --file requirements.txt -c bioconda -c conda-forge
conda install --file requirements_dev.txt -c conda-forge
pip install -e .
```
