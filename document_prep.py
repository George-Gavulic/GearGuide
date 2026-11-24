from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from langchain_docling.loader import DoclingLoader, ExportType

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_chroma import Chroma
from uuid import uuid4

import time
import psutil
import os 





process = psutil.Process(os.getpid())

# Configure pipeline settings (disabling OCR speeds up digital text PDFs significantly)
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = False 

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options
        )
    }
)






print("Loading embedding model...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2", 
    encode_kwargs={"normalize_embeddings": True}
)

vector_store = Chroma(
    collection_name="2004_buick_lesabre",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)






def index_chunks_to_chroma(chunks):
    """Takes Docling chunks, generates UUIDs, and adds them to Chroma."""
    print(f"Indexing {len(chunks)} chunks into Chroma vector store...")

    # --- START PERFORMANCE TRACKING ---
    start_time = time.time()
    initial_memory = process.memory_info().rss / (1024 * 1024) # Memory in MB

    # getting source, headings, and page number out of the metadata
    for chunk in chunks:
        dl_meta = chunk.metadata.get("dl_meta", {})

        # Gather headings if present in Docling's dl_meta
        headings = dl_meta.get("headings", [])
        # Join headings into a readable string or take the primary heading
        chunk.metadata["heading"] = " > ".join(headings) if headings else "General"

        # Gather page numbers from provenance (doc_items -> prov -> page_no)
        doc_items = dl_meta.get("doc_items", [])
        page_no = 1
        for item in doc_items:
            for prov in item.get("prov", []):
                if "page_no" in prov:
                    page_no = int(prov["page_no"])
                    break
            else:
                continue
            break
        
        # Store as a comma-separated string or list (Chroma supports lists of strings/ints)
        # Uncommon but the chunk may go accross multiple pages so we will need a list
        chunk.metadata["page_numbers"] = page_no

        # Keeping source clean
        source_path = chunk.metadata.get("source", "")
        chunk.metadata["source"] = os.path.basename(source_path)

    cleaned_chunks = filter_complex_metadata(chunks)
    
    # Chroma's add_documents takes LangChain Document objects directly.
    # DoclingLoader already outputs chunks as LangChain Documents with page_content and metadata.
    uuids = [str(uuid4()) for _ in range(len(cleaned_chunks))]
    vector_store.add_documents(documents=cleaned_chunks, ids=uuids)

    elapsed_time = time.time() - start_time
    final_memory = process.memory_info().rss / (1024 * 1024)
    memory_delta = final_memory - initial_memory

    print("Successfully indexed chunks into Chroma!")
    print(f"\n--- Embedding Performance Metrics ---")
    print(f"-> Processing Time: {elapsed_time:.2f} seconds")
    print(f"-> Memory Delta:    {memory_delta:.2f} MB")

    # TEMP just for demop
    # formatted_output = []
    # output_txt_path = "docling_cleaned_output_preview2.md"
    # for i, chunk in enumerate(cleaned_chunks):
    #     chunk_header = f"--- CHUNK {i+1} [Metadata: {chunk.metadata}] ---\n"
    #     formatted_output.append(chunk_header + chunk.page_content)

    # full_markdown = "\n\n".join(formatted_output)

    # # Write the hybrid chunks to your review text file
    # with open(output_txt_path, "w", encoding="utf-8") as f:
    #     f.write(full_markdown)






dir_path = r'PDFdocs'

if not os.path.exists(dir_path):
    print(f"Directory '{dir_path}' not found!")
else:
    for path in os.listdir(dir_path):
        if not path.lower().endswith(".pdf"):
            continue
            
        file_path = os.path.join(dir_path, path)
        print(f"Processing PDF with Docling HybridChunker: {file_path}")

        # Instantiate DoclingLoader with ExportType.DOC_CHUNKS and HybridChunker
        loader = DoclingLoader(
            file_path=file_path,
            converter=converter,
            export_type=ExportType.DOC_CHUNKS,
            chunker=HybridChunker(max_tokens=512)
        )
        
        # --- START PERFORMANCE TRACKING ---
        start_time = time.time()
        initial_memory = process.memory_info().rss / (1024 * 1024) # Memory in MB

        # Load structural chunks (conversion + hybrid chunking)
        chunks = loader.load()

        elapsed_time = time.time() - start_time
        final_memory = process.memory_info().rss / (1024 * 1024)
        memory_delta = final_memory - initial_memory

        print(f"\n--- Docling Performance Metrics ---")
        print(f"-> Processing Time: {elapsed_time:.2f} seconds")
        print(f"-> Memory Delta:    {memory_delta:.2f} MB")
        print(f"-> Total Chunks:    {len(chunks)}")

        # Pass chunks to our indexing function
        index_chunks_to_chroma(chunks)
        
        break # Stop after processing the first PDF file for testing