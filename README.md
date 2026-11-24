# GearGuide

Current Dependancies

step 1
install python
run apt install python3-pypdf or pip install pypdf

install pillow for images




step 1 actual
Docling
needs C++ compiler (download the Microsoft C++ Build Tools installer)

the code docling package
pip install -qU langchain-docling

a docling-parse package which was not gathered automatically
pip install 'docling-slim[format-pdf-docling]'

# 1. Install the CPU version of PyTorch (required for Docling's layout AI models)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 2. Ensure Docling's PDF-parsing and layout tools are fully present
pip install 'docling-slim[format-pdf-docling]'

pip install docling-ibm-models

pip install "docling[all]"


1.2
PyMuPDF4LLM 

pip install pymupdf4llm
so many installs could not get working



1.3 
unstructured
# Install package, compatible with API partitioning
pip install -qU langchain-unstructured unstructured-client unstructured "unstructured[pdf]" python-magic


pip install "langchain-unstructured[local]"





Step 2 look at mem usage for each step
pip install psutil

