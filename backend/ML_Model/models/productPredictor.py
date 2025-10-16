from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the ReactionT5 model (forward reaction prediction)
model_name = "sagawa/ReactionT5v2-forward-USPTO_MIT"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def predict_product(reactant1_smiles, reactant2_smiles):
    # Format input as required: "reactant1.SMILES.reactant2.SMILES>>"
    input_str = f"{reactant1_smiles}.{reactant2_smiles}>>"
    inputs = tokenizer([input_str], return_tensors="pt")
    outputs = model.generate(**inputs, max_length=128)
    product_smiles = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return product_smiles