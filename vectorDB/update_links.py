import json
import psycopg2
import psycopg2.extras
from tqdm import tqdm
import os

# Cấu hình đường dẫn dữ liệu đã được chunking
DATA_PATH = r"d:\RAG\vectorDB\chungking\chunked_data.json"

# Cấu hình DB PostgreSQL
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "phapluat_rag"
DB_USER = "admin"
DB_PASS = "admin123"

def main():
    print("1. Đang kết nối Database PostgreSQL...")
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()
    
    # Đảm bảo cột link_goc tồn tại trước khi cập nhật
    print("\n2. Đang kiểm tra cấu trúc bảng van_ban_phap_luat...")
    cur.execute("ALTER TABLE van_ban_phap_luat ADD COLUMN IF NOT EXISTS link_goc VARCHAR(255);")
    conn.commit()
    
    print(f"\n3. Đọc dữ liệu từ: {DATA_PATH}...")
    if not os.path.exists(DATA_PATH):
        print(f"LỖI: Không tìm thấy file {DATA_PATH}!")
        return
        
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"   -> Đã tải thành công {len(data)} chunk dữ liệu pháp luật.")
    print("\n3. BẮT ĐẦU CẬP NHẬT LINK_GOC CHO CÁC VECTOR ĐÃ CÓ (KHÔNG RE-EMBED)...")
    
    updates = []
    for item in data:
        chunk_id = item.get("chunk_id", "")
        metadata = item.get("metadata", {})
        link_goc = metadata.get("link_goc", "")
        
        if chunk_id and link_goc:
            updates.append((link_goc, chunk_id))
            
    print(f"   -> Chuẩn bị cập nhật {len(updates)} bản ghi...")
    
    # Chia nhỏ dữ liệu ra để hiển thị thanh tiến trình tqdm (mỗi 1000 bản ghi)
    page_size = 10
    for i in tqdm(range(0, len(updates), page_size), desc="Tiến trình cập nhật DB"):
        batch = updates[i:i + page_size]
        psycopg2.extras.execute_batch(
            cur,
            "UPDATE van_ban_phap_luat SET link_goc = %s WHERE chunk_id = %s",
            batch,
            page_size=page_size
        )
            
    conn.commit()
    cur.close()
    conn.close()
    print("\nHOÀN TẤT TUYỆT ĐỐI! Toàn bộ Database của bạn đã được đính kèm link gốc thành công mà không cần embed lại.")

if __name__ == "__main__":
    main()
