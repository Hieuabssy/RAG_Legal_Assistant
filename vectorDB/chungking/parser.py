import re

def parse_dieu_into_khoans(lines):
    """
    Splits the lines of a single 'Điều' into multiple 'Khoản' (Clauses) if applicable.
    Any text before the first '1. ' is treated as introductory text and prepended to all Khoản.
    """
    intro = []
    khoan_dict = {}  # dict to maintain order conceptually, using string keys for Khoản numbers
    current_khoan = None
    
    for line in lines:
        # Match lines starting with a number followed by a dot and a space (e.g., "1. ")
        m = re.match(r'^(\d+)\.\s+(.*)$', line)
        if m:
            current_khoan = m.group(1)
            khoan_dict[current_khoan] = [line]
        else:
            if current_khoan is None:
                intro.append(line)
            else:
                khoan_dict[current_khoan].append(line)
                
    if not khoan_dict:
        # No Khoản found, return the whole Article as one chunk
        return [{"khoan_so": "", "content": "\n".join(intro)}]
    
    results = []
    intro_text = "\n".join(intro)
    for k_so, k_lines in khoan_dict.items():
        content = "\n".join(k_lines)
        if intro_text:
            content = intro_text + "\n" + content
        results.append({"khoan_so": k_so, "content": content})
        
    return results

def group_into_dieus(text):
    """
    Parses the full text of a legal document into a list of dictionaries,
    each representing a 'Điều' (Article) and its associated Chapter.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    chuong_so = ""
    chuong_ten = ""
    
    dieus = []
    current_dieu = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for Chương (Chapter)
        m_chuong = re.match(r'^Chương\s+([IVXLCDM]+)(?:\s*[-:]?\s*(.*))?$', line, re.IGNORECASE)
        if m_chuong:
            chuong_so = m_chuong.group(1)
            chuong_ten = m_chuong.group(2) if m_chuong.group(2) else ""
            
            # If chapter title was empty on this line, it might be on the next line
            if not chuong_ten and i + 1 < len(lines):
                next_line = lines[i+1].lower()
                if not next_line.startswith("điều") and not next_line.startswith("chương"):
                    chuong_ten = lines[i+1]
                    i += 1 # Consume the next line
            i += 1
            continue
            
        # Check for Điều spread across multiple lines: "Điều\n1.\nTitle"
        if line.lower() == "điều" and i + 1 < len(lines):
            m_so = re.match(r'^(\d+)\.?$', lines[i+1])
            if m_so:
                d_so = m_so.group(1)
                d_ten = ""
                # Check if line i+2 exists and is the Title
                if i + 2 < len(lines):
                     next_next = lines[i+2]
                     if not re.match(r'^(\d+)\.', next_next) and not next_next.lower().startswith("điều") and not next_next.lower().startswith("chương"):
                         d_ten = next_next
                         i += 3
                     else:
                         i += 2
                else:
                     i += 2
                
                if current_dieu:
                    dieus.append(current_dieu)
                current_dieu = {
                    "chuong_so": chuong_so,
                    "chuong_ten": chuong_ten,
                    "dieu_so": d_so,
                    "dieu_ten": d_ten,
                    "lines": []
                }
                continue
                
        # Check for Điều on a single line: "Điều 1. Title"
        m_dieu_single = re.match(r'^Điều\s+(\d+)[.:]?\s*(.*)$', line, re.IGNORECASE)
        if m_dieu_single:
            d_so = m_dieu_single.group(1)
            d_ten = m_dieu_single.group(2)
            
            # If title is empty on this line, check next line
            if not d_ten and i + 1 < len(lines):
                 next_line = lines[i+1]
                 if not re.match(r'^(\d+)\.', next_line) and not next_line.lower().startswith("điều") and not next_line.lower().startswith("chương"):
                     d_ten = next_line
                     i += 2
                 else:
                     i += 1
            else:
                 i += 1
                 
            if current_dieu:
                dieus.append(current_dieu)
            current_dieu = {
                "chuong_so": chuong_so,
                "chuong_ten": chuong_ten,
                "dieu_so": d_so,
                "dieu_ten": d_ten,
                "lines": []
            }
            continue
            
        if current_dieu is not None:
            current_dieu["lines"].append(line)
        
        i += 1
        
    if current_dieu:
        dieus.append(current_dieu)
        
    return dieus
