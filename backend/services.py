import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import os
from dotenv import load_dotenv

# 1. LLM Gemini
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
# Sử dụng gemini-1.5-flash cho tốc độ nhanh vì chúng ta chỉ cần viết lại câu (query rewriting)
llm_model = genai.GenerativeModel("gemini-2.5-flash")

def rewrite_query(original_query: str) -> str:
    """
    Sử dụng LLM để viết lại câu hỏi ngắn thành một câu hỏi rõ nghĩa hơn, 
    mang tính chất pháp lý để hỗ trợ việc tìm kiếm tốt hơn.
    """
    prompt = f"""Bạn là một chuyên gia pháp lý Việt Nam. Người dùng thường hỏi các câu hỏi ngắn hoặc dùng từ lóng. 
Nhiệm vụ của bạn là viết lại câu hỏi của người dùng thành một câu truy vấn rõ nghĩa hơn, chuẩn xác về mặt ngữ nghĩa, sử dụng từ ngữ pháp lý Việt Nam, để dùng làm đầu vào cho hệ thống tìm kiếm ngữ nghĩa (Vector Search). Chỉ trả về câu đã viết lại, không thêm lời giải thích hay bất kì thông tin nào khác.

Ví dụ:
Câu hỏi: "Trộm chó phạt nhiêu?"
Viết lại: "Quy định xử phạt hành chính hoặc hình sự đối với hành vi trộm cắp tài sản là vật nuôi (chó) theo pháp luật Việt Nam hiện hành."

Câu hỏi hiện tại: "{original_query}"
Viết lại:"""
    try:
        response = llm_model.generate_content(prompt)
        rewritten = response.text.strip()
        # Fallback nếu model trả rỗng
        if not rewritten:
            return original_query
        return rewritten
    except Exception as e:
        print(f"Lỗi khi viết lại truy vấn: {e}")
        return original_query

# 2. Embedding Model (Vietnamese SBERT)
print("Loading Embedding Model...")
embedding_model = SentenceTransformer('keepitreal/vietnamese-sbert')

def embed_text(text: str) -> list[float]:
    """Chuyển đổi văn bản thành vector 768 chiều."""
    vector = embedding_model.encode(text)
    return vector.tolist()

# 3. Reranker (Cross-Encoder: BAAI/bge-reranker-v2-m3)
print("Loading Reranker Model...")
reranker_model_name = 'BAAI/bge-reranker-v2-m3'
reranker_tokenizer = AutoTokenizer.from_pretrained(reranker_model_name)
reranker_model = AutoModelForSequenceClassification.from_pretrained(reranker_model_name)
reranker_model.eval()

def rerank_results(query: str, documents: list[dict], top_k: int = 5) -> list[dict]:
    """
    Sử dụng Cross-Encoder để chấm điểm lại danh sách kết quả dựa trên độ liên quan giữa query và page_content.
    documents là list các dictionary, mỗi dict có trường 'page_content'.
    """
    if not documents:
        return []
        
    pairs = [[query, doc["page_content"]] for doc in documents]
    
    with torch.no_grad():
        inputs = reranker_tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
        scores = reranker_model(**inputs, return_dict=True).logits.view(-1,).float()
        
    # Gắn điểm vào từng doc
    for i, doc in enumerate(documents):
        doc["rerank_score"] = float(scores[i])
        
    # Sắp xếp lại theo điểm rerank giảm dần
    documents.sort(key=lambda x: x["rerank_score"], reverse=True)
    
    # Lấy top K
    return documents[:top_k]

def generate_answer(query: str, retrieved_texts: str) -> str:
    """
    Sử dụng LLM tổng hợp thông tin từ nhiều khoản/điều của cùng (các) văn bản để 
    viết thành câu trả lời duy nhất.
    """
    prompt = f"""Bạn là một chuyên gia pháp lý thông minh. 
Người dùng hỏi: "{query}"

Dưới đây là các tài liệu pháp lý liên quan được trích xuất (có thể chứa nhiều khoản/điều của cùng một văn bản):
{retrieved_texts}

Dựa vào các tài liệu trên, hãy tổng hợp thông tin, chọn lọc những thông tin đúng và liên quan nhất 
để viết một câu trả lời duy nhất, súc tích, mạch lạc, đẩy đủ ý và dễ hiểu cho người dùng.
- Nếu tài liệu có nhiều khoản của cùng một điều luật, hãy tổng hợp ý chính của các khoản đó thành một câu trả lời thống nhất. 
- Không liệt kê khô khan, hãy trả lời dưới dạng một chuyên gia đang tư vấn quy định luật.
- Chỉ trả lời dựa trên tài liệu được cung cấp.

Câu trả lời của bạn:"""
    try:
        response = llm_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Lỗi khi tạo câu trả lời tổng hợp: {e}")
        return "Xin lỗi, đã xảy ra lỗi trong quá trình tổng hợp câu trả lời tư vấn."

print("All models loaded successfully.")
