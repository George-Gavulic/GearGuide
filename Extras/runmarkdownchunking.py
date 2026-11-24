from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Assume 'markdown_text' is the output string from pymupdf4llm.to_markdown()
output_txt_path = "markdownToChunks.md"

markdown_text

# Define the headers you want to split and track as metadata
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

# 2. Instantiate the Markdown header splitter
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# This splits the document into chunks grouped by its structural headings
header_splits = markdown_splitter.split_text(markdown_text)

# 3. (Optional) If any resulting section chunk is still too large for your embedding model,
# pass them through a recursive character splitter to keep chunk sizes ideal for your vector DB
chunk_size = 1000
chunk_overlap = 200

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size, 
    chunk_overlap=chunk_overlap
)

final_chunks = recursive_splitter.split_documents(header_splits)

print(f"Successfully created {len(final_chunks)} structured chunks ready for vector indexing!")

with open(output_txt_path, "w", encoding="utf-8") as f:
    f.write(final_chunks)