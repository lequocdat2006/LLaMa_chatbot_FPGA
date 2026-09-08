import os
os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jre1.8.0_501"
VNCORENLP_ABS_PATH = os.path.abspath('./vncorenlp')
DATASET_ABS_PATH = os.path.abspath('./vietnamese_history_dataset')
VIETNAMESE_BI_ENCODER_ABS_PATH = os.path.abspath('./vietnamese_bi_encoder')
PROJECT_ABS_PATH = os.path.abspath('.')

from py_vncorenlp import VnCoreNLP
model_vncorenlp = VnCoreNLP(annotators= ['wseg'], save_dir= VNCORENLP_ABS_PATH)

from sentence_transformers import SentenceTransformer
from datasets import load_from_disk
import pickle

def vn_word_tokenize(text):
    words = model_vncorenlp.word_segment(text)
    return " ".join(words)

# Login using e.g. `huggingface-cli login` to access this dataset
ds = load_from_disk(DATASET_ABS_PATH)
test_set = ds['train']

# EMBEDDING DATASET!
print("Đang tiến hành mã hóa toàn bộ tập test...")
model = SentenceTransformer(VIETNAMESE_BI_ENCODER_ABS_PATH)
combined_texts = [f"{item['question']} {item['answer']}" for item in test_set]
word_tokenized_texts = [vn_word_tokenize(text) for text in combined_texts]

combined_embeddings = model.encode(word_tokenized_texts)
print(f"Kích thước ma trận vector câu hỏi_trả lời: {combined_embeddings.shape}")
data_to_store = {
    "text_questions": test_set['question'],
    "text_answers": test_set['answer'],
    "pre_processed_texts": word_tokenized_texts,
    "vector_embeddings": combined_embeddings
}
with open(f"{PROJECT_ABS_PATH}/vietnamese_history_dataset.pkl", "wb") as f:
    pickle.dump(data_to_store, f)
print("Đã lưu dữ liệu đã được embedding vào tệp vietnamese_history_dataset.pkl trên ổ đĩa.")