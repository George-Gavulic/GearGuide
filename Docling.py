from langchain_docling.loader import DoclingLoader, ExportType
from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
import time
import psutil
import os

# Initialize process tracking for memory usage
process = psutil.Process(os.getpid())

# 1. Configure pipeline settings (disabling OCR speeds up digital text PDFs significantly)
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = False 

# 2. Setup custom converter with a strict page range limit passed as a tuple (page_from, page_to)
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options,
            page_range=(1, 20)  # Limiting test scope to first 20 pages
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

        # 3. Instantiate DoclingLoader with ExportType.DOC_CHUNKS and HybridChunker
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
        # --- END PERFORMANCE TRACKING ---

        # Format chunks for inspection, including their parent section breadcrumbs/metadata
        formatted_output = []
        for i, chunk in enumerate(chunks):
            chunk_header = f"--- CHUNK {i+1} [Metadata: {chunk.metadata}] ---\n"
            formatted_output.append(chunk_header + chunk.page_content)

        full_markdown = "\n\n".join(formatted_output)

        # Write the hybrid chunks to your review text file
        with open(output_txt_path, "w", encoding="utf-8") as f:
            f.write(full_markdown)

        print(f"\n--- Performance Metrics ---")
        print(f"-> Processing Time: {elapsed_time:.2f} seconds")
        print(f"-> Memory Delta:    {memory_delta:.2f} MB")
        print(f"Successfully saved {len(chunks)} hybrid chunks to: {output_txt_path}")
        
        break # Stops after processing the first PDF file for testing
        
# from langchain_docling.loader import DoclingLoader
# import os

# dir_path = r'PDFdocs'

# # for path in os.listdir(dir_path):
# #     if not path.lower().endswith(".pdf"):
# #         continue
#     # file_path = os.path.join(dir_path, path)

#     # loader = DoclingLoader(file_path=file_path)

# FILE_PATH = "https://arxiv.org/pdf/2408.09869"

# loader = DoclingLoader(file_path=FILE_PATH)

#     # lanchain code
#     # loads the doc all at once, there is a lazy load option
#     # ToDo test if vvv needs to be in loop
# docs = loader.load()

# for d in docs[:3]:
#     print(f"- {d.page_content=}")




# # FILE_PATH = "https://arxiv.org/pdf/2408.09869"

# # loader = DoclingLoader(file_path=FILE_PATH)







# # from pypdf import PdfReader
# # import os

# # dir_path = r'PDFdocs'
# # output_dir = r'output_images'
# # count = 0

# # def main():
# #     process_pdfs()
# #     pass

# # def process_pdfs():
# #     for path in os.listdir(dir_path):
# #         if not path.lower().endswith(".pdf"):
# #             continue
# #             # the code os.path.join combines args into past based on the operating system / for linus \ for windows
# #         file_path = os.path.join(dir_path, path)
# #         reader = PdfReader(file_path)
# #         print(f"Processing '{path}' - Pages: {len(reader.pages)}")
# #         extract_images(reader, output_dir, tempstart, tempstop)

# # def extract_images(reader, output_dir, page_start, page_stop):
# #     global count
# #     for page_num, page in enumerate(reader.pages[page_start:page_stop]):
# #         for image_file_object in page.images:
# #             try:
# #                 count += 1
# #                 # image_file_object.name includes the proper extension (e.g., 'Im1.jpg' or 'Im2.png')
# #                 out_filename = f"{count}_p{page_num + 1}_{image_file_object.name}"
# #                 out_path = os.path.join(output_dir, out_filename)

# #                 with open(out_path, "wb") as fp:
# #                     fp.write(image_file_object.data)

# #                 print(f"Saved: {out_filename}")
# #             except Exception as exception:
# #                 print(f"Error on page {page_num + 1} image '{image_file_object.name}': {exception}")


# # # only run this if the pdf page numbers are settup to be sectioned instead of pages
# # # detect before calling or something else
# # def extract_sections(reader, page_start, page_stop):
# #     page = reader.pages[page_start:page_stop].extract_text()
# #     section_num = 0
# #     print(section_num)