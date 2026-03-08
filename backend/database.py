import psycopg2
from typing import List, Dict, Any

import os
from dotenv import load_dotenv

load_dotenv()

# Cấu hình DB PostgreSQL 
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "phapluat_rag")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASSWORD", "admin123")
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def search_documents(query_vector: List[float], query_text: str, top_k: int = 20) -> List[Dict[str, Any]]:
    """
    Thực hiện Hybrid Search: Vector Search + Keyword Search (BM25/ts_rank).
    Kết hợp kết quả lại với metadata filtering 'tinh_trang_hieu_luc' = 'Còn hiệu lực'.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Vector (768 chiều), ts_query, và filter tình trạng hiệu lực
    # Sử dụng phép gộp dạng rrf (Reciprocal Rank Fusion) hoặc weighted sum thủ công.
    # Trong PG, truy vấn pgvector dùng toán tử <=> (cosine distance). 
    # Truy vấn keyword dùng ts_rank_cd(to_tsvector('simple', page_content), plainto_tsquery('simple', %s)).
    # Vì ts_rank và cosine distance có scale khác nhau, ta lấy khoảng top_k * 2 từ mỗi bên, 
    # chấm điểm lại rồi trả về top_k. Hoặc đơn giản lấy thẳng combined score ở SQL.
    
    # Để đơn giản và hiệu quả, ta lấy vector search làm chính, keyword làm phụ (có thể normalize score).
    # Chú ý: cosine distance càng nhỏ càng giống, cosine similarity = 1 - cosine distance.
    
    sql_query = """
    WITH vector_search AS (
        SELECT 
            id, chunk_id, ten_van_ban, chu_de, loai_van_ban, tinh_trang_hieu_luc, page_content, link_goc,
            1 - (embedding <=> %s::vector) AS vector_score
        FROM van_ban_phap_luat
        WHERE tinh_trang_hieu_luc = 'Còn hiệu lực'
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    ),
    keyword_search AS (
        SELECT 
            id, chunk_id, ten_van_ban, chu_de, loai_van_ban, tinh_trang_hieu_luc, page_content, link_goc,
            ts_rank_cd(to_tsvector('simple', page_content), plainto_tsquery('simple', %s)) AS keyword_score
        FROM van_ban_phap_luat
        WHERE tinh_trang_hieu_luc = 'Còn hiệu lực' 
          AND to_tsvector('simple', page_content) @@ plainto_tsquery('simple', %s)
        ORDER BY keyword_score DESC
        LIMIT %s
    )
    SELECT 
        COALESCE(v.id, k.id) as id, 
        COALESCE(v.page_content, k.page_content) as page_content,
        COALESCE(v.ten_van_ban, k.ten_van_ban) as ten_van_ban,
        COALESCE(v.chu_de, k.chu_de) as chu_de,
        COALESCE(v.loai_van_ban, k.loai_van_ban) as loai_van_ban,
        COALESCE(v.link_goc, k.link_goc) as link_goc,
        COALESCE(v.vector_score, 0) as vector_score, 
        COALESCE(k.keyword_score, 0) as keyword_score,
        -- Weighted sum giả định: Vector đóng vai trò 0.7, Keyword 0.3
        -- Lưu ý keyword_score không bị chặn ở 1 nhưng thường khá nhỏ ở simple dict, có thể phải normalize.
        (COALESCE(v.vector_score, 0) * 0.7 + COALESCE(k.keyword_score, 0) * 0.3) AS combined_score
    FROM vector_search v
    FULL OUTER JOIN keyword_search k ON v.id = k.id
    ORDER BY combined_score DESC
    LIMIT %s;
    """
    
    cur.execute(
        sql_query, 
        (query_vector, query_vector, top_k * 2, query_text, query_text, top_k * 2, top_k * 2)
    )
    rows = cur.fetchall()
    
    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "page_content": r[1],
            "ten_van_ban": r[2],
            "chu_de": r[3],
            "loai_van_ban": r[4],
            "link_goc": r[5],
            "vector_score": r[6],
            "keyword_score": r[7],
            "combined_score": r[8]
        })
        
    cur.close()
    conn.close()
    
    return results
