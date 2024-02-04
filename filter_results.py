import os


if __name__ == '__main__':

    for protein in os.listdir('./results/protein315_drugbank9k'):
        confidence_list = []

        for ligand in os.listdir(f"./results/protein315_drugbank9k/{protein}"):
            for prediction in os.listdir(f"./results/protein315_drugbank9k/{protein}/{ligand}"):
                if prediction.endswith('sdf') and prediction.startswith('rank1'):
                    confidence = float(prediction.split('confidence')[1].split('.sdf')[0])
                    break
            confidence_list.append((ligand, confidence))

        confidence_list.sort(key=lambda x: x[1], reverse=True)
        top_3_ligands = [item for item in confidence_list if item[1] > 0.85][:3]

        print(top_3_ligands)