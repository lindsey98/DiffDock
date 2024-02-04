# DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/diffdock-diffusion-steps-twists-and-turns-for/blind-docking-on-pdbbind)](https://paperswithcode.com/sota/blind-docking-on-pdbbind?p=diffdock-diffusion-steps-twists-and-turns-for)

### [Paper on arXiv](https://arxiv.org/abs/2210.01776)

Implementation of DiffDock, state-of-the-art method for molecular docking, by Gabriele Corso*, Hannes Stark*, Bowen Jing*, Regina Barzilay and Tommi Jaakkola.
This repository contains all code, instructions and model weights necessary to run the method or to retrain a model. 
If you have any question, feel free to open an issue or reach out to us: [gcorso@mit.edu](gcorso@mit.edu), [hstark@mit.edu](hstark@mit.edu), [bjing@mit.edu](bjing@mit.edu).

![Alt Text](visualizations/overview.png)

The repository also contains all the scripts to run the baselines and generate the figures.
Additionally, there are visualization videos in `visualizations`.

You might also be interested in this [Google Colab notebook](https://colab.research.google.com/drive/1CTtUGg05-2MtlWmfJhqzLTtkDDaxCDOQ#scrollTo=zlPOKLIBsiPU) to run DiffDock by Brian Naughton. 

## Setup Environment
```bash
    conda create --name diffdock39 python=3.9
    conda activate diffdock39
    conda install pytorch=2.1.0 torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
    pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.1.0+cu121.html
    python -m pip install PyYAML scipy "networkx[default]" biopython rdkit-pypi e3nn spyrmsd pandas biopandas
    pip install "fair-esm[esmfold]"
    pip install 'dllogger @ git+https://github.com/NVIDIA/dllogger.git'
    pip install 'openfold @ git+https://github.com/aqlaboratory/openfold.git@4b41059694619831a7db195b7e0988fc4ff3a307'
    conda install pyg -c pyg
```


# Run virutal screening
```bash
python prepared_dataset.py
bash inference.sh
```
