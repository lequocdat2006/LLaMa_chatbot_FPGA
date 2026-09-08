from sentence_transformers import SentenceTransformer
from datasets import load_dataset

# Login using e.g. `huggingface-cli login` to access this dataset
ds = load_dataset("TranHoanggg/Vietnamese-history")
ds.save_to_disk("vietnamese_history_dataset")

# Load the vietnamese bi-encoder model
model = SentenceTransformer('bkai-foundation-models/vietnamese-bi-encoder')
model.save("vietnamese_bi_encoder")