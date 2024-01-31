
import argparse
import torch
import os
import pandas as pd

if __name__ == '__main__':
    # For many complexes:
    # create a csv file with paths to proteins and ligand files or SMILES.
    # It contains as columns `complex_name` (name used to save predictions, can be left empty),
    # `protein_path` (path to `.pdb` file, if empty uses sequence),
    # `ligand_description` (SMILE or file path)  and `protein_sequence` (to fold with ESMFold in case the protein_path is empty).
    # An example .csv is at `data/protein_ligand_example_csv.csv` and you would use it with `--protein_ligand_csv protein_ligand_example_csv.csv`.

    parser = argparse.ArgumentParser(description='Process some inputs.')

    # Add arguments with default values
    parser.add_argument('--proteinDirs', default="/home/ruofan/git_space/TankBind/datasets/protein_315", help='Directory for protein files')

    parser.add_argument('--ligandDirs', default="/home/ruofan/git_space/TankBind/datasets/drugbank", help='Directory for ligand files')

    parser.add_argument('--dataset_path', default='./data', help='Where to save the dataset')


    # Parse the arguments
    args = parser.parse_args()

    #### List of protein_path * List of ligand path
    for proteinName in os.listdir(args.proteinDirs):
        if proteinName.endswith('.pdb'):
            info = []
            proteinFile = os.path.join(args.proteinDirs, proteinName) # fixme: only the highest confidence prediction
            for ligand in os.listdir(args.ligandDirs):
                ligandFile = os.path.join(args.ligandDirs, ligand)
                info.append([f"Protein-{proteinName.split('.pdb')[0]}-Ligand-{ligand.split('.sdf')[0]}", proteinFile, ligandFile, None])

            info = pd.DataFrame(info, columns=['complex_name', 'protein_path', 'ligand_description', 'protein_sequence'])
            print(info)
            info.to_csv(os.path.join(args.dataset_path, proteinName.replace('.pdb', '.csv')), index=False)