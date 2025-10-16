import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
import os

from ML_Model.utils.smiles_utils import is_valid_reaction_smiles, is_valid_smiles
from ML_Model.models.chemberta_features import get_chemberta_features

models_dir = "ML_Model/models"
os.makedirs(models_dir, exist_ok=True)
data_path = "data/chemical_reactions.csv"

df = pd.read_csv(data_path)
df['reaction_smiles'] = df['Reactant1_SMILES'] + '.' + df['Reactant2_SMILES'] + '>>' + df['Product_SMILES']

features = []
for s in df['reaction_smiles']:
    if is_valid_reaction_smiles(s):
        features.append(get_chemberta_features(s))
    else:
        features.append(np.zeros(768))  # or skip, or log

X = np.array(features)
le_type = LabelEncoder()
y_type = le_type.fit_transform(df['Reaction_Type'])
le_hazard = LabelEncoder()
y_hazard = le_hazard.fit_transform(df['Safety_Hazard_Level'])

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
