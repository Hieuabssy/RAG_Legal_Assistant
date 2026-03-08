import re
from typing import List, Dict, Any
from models import Chunk, ChunkMetadata
from parser import group_into_dieus, parse_dieu_into_khoans

def process_document(doc: Dict[Any, Any]) -> List[dict]:
    chunks = []
    
    toan_van = doc.get("Toàn văn", "")
    if not toan_van:
        return []
        
    link = doc.get("link", "")
    doc_id_match = re.search(r'ItemID=(\d+)', link)
    doc_id = doc_id_match.group(1) if doc_id_match else "unknown"
    
    chu_de_ten = doc.get("chu_de_ten", "")
    ten_van_ban = doc.get("Tên văn bản", "")
    
    thuoc_tinh = doc.get("Thuộc tính", {})
    so_ky_hieu = thuoc_tinh.get("Số ký hiệu", "")
    loai_van_ban = thuoc_tinh.get("Loại văn bản", "")
    ngay_co_hieu_luc = thuoc_tinh.get("Ngày có hiệu lực", "")
    tinh_trang_hieu_luc = thuoc_tinh.get("Tình trạng hiệu lực", "")
    co_quan_ban_hanh = thuoc_tinh.get("Cơ quan ban hành", "")

    dieus = group_into_dieus(toan_van)
    
    for dieu in dieus:
        khoans = parse_dieu_into_khoans(dieu["lines"])
        for khoan in khoans:
            chuong_so = dieu["chuong_so"]
            chuong_ten = dieu["chuong_ten"]
            dieu_so = dieu["dieu_so"]
            dieu_ten = dieu["dieu_ten"]
            khoan_so = khoan["khoan_so"]
            content = khoan["content"]
            
            # Format chunk_id
            chunk_id = f"doc_{doc_id}"
            if chuong_so:
                chunk_id += f"_chuong{chuong_so}"
            chunk_id += f"_dieu{dieu_so}"
            if khoan_so:
                chunk_id += f"_khoan{khoan_so}"
                
            # Format page_content
            page_content = f"[Văn bản]: {ten_van_ban}\n"
            if chuong_so:
                page_content += f"[Chương]: Chương {chuong_so} - {chuong_ten}\n"
            page_content += f"[Điều]: Điều {dieu_so} - {dieu_ten}\n"
            page_content += f"[Nội dung]:\n{content}"
            
            # Construct metadata
            metadata = ChunkMetadata(
                doc_id=doc_id,
                ten_van_ban=ten_van_ban,
                chu_de_ten=chu_de_ten,
                so_ky_hieu=so_ky_hieu,
                loai_van_ban=loai_van_ban,
                chuong_so=chuong_so,
                dieu_so=dieu_so,
                khoan_so=khoan_so,
                ngay_co_hieu_luc=ngay_co_hieu_luc,
                tinh_trang_hieu_luc=tinh_trang_hieu_luc,
                co_quan_ban_hanh=co_quan_ban_hanh,
                link_goc=link
            )
            
            # If khoan_so isn't applicable, omit it from the dictionary so it doesn't default to empty string
            metadata_dict = metadata.__dict__.copy()
            if not khoan_so:
                 metadata_dict.pop("khoan_so", None)
            
            chunk = Chunk(
                chunk_id=chunk_id,
                page_content=page_content,
                metadata=metadata_dict
            )
            chunks.append(chunk.to_dict())
            
    return chunks
