import os


if __name__ == '__main__':

    for protein in os.listdir('./results/protein315_drugbank9k'):
        for ligand in os.listdir(f"./results/protein315_drugbank9k/{protein}"):
            for prediction in os.listdir(f"./results/protein315_drugbank9k/{protein}/{ligand}"):
                if prediction.endswith('sdf') and prediction.startswith('rank1'):
                    confidence = prediction.split('confidence')[1].split('.sdf')[0]
                    if float(confidence) > 0.8:
                        print(ligand)