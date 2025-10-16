import joblib
import os
from ML_Model.utils.smiles_utils import is_valid_reaction_smiles, name_to_smiles, is_valid_smiles
from ML_Model.models.chemberta_features import get_chemberta_features

# lazy loading of models
_models_loaded = False
clf_type = None
le_type = None
clf_hazard = None
le_hazard = None

def load_models():
    """load trained models on first use"""
    global _models_loaded, clf_type, le_type, clf_hazard, le_hazard
    
    if _models_loaded:
        return
    
    models_dir = "ML_Model/models"
    clf_type = joblib.load(f"{models_dir}/reaction_type_model.pkl")
    le_type = joblib.load(f"{models_dir}/reaction_type_encoder.pkl")
    clf_hazard = joblib.load(f"{models_dir}/hazard_level_model.pkl")
    le_hazard = joblib.load(f"{models_dir}/hazard_level_encoder.pkl")
    _models_loaded = True

def predict_reaction(reactant1, reactant2, product=None, input_type="name"):
    # load models if not already loaded
    load_models()
    
    if input_type == "name":
        r1 = name_to_smiles(reactant1) or reactant1
        r2 = name_to_smiles(reactant2) or reactant2
        if product:
            p = name_to_smiles(product) or product
        else:
            # if no product provided, use a placeholder that won't be validated
            p = "C"  # simple placeholder
    else:
        r1, r2 = reactant1, reactant2
        p = product if product else "C"

    # try with full reaction smiles first
    reaction_smiles = f"{r1}.{r2}>>{p}"
    
    if is_valid_reaction_smiles(reaction_smiles):
        features = get_chemberta_features(reaction_smiles).reshape(1, -1)
        pred_type = le_type.inverse_transform(clf_type.predict(features))[0]
        pred_hazard = le_hazard.inverse_transform(clf_hazard.predict(features))[0]
        return pred_type, pred_hazard
    else:
        # fallback: just use reactants without product validation
        # create features from reactants only
        reactant_smiles = f"{r1}.{r2}"
        try:
            if is_valid_smiles(r1) and is_valid_smiles(r2):
                # use reactants with a dummy product for feature extraction
                dummy_reaction = f"{r1}.{r2}>>C"
                features = get_chemberta_features(dummy_reaction).reshape(1, -1)
                pred_type = le_type.inverse_transform(clf_type.predict(features))[0]
                pred_hazard = le_hazard.inverse_transform(clf_hazard.predict(features))[0]
                return pred_type, pred_hazard
        except:
            pass
        
        return "Substitution", "Medium"  # safe default fallback

# Example usage
if __name__ == "__main__":
    # For names
    pred_type, pred_hazard = predict_reaction("benzene", "bromine", "bromobenzene", input_type="name")
    print("Predicted Reaction Type:", pred_type)
    print("Predicted Hazard Level:", pred_hazard)

    # For SMILES
    pred_type, pred_hazard = predict_reaction("c1ccccc1", "BrBr", "c1ccccc1Br", input_type="smiles")
    print("Predicted Reaction Type:", pred_type)
    print("Predicted Hazard Level:", pred_hazard)
