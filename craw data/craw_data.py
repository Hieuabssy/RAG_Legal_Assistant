import json
import time
import os
import urllib.request
from bs4 import BeautifulSoup
from urllib.error import URLError

def get_html(url, retries=3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
            return html
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                print(f"Failed to fetch {url}: {e}")
                return ""
    return ""

def extract_toanvan(html):
    if not html: return ""
    soup = BeautifulSoup(html, "html.parser")
    content_div = soup.find('div', class_='toanvancontent')
    if not content_div:
        content_div = soup.find('div', id='toanvancontent')
    if content_div:
        # User wants the whole content. Using get_text with separator to preserve formatting
        return content_div.get_text(separator='\n', strip=True)
    return ""

def extract_thuoctinh(html):
    data = {
        "Số ký hiệu": "",
        "Ngày ban hành": "",
        "Loại văn bản": "",
        "Ngày có hiệu lực": "",
        "Nguồn thu thập": "",
        "Ngày đăng công báo": "",
        "Cơ quan ban hành": "",
        "Chức danh": "",
        "Người ký": "",
        "Phạm vi": "",
        "Thông tin áp dụng": "",
        "Tình trạng hiệu lực": ""
    }
    if not html: return data
    soup = BeautifulSoup(html, "html.parser")
    
    # 1. Tình trạng hiệu lực
    info_div = soup.find('div', class_='vbInfo')
    if info_div:
        for li in info_div.find_all('li'):
            if 'Hiệu lực:' in li.text:
                data["Tình trạng hiệu lực"] = li.text.replace('Hiệu lực:', '').strip()
                break

    # 2. Metadata table
    tables = soup.find_all('table')
    target_table = None
    for t in tables:
        if "Số ký hiệu" in t.text or "Ngày ban hành" in t.text:
            target_table = t
            break
            
    if target_table:
        rows = target_table.find_all('tr')
        for r in rows:
            cells = r.find_all(['th', 'td'])
            if not cells: continue
            
            # Check the first cell for the label
            first_cell_text = cells[0].text.strip().replace(':', '')
            
            if "Cơ quan ban hành" in first_cell_text or "Người ký" in first_cell_text:
                # Based on user feedback:
                # td 0: label
                # td 1: Cơ quan ban hành
                # td 2: Chức danh
                # td 3: Người ký
                if len(cells) > 1:
                    data["Cơ quan ban hành"] = cells[1].text.strip()
                if len(cells) > 2:
                    data["Chức danh"] = cells[2].text.strip()
                if len(cells) > 3:
                    data["Người ký"] = cells[3].text.strip()
            else:
                # Traditional 2-column key-value format
                if len(cells) >= 2:
                    for i in range(0, len(cells)-1, 2):
                        key = cells[i].text.strip().replace(':', '')
                        val = " - ".join([x.strip() for x in cells[i+1].stripped_strings if x.strip()])
                        for k in data.keys():
                            if k in key and k not in ["Cơ quan ban hành", "Chức danh", "Người ký", "Tình trạng hiệu lực"]:
                                data[k] = val
                                break
    return data

def extract_vanbanlienquan(html, current_url):
    results = []
    if not html: return results
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all('tr')
    
    seen_links = set()
    
    for r in rows:
        label_td = r.find('td', class_='label')
        if label_td:
            relation_type = label_td.text.strip()
            ul_list = r.find('ul', class_='listVB')
            if ul_list:
                items = ul_list.find_all('li', recursive=False)
                for item in items:
                    a_tag = item.find('a')
                    if a_tag and 'href' in a_tag.attrs:
                        href = a_tag['href']
                        if 'vbpq-toanvan.aspx' in href:
                            title = a_tag.text.strip()
                            link = "http://vbpl.vn" + href if href.startswith('/') else href
                            
                            # Loại bỏ chính văn bản đang xem và chống lặp
                            if current_url in link or link in seen_links:
                                continue
                                
                            seen_links.add(link)
                            results.append({
                                "Tên văn bản": title,
                                "link": link,
                                "Loại quan hệ": relation_type
                            })
    return results

def crawl_all(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data_json = json.load(f)
    
    total_docs = sum(len(chu_de.get('danh_sach_van_ban', [])) for chu_de in data_json)
    print(f"Bắt đầu crawl {total_docs} văn bản pháp luật...")
    processed = 0

    # Initialize file with empty array
    if not os.path.exists(output_file):
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("[\n")
    else:
        # If resuming/overwriting, we just start fresh
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("[\n")

    first_item = True

    for chu_de in data_json:
        for vb in chu_de.get('danh_sach_van_ban', []):
            url_toanvan = vb.get('link', '')
            if not url_toanvan:
                continue
                
            url_thuoctinh = url_toanvan.replace('vbpq-toanvan.aspx', 'vbpq-thuoctinh.aspx')
            url_vanbanlienquan = url_toanvan.replace('vbpq-toanvan.aspx', 'vbpq-vanbanlienquan.aspx')
            
            html_toanvan = get_html(url_toanvan)
            html_thuoctinh = get_html(url_thuoctinh)
            html_vblq = get_html(url_vanbanlienquan)
            
            toanvan = extract_toanvan(html_toanvan)
            thuoctinh = extract_thuoctinh(html_thuoctinh)
            vanban_lq = extract_vanbanlienquan(html_vblq, url_toanvan)
            
            doc_data = {
                "chu_de_id": chu_de.get("chu_de_id", ""),
                "chu_de_ten": chu_de.get("chu_de_ten", ""),
                "de_muc_id": chu_de.get("de_muc_id", ""),
                "de_muc_ten": chu_de.get("de_muc_ten", ""),
                "link": url_toanvan,
                "Tên văn bản": vb.get('ten_van_ban', ''),
                "Toàn văn": toanvan,
                "Thuộc tính": thuoctinh,
                "Văn bản liên quan": vanban_lq
            }
            
            # Save immediately
            with open(output_file, "a", encoding="utf-8") as f:
                if not first_item:
                    f.write(",\n")
                json.dump(doc_data, f, ensure_ascii=False, indent=4)
            first_item = False
            
            processed += 1
            print(f"Đã xử lý và lưu {processed}/{total_docs}: {vb.get('ten_van_ban', '')[:50]}...")
            time.sleep(1)

    # Close the JSON array
    with open(output_file, "a", encoding="utf-8") as f:
        f.write("\n]")
        
    print(f"Hoàn thành toàn bộ, kết quả nằm trong {output_file}")

if __name__ == "__main__":
    input_file = "link_vb.json"
    output_file = "crawled_data_copy.json"
    crawl_all(input_file, output_file)
