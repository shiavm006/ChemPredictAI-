import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
import os

from ML_Model.utils.smiles_utils import is_valid_reaction_smiles
from ML_Model.models.chemberta_features import get_chemberta_features

models_dir = "ML_Model/models"
os.makedirs(models_dir, exist_ok=True)
data_path = "data/traindata.csv"  # Update as needed

def label_mechanistic_hazard(label_str):
    """
    Placeholder hazard level based on number of unique mechanistic steps.
    You MUST update this mapping based on domain knowledge.
    """
    try:
        items = eval(label_str)
        vals = []
        for elem in items:
            if isinstance(elem, (list, tuple)): vals.extend(elem)
            else: vals.append(elem)
        n = len(set([int(float(i)) for i in vals if str(i).replace('.', '', 1).isdigit()]))
        if n > 10: return 'High'
        elif n > 5: return 'Moderate'
        else: return 'Low'
    except Exception:
        return 'Unknown'

df = pd.read_csv(data_path)
df = df.dropna(subset=['original_reactions', 'updated_reaction', 'mechanistic_class', 'mechanistic_label'])

valid_indices = []
features = []
print("Generating features and validating SMILES ...")
for idx, reaction in enumerate(df['original_reactions']):
    if is_valid_reaction_smiles(reaction):
        features.append(get_chemberta_features(reaction))
        valid_indices.append(idx)
    # else: you may wish to log invalid rows

X = np.array(features)
df_valid = df.iloc[valid_indices].reset_index(drop=True)

# Target: Reaction Type
le_type = LabelEncoder()
y_type = le_type.fit_transform(df_valid['mechanistic_class'])

# Target: Hazard, derived from mechanistic_label
y_hazard_txt = df_valid['mechanistic_label'].apply(label_mechanistic_hazard)
le_hazard = LabelEncoder()
y_hazard = le_hazard.fit_transform(y_hazard_txt)

# Train/test split & classifiers
X_train, X_test, y_train, y_test = train_test_split(X, y_type, test_size=0.2, random_state=42)
clf_type = RandomForestClassifier(n_estimators=100, random_state=42)
clf_type.fit(X_train, y_train)
print("Reaction Type Classification Report:")
print(classification_report(y_test, clf_type.predict(X_test), labels=np.arange(len(le_type.classes_)), target_names=le_type.classes_, zero_division=0))
joblib.dump(clf_type, os.path.join(models_dir, "reaction_type_model.pkl"))
joblib.dump(le_type, os.path.join(models_dir, "reaction_type_encoder.pkl"))

X_train, X_test, y_train, y_test = train_test_split(X, y_hazard, test_size=0.2, random_state=42)
clf_hazard = RandomForestClassifier(n_estimators=100, random_state=42)
clf_hazard.fit(X_train, y_train)
print("Safety Hazard Classification Report:")
print(classification_report(y_test, clf_hazard.predict(X_test), labels=np.arange(len(le_hazard.classes_)), target_names=le_hazard.classes_, zero_division=0))
joblib.dump(clf_hazard, os.path.join(models_dir, "hazard_level_model.pkl"))
joblib.dump(le_hazard, os.path.join(models_dir, "hazard_level_encoder.pkl"))