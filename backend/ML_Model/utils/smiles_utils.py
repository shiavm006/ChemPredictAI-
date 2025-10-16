from rdkit import Chem
import cirpy

def is_valid_smiles(smiles):
    '''
    Returns True if RDKit can parse the SMILES (including atom-mapped), False otherwise.
    '''
    try:
        mol = Chem.MolFromSmiles(smiles, sanitize=False)
        return mol is not None
    except Exception:
        return False

def is_valid_reaction_smiles(reaction_smiles):
    '''
    Returns True if all reactants and all products in the reaction are valid (including atom-mapped).
    '''
    try:
        reactant_part, product_part = reaction_smiles.split(">>")
        reactant_smiles = [s for s in reactant_part.split(".") if s.strip()]
        product_smiles = [s for s in product_part.split(".") if s.strip()]
        # Check at least 1 reactant and 1 product, and all parse
        return (
            bool(reactant_smiles) and bool(product_smiles) and
            all(is_valid_smiles(smi) for smi in reactant_smiles + product_smiles)
        )
    except Exception:
        return False

def name_to_smiles(name):
    common_chemicals = {
        "hydrochloric acid": "Cl",
        "nitric acid": "[N+](=O)(O)[O-]",
        "sulfuric acid": "OS(=O)(=O)O",
        "acetic acid": "CC(=O)O",
        "formic acid": "C(=O)O",
        "phosphoric acid": "OP(=O)(O)O",
        "carbonic acid": "OC(=O)O",
        "hydrogen chloride": "Cl",
        "hcl": "Cl",
        "h2so4": "OS(=O)(=O)O",
        "hno3": "[N+](=O)(O)[O-]",
    }
    
    name_lower = name.lower().strip()
    if name_lower in common_chemicals:
        return common_chemicals[name_lower]
    
    result = cirpy.resolve(name, 'smiles')
    return result if result else None

def smiles_to_name(smiles):
    try:
        result = cirpy.resolve(smiles, 'names')
        if result:
            if isinstance(result, list):
                result = result[0]
            if not result.startswith('('):
                return result
        
        result = cirpy.resolve(smiles, 'iupac_name')
        if result:
            if result.startswith('(') and ')' in result:
                result = result.split(')', 1)[1].strip('-')
            return result
            
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            Chem.RemoveStereochemistry(mol)
            simple_smiles = Chem.MolToSmiles(mol)
            simple_name = cirpy.resolve(simple_smiles, 'iupac_name')
            if simple_name and not simple_name.startswith('('):
                return simple_name
            
        return smiles
    except:
        return smiles
