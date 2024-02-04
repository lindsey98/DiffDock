# small script to extract the ligand and save it in a separate file because GNINA will use the ligand position as
# initial pose
import os
import shutil
import subprocess
import sys

import time
from argparse import ArgumentParser, FileType
from datetime import datetime

import numpy as np
import pandas as pd
from biopandas.pdb import PandasPdb
from rdkit import Chem
from rdkit.Chem import AllChem, MolToPDBFile
from scipy.spatial.distance import cdist

from datasets.pdbbind import read_mol, read_molecule
from utils.utils import read_strings_from_txt
import torch

class Logger(object):
    def __init__(self, logpath, syspart=sys.stdout):
        self.terminal = syspart
        self.log = open(logpath, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        pass

def log(*args):
    print(f'[{datetime.now()}]', *args)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='data/PDBBind_processed', help='')
    parser.add_argument('--file_suffix', type=str, default='_baseline_ligand', help='Path to folder with trained model and hyperparameters')
    parser.add_argument('--results_path', type=str, default='./results/gnina_predictions', help='')
    parser.add_argument('--complex_names_path', type=str, default='data/splits/timesplit_test', help='')
    parser.add_argument('--seed_molecules_path', type=str, default=None, help='Use the molecules at seed molecule path as initialization and only search around them')
    parser.add_argument('--seed_molecule_filename', type=str, default='equibind_corrected.sdf', help='Use the molecules at seed molecule path as initialization and only search around them')
    parser.add_argument('--smina', action='store_true', default=False, help='')
    parser.add_argument('--no_gpu', action='store_true', default=False, help='')
    parser.add_argument('--exhaustiveness', type=int, default=8, help='')
    parser.add_argument('--num_cpu', type=int, default=16, help='')
    parser.add_argument('--pocket_mode', action='store_true', default=False, help='')
    parser.add_argument('--pocket_cutoff', type=int, default=5, help='')
    parser.add_argument('--num_modes', type=int, default=10, help='')
    parser.add_argument('--autobox_add', type=int, default=4, help='')
    parser.add_argument('--prank_path', type=str, default='/Users/hstark/projects/p2rank_2.3/prank', help='')
    parser.add_argument('--skip_existing', action='store_true', default=False, help='')
    args = parser.parse_args()

    if os.path.exists(args.results_path) and not args.skip_existing:
        shutil.rmtree(args.results_path)
    os.makedirs(args.results_path, exist_ok=True)

    all_times = []
    start_time = time.time()
    protein_dict = torch.load('/home/ruofan/git_space/TankBind/datasets/protein_315.pt')
    compound_dict = torch.load('/home/ruofan/git_space/TankBind/datasets/drugbank_9k.pt')

    for protein in list(protein_dict.keys()):

        # call gnina to find binding pose
        log_path = os.path.join(args.results_path, f'{protein}{args.file_suffix}.log')

        # protein
        protein_pdb = os.path.join('/home/ruofan/git_space/TankBind/datasets/protein_315', protein + ".pdb")
        rec = PandasPdb().read_pdb(protein_pdb)
        rec_df = rec.get(s='c-alpha')
        rec_pos = rec_df[['x_coord', 'y_coord', 'z_coord']].to_numpy().squeeze().astype(np.float32)
        center_pocket = rec_pos.mean(axis=0)
        center_x = center_pocket[0]
        center_y = center_pocket[1]
        center_z = center_pocket[2]

        # ligand
        for ligand in list(compound_dict.keys()):

            prediction_output_name = os.path.join(args.results_path, f"{protein}_{ligand.split('_rdkit')[0]}.pdb")

            rdkit_mol_path = f"/home/ruofan/git_space/TankBind/datasets/drugbank_rdkit/{ligand.split('_rdkit')[0]}_from_rdkit.sdf"
            mol_rdkit = read_molecule(rdkit_mol_path, remove_hs=False)
            rdkit_lig_pos = mol_rdkit.GetConformer().GetPositions()
            diameter_pocket = np.max(cdist(rdkit_lig_pos, rdkit_lig_pos))
            size_x = diameter_pocket + args.autobox_add * 2
            size_y = diameter_pocket + args.autobox_add * 2
            size_z = diameter_pocket + args.autobox_add * 2

            '''p2rank predictions'''
            df = pd.read_csv(f"/home/ruofan/git_space/TankBind/datasets/protein_315_p2rank/{protein}.pdb_predictions.csv")
            if not df.empty:
                center_x = df.iloc[0]['   center_x']
                center_y = df.iloc[0]['   center_y']
                center_z = df.iloc[0]['   center_z']

        #     log(f'processing {rec_path}')
        #     # Start your Docker container if it's not already running
        #     subprocess.run(f"echo {111} | sudo -S docker run -d --name gnina gnina", shell=True)
        #
            command = (
                f"gnina --receptor {protein_pdb} --ligand {rdkit_mol_path} "
                f"--num_modes {args.num_modes} -o {prediction_output_name} "
                f"{'--no_gpu' if args.no_gpu else ''} --log {log_path} "
                f"--exhaustiveness {args.exhaustiveness} --cpu {args.num_cpu} "
                f"{'--cnn_scoring none' if args.smina else ''} "
                f"--center_x {center_x} --center_y {center_y} "
                f"--center_z {center_z} --size_x {size_x} "
                f"--size_y {size_y} --size_z {size_z}"
            )
            docker_run_command = f"echo {111} | sudo -S docker run gnina /bin/bash -c \"{command}\""

            process = subprocess.run(docker_run_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(process.stdout.decode())
            print(process.stderr.decode())

            # log("single time: --- %s seconds ---" % (time.time() - single_time))
            # log("time so far: --- %s seconds ---" % (time.time() - start_time))
            # log('\n')
    #
    # log(all_times)
    # log("--- %s seconds ---" % (time.time() - start_time))
