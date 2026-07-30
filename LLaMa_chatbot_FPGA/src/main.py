import os
os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jre1.8.0_501"
VNCORENLP_ABS_PATH = os.path.abspath('./vncorenlp')
VIETNAMESE_BI_ENCODER_ABS_PATH = os.path.abspath('./vietnamese_bi_encoder')
PROJECT_ABS_PATH = os.path.abspath('.')

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

with open(f"{PROJECT_ABS_PATH}/vietnamese_history_dataset.pkl", "rb") as f:
    db = pickle.load(f)
model = SentenceTransformer(VIETNAMESE_BI_ENCODER_ABS_PATH)

print("Đang tự động tách từ toàn bộ cơ sở dữ liệu cho BM25...")
tokenized_corpus = db["pre_processed_texts"]
bm25 = BM25Okapi(tokenized_corpus)

while True:
    string_input = input("Nhập yêu cầu truy vấn của bạn (nhập 'exit' để thoát): ")
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

    top_scores, top_indices = torch.topk(hybrid_scores_tensor, k=2)
    passages_context = []
    for rank, idx in enumerate(top_indices):
        index_on_db = idx.item()
        score = top_scores[rank].item()
        answer_text = db["text_answers"][index_on_db]
        passages_context.append(answer_text)
    full_context = "\n".join(passages_context)

    system_content = (
            f"Bạn là một chuyên gia am hiểu về lịch sử Việt Nam."
            f"Trả lời bằng tiếng Việt, CHÍNH XÁC dựa vào các ngữ cảnh dưới đây."
            f"CHỈ được lấy thông tin từ ngữ cảnh được cung cấp dưới đây để trả lời. Nếu ngữ cảnh không có thông tin, hãy trả lời\"Tôi không biết\"."
            f"Phải TRÍCH XUẤT TOÀN BỘ các ngữ cảnh."
            f"Hiểu ngữ cảnh và mở rộng chúng, tạo ra phản hồi cho người dùng."
            f"=== NGỮ CẢNH ===\n{full_context}\n==================================="
        )
    try:
        response = ollama.chat(
            model='llama3.1:8b',
            options={
                'temperature': 0.0
            },
            messages=[
                {
                    'role': 'system', 
                    'content': system_content,
                },
                {
                    'role': 'user', 
                    'content': 'tạo phản hồi cho người dùng bằng cách hiểu và tóm tắt ngữ cảnh đã được cung cấp (tóm tắt nhưng vẫn đảm bảo đầy đủ thông tin trong ngữ cảnh)',
                }
            ]
        )
        print("\n=== CHATBOT PHẢN HỒI ===")
        print(response['message']['content'])
        print("===================================\n")
    except Exception as e:
        print(f"[Lỗi] Không thể kết nối hoặc xử lý với Ollama: {e}")