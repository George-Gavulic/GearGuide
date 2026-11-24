from langchain_docling.loader import DoclingLoader, ExportType
from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
import time
import psutil
import os

from Embeddings import Embeddings

# Initialize process tracking for memory usage
process = psutil.Process(os.getpid())

#Configure pipeline settings (disabling OCR speeds up digital text PDFs significantly)
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = False #don't look at the pdfs as immages

# Setup custom converter with a strict page range limit passed as a tuple (page_from, page_to)
# Not working but needed for implementation
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options,
            # page_range=(1, 20)  # Limiting test scope to first 20 pages
            #this has not been working so for testing I gave it a smaller pdf
        )
    }
)

dir_path = r'PDFdocs'
output_txt_path = "docling_output_preview2.md"

if not os.path.exists(dir_path):
    print(f"Directory '{dir_path}' not found!")
else:
    for path in os.listdir(dir_path):
        if not path.lower().endswith(".pdf"):
            continue
            
        file_path = os.path.join(dir_path, path)
        print(f"Processing first 20 pages with HybridChunker: {file_path}")

        # Instantiate DoclingLoader with ExportType.DOC_CHUNKS and HybridChunker
        loader = DoclingLoader(
            file_path=file_path,
            converter=converter,
            export_type=ExportType.DOC_CHUNKS,
            chunker=HybridChunker(max_tokens=512)  # Token limit per structural chunk
        )
        
        # --- START PERFORMANCE TRACKING ---
        start_time = time.time()
        initial_memory = process.memory_info().rss / (1024 * 1024) # Memory in MB

        # Load structural chunks (this handles both conversion and hybrid chunking)
        chunks = loader.load()

        elapsed_time = time.time() - start_time
        final_memory = process.memory_info().rss / (1024 * 1024)
        memory_delta = final_memory - initial_memory

        Embedings(chunks)

        # --- END PERFORMANCE TRACKING ---

        # # Format chunks for inspection, including their parent section breadcrumbs/metadata
        # formatted_output = []
        # for i, chunk in enumerate(chunks):
        #     chunk_header = f"--- CHUNK {i+1} [Metadata: {chunk.metadata}] ---\n"
        #     formatted_output.append(chunk_header + chunk.page_content)

        # full_markdown = "\n\n".join(formatted_output)

        # # Write the hybrid chunks to your review text file
        # with open(output_txt_path, "w", encoding="utf-8") as f:
        #     f.write(full_markdown)

        print(f"\n--- Performance Metrics ---")
        print(f"-> Processing Time: {elapsed_time:.2f} seconds")
        print(f"-> Memory Delta:    {memory_delta:.2f} MB")
        print(f"Successfully saved {len(chunks)} hybrid chunks to: {output_txt_path}")
        
        break # Stops after processing the first PDF file for testing