import pymupdf4llm
import os
import time
import psutil
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Get the current Python process to track resource usage
process = psutil.Process(os.getpid())

dir_path = r'PDFdocs'
output_txt_path = "pymupdf4llm_full_output.md"
output_txt_path2 = "markdownToChunks_full.md"

if not os.path.exists(dir_path):
    print(f"Directory '{dir_path}' not found!")
else:
    for path in os.listdir(dir_path):
        if not path.lower().endswith(".pdf"):
            continue
            
        file_path = os.path.join(dir_path, path)
        print(f"Processing entire PDF with PyMuPDF4LLM: {file_path}")

        # --- STEP 1: MARKDOWN EXTRACTION ---
        start_time_extraction = time.time()
        initial_memory = process.memory_info().rss / (1024 * 1024) # in MB

        # Extract ALL pages (remove 'pages' parameter to parse the whole book)
        markdown_text = pymupdf4llm.to_markdown(
            file_path, 
            draw_images=False
        )

        extraction_duration = time.time() - start_time_extraction
        extraction_memory = (process.memory_info().rss / (1024 * 1024)) - initial_memory

        with open(output_txt_path, "w", encoding="utf-8") as f:
            f.write(markdown_text)

        print(f"-> Extraction completed in: {extraction_duration:.2f} seconds")
        print(f"-> Estimated Memory Delta: {extraction_memory:.2f} MB")

        # --- STEP 2: STRUCTURAL & RECURSIVE CHUNKING ---
        start_time_chunking = time.time()

        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        header_splits = markdown_splitter.split_text(markdown_text)

        chunk_size = 1000
        chunk_overlap = 200
        recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )

        final_chunks = recursive_splitter.split_documents(header_splits)

        chunking_duration = time.time() - start_time_chunking

        print(f"-> Chunking completed in: {chunking_duration:.2f} seconds ({len(final_chunks)} chunks created)")

        with open(output_txt_path2, "w", encoding="utf-8") as f:
            for i, chunk in enumerate(final_chunks):
                f.write(f"--- CHUNK {i + 1} ---\n")
                f.write(f"Metadata: {chunk.metadata}\n")
                f.write(f"{chunk.page_content}\n\n")

        break  # Processed the target file