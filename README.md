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

# Dataset

The files in `data` contain the names for the time-based data split.

If you want to train one of our models with the data then: 
1. download it from [zenodo](https://zenodo.org/record/6408497) 
2. unzip the directory and place it into `data` such that you have the path `data/PDBBind_processed`


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


# Running DiffDock on your own complexes
We support multiple input formats depending on whether you only want to make predictions for a single complex or for many at once.\
The protein inputs need to be `.pdb` files or sequences that will be folded with ESMFold. 
The ligand input can either be a SMILES string or a filetype that RDKit can read like `.sdf` or `.mol2`.

For a single complex: specify the protein with `--protein_path protein.pdb` or `--protein_sequence GIQSYCTPPYSVLQDPPQPVV` and the ligand with `--ligand ligand.sdf` or `--ligand "COc(cc1)ccc1C#N"`

For many complexes: 
create a csv file with paths to proteins and ligand files or SMILES. 
It contains as columns `complex_name` (name used to save predictions, can be left empty), 
`protein_path` (path to `.pdb` file, if empty uses sequence), 
`ligand_description` (SMILE or file path)  and `protein_sequence` (to fold with ESMFold in case the protein_path is empty).
An example .csv is at `data/protein_ligand_example_csv.csv` and you would use it with `--protein_ligand_csv protein_ligand_example_csv.csv`.

And you are ready to run inference:

    CUDA_VISIBLE_DEVICES=2 python -m inference --protein_ligand_csv data/protein315_to_drugbank9k.csv --out_dir results/protein315_drugbank9k --inference_steps 20 --samples_per_complex 40 --batch_size 10 --actual_steps 18 --no_final_step_noise

When providing the `.pdb` files you can run DiffDock also on CPU, however, if possible, we recommend using a GPU as the model runs significantly faster. 
Note that the first time you run DiffDock on a device the program will precompute and store in cache look-up tables for SO(2) and SO(3) distributions (typically takes a couple of minutes), this won't be repeated in following runs.  


## Citation
    @article{corso2023diffdock,
          title={DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking}, 
          author = {Corso, Gabriele and Stärk, Hannes and Jing, Bowen and Barzilay, Regina and Jaakkola, Tommi},
          journal={International Conference on Learning Representations (ICLR)},
          year={2023}
    }

## License
MIT

## Acknowledgements

We thank Wei Lu and Rachel Wu for pointing out some issues with the code.


![Alt Text](visualizations/example_6agt_symmetric.gif)
