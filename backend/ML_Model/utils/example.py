import pandas as pd
from rdkit import Chem
import cirpy

def name_to_smiles(name):
    if Chem.MolFromSmiles(name):
        return name  # already valid SMILES
    result = cirpy.resolve(name, 'smiles')
    return result if result and Chem.MolFromSmiles(result) else None

def all_valid_smiles(row):
    r1 = name_to_smiles(row['Reactant1_SMILES'])
    r2 = name_to_smiles(row['Reactant2_SMILES'])
    p = name_to_smiles(row['Product_SMILES'])
    if r1 and r2 and p:
        return pd.Series({'Reactant1_SMILES': r1, 'Reactant2_SMILES': r2, 'Product_SMILES': p})
    else:
        return pd.Series({'Reactant1_SMILES': None, 'Reactant2_SMILES': None, 'Product_SMILES': None})

raw = pd.read_csv('data/chemical_reactions_raw.csv')
smiles_df = raw.apply(all_valid_smiles, axis=1)
clean = pd.concat([smiles_df, raw[['Reaction_Type', 'Safety_Hazard_Level']]], axis=1)
clean = clean.dropna()
clean.to_csv('data/chemical_reactions.csv', index=False)
