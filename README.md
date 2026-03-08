# RAG Legal Assistant (Hệ Thống RAG Tư Vấn Pháp Luật)

Đây là hệ thống Chatbot/trợ lý pháp luật sử dụng kiến trúc **Retrieval-Augmented Generation (RAG)**. 
Dự án bao gồm 3 thành phần chính:
- **Cơ sở dữ liệu Vector**: PostgreSQL với extension `pgvector`.
- **Backend**: FastAPI (Python) cung cấp API, xử lý Embedding và tương tác với LLM (Gemini).
- **Frontend**: Giao diện người dùng Web xây dựng bằng ReactJS & Vite.

---

## Phần 1: Chuẩn Bị Dữ Liệu (Bắt Buộc Cho Lần Đầu Tiên)

Hệ thống cần có dữ liệu trước khi có thể hoạt động tư vấn. Nếu Database của bạn chưa có sẵn dữ liệu, hãy thực hiện lần lượt các bước sau:

**1. Thu thập dữ liệu (Crawling):**
Hệ thống sẽ tải toàn bộ văn bản pháp luật được khai báo trong file danh sách liên kết.

```bash
#Di chuyển vào thư mục `craw data`
cd craw data
pip install -r requirements.txt
python craw_data.py
```

**2. Phân đoạn dữ liệu (Chunking):**

```bash
cd vectorDB
pip install -r requirements.txt
cd chungking
python main.py
```
**3. Lưu trữ vào Database (Ingestion):**

```bash
cd vectorDB
# Khởi động cơ sở dữ liệu pgvector bằng Docker trước
docker-compose up -d

# Cài đặt thư viện và nạp dữ liệu vào Database
pip install -r requirements.txt
python ingest_data.py
```
---

## Phần 2: Khởi Chạy Hệ Thống RAG

### Cách 1: Chạy dự án bằng Docker (Khuyên dùng)
Phù hợp khi bạn muốn khởi chạy toàn bộ hệ thống bằng 1 lệnh duy nhất hoặc triển khai lên máy chủ.

Yêu cầu: Đã cài đặt Docker Desktop và đang mở chạy ngầm.

1. Bật phần mềm Docker Desktop.
2. Mở Terminal/CMD tại thư mục gốc của dự án.
3. Chạy lệnh:
   ```bash
   docker-compose up --build -d
   ```
4. Truy cập giao diện ứng dụng tại: http://localhost
(Backend tự động chạy ở cổng 8000 nội bộ và Frontend Nginx phục vụ ở cổng 80).
Lưu ý: Để dừng hệ thống: `docker-compose down`.

### Cách 2: Chạy dự án thủ công
Phù hợp khi đang viết code lập trình hoặc thao tác kiểm thử từng thành phần.

**2.1. Mở Cơ sở dữ liệu (VectorDB)**
Bắt buộc phải bật database bằng Docker.
```bash
# Di chuyển vào thư mục vectorDB 
cd vectorDB

# Bật database pgvector 
docker-compose up -d
```
(Lưu ý: Bạn cũng có thể dùng file `docker-compose.yml` ở thư mục gốc như Cách 1 để khởi động Database).

**2.2. Chạy Backend (Python/FastAPI)**
Mở một Terminal/CMD mới:
```bash
# Di chuyển vào thư mục backend
cd backend

# Cài đặt thư viện
pip install -r requirements.txt

# Khởi chạy Server (Nhớ cấu hình file .env có chứa GEMINI_API_KEY)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
API của bạn sẽ chạy tại: http://localhost:8000. Bạn có thể xem tài liệu API tại http://localhost:8000/docs.

**2.3. Chạy Frontend (React/Vite)**
Mở tiếp một Terminal/CMD mới:
```bash
# Di chuyển vào thư mục frontend/rag_app
cd frontend/rag_app

# Cài đặt các gói thư viện Node
npm install

# Khởi chạy server phát triển giao diện
npm run dev
```
Giao diện Web sẽ xuất hiện tại đường dẫn hiển thị trên terminal (thường là http://localhost:5173).
