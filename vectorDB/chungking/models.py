from dataclasses import dataclass

@dataclass
class ChunkMetadata:
    doc_id: str
    ten_van_ban: str
    chu_de_ten: str
    so_ky_hieu: str
    loai_van_ban: str
    chuong_so: str
    dieu_so: str
    khoan_so: str
    ngay_co_hieu_luc: str
    tinh_trang_hieu_luc: str
    co_quan_ban_hanh: str
    link_goc: str

@dataclass
class Chunk:
    chunk_id: str
    page_content: str
    metadata: dict

    def to_dict(self):
        return {
            "chunk_id": self.chunk_id,
            "page_content": self.page_content,
            "metadata": self.metadata
        }
