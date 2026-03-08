from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

from database import search_documents
from services import rewrite_query, embed_text, rerank_results, generate_answer

app = FastAPI(title="Legal RAG API")

# Cấu hình CORS để frontend có thể gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    original_query: str
    rewritten_query: str
    results: list
    generated_answer: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Legal RAG API is running"}

@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    original_query = request.query
    if not original_query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    logging.info(f"Original Query: {original_query}")
    print(f"Original Query: {original_query}")
    
    # 1. Query Rewriting via LLM
    rewritten_query = rewrite_query(original_query)
    logging.info(f"Rewritten Query: {rewritten_query}")
    print(f"Rewritten Query: {rewritten_query}")
    
    # 2. Embedding text
    query_vector = embed_text(rewritten_query)
    
    # 3. Hybrid Search DB (Vector Search + Keyword Search) -> Top 20
    docs = search_documents(query_vector=query_vector, query_text=rewritten_query, top_k=20)
    
    if not docs:
        return SearchResponse(
            original_query=original_query,
            rewritten_query=rewritten_query,
            results=[]
        )
        
    # 4. Rerank the results via CrossEncoder
    # Truyền cả query gốc để model reranker biết được user thực sự muốn gì (hoặc dùng text đã viết lại)
    # Lấy top 10 để gom được các chunk cùng loại văn bản
    reranked_docs = rerank_results(query=rewritten_query, documents=docs, top_k=10)
    
    # 5. Gom nhóm các khoản/điều theo cùng một tên văn bản (loại văn bản)
    grouped = {}
    ordered_ten_van_ban = []
    
    for doc in reranked_docs:
        tvb = doc.get("ten_van_ban", "Khác")
        if tvb not in grouped:
            grouped[tvb] = []
            ordered_ten_van_ban.append(tvb)
        grouped[tvb].append(doc["page_content"])
        
    # Chọn top 3 văn bản liên quan nhất
    top_3_tvb = ordered_ten_van_ban[:3]
    
    combined_texts = ""
    for tvb in top_3_tvb:
        combined_texts += f"--- Văn bản pháp luật: {tvb} ---\n"
        for content in grouped[tvb]:
            combined_texts += f"{content}\n"
            
    # Lọc lại danh sách Source Cards trả ra cho người dùng để chỉ hiện top 3 văn bản
    final_docs = []
    for tvb in top_3_tvb:
        # Lấy document đầu tiên đại diện cho văn bản này để lấy id, chu_de, loai_van_ban
        representative_doc = next(doc for doc in reranked_docs if doc.get("ten_van_ban", "Khác") == tvb)
        
        # Tạo merged document
        merged_doc = {
            "id": representative_doc.get("id"),
            "ten_van_ban": tvb,
            "chu_de": representative_doc.get("chu_de"),
            "loai_van_ban": representative_doc.get("loai_van_ban"),
            "link_goc": representative_doc.get("link_goc"),
            "rerank_score": representative_doc.get("rerank_score"),
            "page_content": "\n\n".join(grouped[tvb]) # Gộp nội dung tất cả các khoản/điều
        }
        final_docs.append(merged_doc)
    
    # 6. Sử dụng LLM tổng hợp các điều/khoản lại thành một câu trả lời hoàn chỉnh
    final_answer = generate_answer(original_query, combined_texts)
    
    return SearchResponse(
        original_query=original_query,
        rewritten_query=rewritten_query,
        results=final_docs,
        generated_answer=final_answer
    )

@app.get("/document")
def get_document(ten_van_ban: str):
    """
    Trả về toàn bộ nội dung của một văn bản pháp lý dựa vào tên văn bản.
    """
    if not ten_van_ban:
        raise HTTPException(status_code=400, detail="Thiếu tên văn bản")
        
    from database import get_db_connection
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Lấy toàn bộ chunk của văn bản này, sắp xếp theo ID (tạm coi ID tăng dần là thứ tự nội dung)
    # Nếu có trường chunk_id chứa thứ tự khoản/điều thì có thể sắp xếp tốt hơn
    cur.execute(
        "SELECT page_content FROM van_ban_phap_luat WHERE ten_van_ban = %s ORDER BY id ASC",
        (ten_van_ban,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    if not rows:
        raise HTTPException(status_code=404, detail="Không tìm thấy văn bản này")
        
    full_content = "\n\n".join([r[0] for r in rows])
    return {"ten_van_ban": ten_van_ban, "content": full_content}
