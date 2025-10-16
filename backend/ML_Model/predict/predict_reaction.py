import joblib
from ML_Model.utils.smiles_utils import is_valid_reaction_smiles, name_to_smiles, is_valid_smiles
from ML_Model.models.chemberta_features import get_chemberta_features
from ML_Model.models.productPredictor import predict_product

models_dir = "ML_Model/models"
clf_type = joblib.load(f"{models_dir}/reaction_type_model.pkl")
le_type = joblib.load(f"{models_dir}/reaction_type_encoder.pkl")
clf_hazard = joblib.load(f"{models_dir}/hazard_level_model.pkl")
le_hazard = joblib.load(f"{models_dir}/hazard_level_encoder.pkl")

def predict_reaction(reactant1, reactant2, input_type="name"):
    if input_type == "name":
        r1 = name_to_smiles(reactant1) or reactant1
        r2 = name_to_smiles(reactant2) or reactant2
        p = predict_product(r1, r2)
    else:
        r1, r2, p = reactant1, reactant2, predict_product(reactant1, reactant2)

    reaction_smiles = f"{r1}.{r2}>>{p}"
    if is_valid_reaction_smiles(reaction_smiles):
        features = get_chemberta_features(reaction_smiles).reshape(1, -1)
        pred_type = le_type.inverse_transform(clf_type.predict(features))[0]
        pred_hazard = le_hazard.inverse_transform(clf_hazard.predict(features))[0]
        return pred_type, pred_hazard, p
    else:
        return "Invalid reaction SMILES", "Invalid reaction SMILES", "Invalid reaction SMILES"