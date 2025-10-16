from rdkit import Chem
import cirpy

def is_valid_smiles(smiles):
    return Chem.MolFromSmiles(smiles) is not None

def is_valid_reaction_smiles(reaction_smiles):
    try:
        reactants, products = reaction_smiles.split(">>")
        reactant_smiles = reactants.split(".")
        product_smiles = products.split(".")
        for smi in reactant_smiles + product_smiles:
            if not is_valid_smiles(smi):
                return False
        return True
    except Exception:
        return False

def name_to_smiles(name):
    result = cirpy.resolve(name, 'smiles')
    return result if result else None
