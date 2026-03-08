import json
import os
from processor import process_document

def main():
    input_file = r"d:\RAG\craw data\crawled_data.json"
    output_file = r"d:\RAG\vectorDB\chungking\chunked_data.json"
    
    print(f"Reading data from {input_file}...")
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to load input file: {e}")
        return
        
    all_chunks = []
    print(f"Loaded {len(data)} documents. Processing into chunks...")
    
    for i, doc in enumerate(data):
        doc_chunks = process_document(doc)
        all_chunks.extend(doc_chunks)
        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1} documents...")
            
    print(f"Total chunks created: {len(all_chunks)}")
    
    print(f"Saving chunked data to {output_file}...")
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, ensure_ascii=False, indent=2)
        print("Chunking completed successfully!")
    except Exception as e:
        print(f"Failed to save output file: {e}")

if __name__ == "__main__":
    main()
