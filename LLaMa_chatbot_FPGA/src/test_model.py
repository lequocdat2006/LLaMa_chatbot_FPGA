import os
os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jre1.8.0_501"
VNCORENLP_ABS_PATH = os.path.abspath('./vncorenlp')
VIETNAMESE_BI_ENCODER_ABS_PATH = os.path.abspath('./vietnamese_bi_encoder')

from py_vncorenlp import VnCoreNLP
model_vncorenlp = VnCoreNLP(annotators= ['wseg'], save_dir= VNCORENLP_ABS_PATH)

from Pre_processing import pre_processing
from sentence_transformers import SentenceTransformer, util
import pickle
import torch
import numpy as np
from rank_bm25 import BM25Okapi
import ollama 

def vn_word_tokenize(text):
    words = model_vncorenlp.word_segment(text)
    return " ".join(words)

with open("D:\\NCKH\\Code\\Main\\vietnamese_history_dataset.pkl", "rb") as f:
    db = pickle.load(f)
model = SentenceTransformer(VIETNAMESE_BI_ENCODER_ABS_PATH)

print("Đang tự động tách từ toàn bộ cơ sở dữ liệu cho BM25...")
tokenized_corpus = db["pre_processed_texts"]
bm25 = BM25Okapi(tokenized_corpus)

client = ollama.Client()
with open("D:\\NCKH\\Code\\Main\\input.txt", "r", encoding="utf-8") as f:
    input_text = f.readlines()
input_text = [text.strip() for text in input_text]
file_context = open("D:\\NCKH\\Code\\Main\\context.txt", "w", encoding="utf-8")
for query in input_text:
    string_input = query
    if string_input.lower() == "exit":
        break
    user_query_raw = string_input
    user_query = pre_processing([user_query_raw])
    word_tokenized_query = vn_word_tokenize(user_query[0])
    tokenized_query = word_tokenized_query.split(" ")

    bm25_scores = bm25.get_scores(tokenized_query)
    bm25_scores_max = np.max(bm25_scores) if np.max(bm25_scores) > 0 else 1
    normalized_bm25_scores = bm25_scores / bm25_scores_max

    query_embeddings = model.encode([word_tokenized_query], convert_to_tensor=True)
    stored_embeddings = torch.tensor(db['vector_embeddings'])
    cosine_scores = util.cos_sim(query_embeddings, stored_embeddings)[0].cpu().numpy()

    alpha = 0.7
    hybrid_scores = alpha * normalized_bm25_scores + (1 - alpha) * cosine_scores
    hybrid_scores_tensor = torch.tensor(hybrid_scores)

    top_scores, top_indices = torch.topk(hybrid_scores_tensor, k=1)
    passages_context = []
    for rank, idx in enumerate(top_indices):
        index_on_db = idx.item()
        score = top_scores[rank].item()
        answer_text = db["text_answers"][index_on_db]
        passages_context.append(answer_text)
    full_context = "\n".join(passages_context)
    file_context.write(full_context + "\n")