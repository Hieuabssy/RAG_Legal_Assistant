import json
import psycopg2
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import os

# Cấu hình đường dẫn dữ liệu đã được chunking
DATA_PATH = r"d:\RAG\vectorDB\chungking\chunked_data.json"

# Cấu hình DB PostgreSQL (đã được bọc qua Docker)
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "phapluat_rag"
DB_USER = "admin"
DB_PASS = "admin123"

def init_db():
    print("1. Đang kết nối Database PostgreSQL...")
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()
    
    # Bật extension pgvector
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    
    # Vector kích thước 768 là chuẩn đầu ra của model 'keepitreal/vietnamese-sbert'
    print("   -> Tạo bảng van_ban_phap_luat...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS van_ban_phap_luat (
            id SERIAL PRIMARY KEY,
            chunk_id VARCHAR(255),
            ten_van_ban TEXT,
            chu_de TEXT,
            loai_van_ban VARCHAR(100),
            tinh_trang_hieu_luc VARCHAR(100),
            page_content TEXT,
            embedding VECTOR(768),
            link_goc VARCHAR(255)
        );
    """)
    conn.commit()
    return conn, cur

def main():
    # 1. Khởi tạo Database
    conn, cur = init_db()
    
    # 2. Khởi tạo Model nhúng (Embedding)
    print("\n2. Đang tải Embedding Model (Tiếng Việt: vietnamese-sbert)...")
    model = SentenceTransformer('keepitreal/vietnamese-sbert')
    
    # 3. Đọc file JSON đã chunking
    print(f"\n3. Đọc dữ liệu từ: {DATA_PATH}...")
    if not os.path.exists(DATA_PATH):
        print(f"LỖI: Không tìm thấy file {DATA_PATH}!")
        return
        
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"   -> Đã tải thành công {len(data)} chunk dữ liệu pháp luật.")
    
    print("\n4. BẮT ĐẦU EMBEDDING DỮ LIỆU ĐÃ CHUNKING...")
    print("   CẢNH BÁO: Vì số lượng vector rất lớn, quá trình này sẽ mất một khoảng thời gian!\n")
    
    # Dùng tqdm để tạo thanh tiến trình hiển thị cho trực quan
    for item in tqdm(data, desc="Tiến trình Embedding"):
        chunk_id = item.get("chunk_id", "")
        page_content = item.get("page_content", "")
        metadata = item.get("metadata", {})
        
        ten_van_ban = metadata.get("ten_van_ban", "")
        chu_de = metadata.get("chu_de_ten", "")
        loai_van_ban = metadata.get("loai_van_ban", "")
        tinh_trang_hieu_luc = metadata.get("tinh_trang_hieu_luc", "")
        link_goc = metadata.get("link_goc", "")
        
        if not page_content.strip():
            continue
            
        # ĐƯA VÀO AI: Biến đoạn text thành Vector (mảng 768 con số)
        vector = model.encode(page_content)
        vector_list = vector.tolist() # PostgreSQL nhận định dạng list
        
        # SQL nhét dòng vào Database
        cur.execute(
            """
            INSERT INTO van_ban_phap_luat 
            (chunk_id, ten_van_ban, chu_de, loai_van_ban, tinh_trang_hieu_luc, page_content, embedding, link_goc)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (chunk_id, ten_van_ban, chu_de, loai_van_ban, tinh_trang_hieu_luc, page_content, vector_list, link_goc)
        )
            
    # Commit lưu dữ kiện sau khi xử lý xong
    conn.commit()

    cur.close()
    conn.close()
    print("\nHOÀN TẤT TUYỆT ĐỐI! Toàn bộ chunk của bạn đã được nhúng thành Vector lớn trong PostgreSQL.")

if __name__ == "__main__":
    main()
