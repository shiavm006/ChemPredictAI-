from pathlib import Path
from huggingface_hub import hf_hub_download
import os

def download_models():
    """download ml models from hugging face hub"""
    models_dir = Path("ML_Model/models")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    # your hugging face model repo
    repo_id = "shivammehere/Chempridictai"
    
    model_files = [
        "reaction_type_model.pkl",
        "reaction_type_encoder.pkl",
        "hazard_level_model.pkl",
        "hazard_level_encoder.pkl"
    ]
    
    for filename in model_files:
        local_path = models_dir / filename
        
        if local_path.exists():
            print(f"✓ {filename} already exists")
            continue
        
        try:
            print(f"⏳ downloading {filename}...")
            downloaded_path = hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                repo_type="model",
                local_dir=str(models_dir),
                local_dir_use_symlinks=False
            )
            print(f"✓ downloaded {filename}")
        except Exception as e:
            print(f"✗ error downloading {filename}: {e}")
            print(f"  make sure you've uploaded models to huggingface.co/{repo_id}")

if __name__ == "__main__":
    download_models()

