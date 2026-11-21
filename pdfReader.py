from pypdf import PdfReader
import os

dir_path = r'PDFdocs'
output_dir = r'output_images'
count = 0

def main():
    process_pdfs()
    pass

def process_pdfs():
    for path in os.listdir(dir_path):
        if not path.lower().endswith(".pdf"):
            continue
            # the code os.path.join combines args into past based on the operating system / for linus \ for windows
        file_path = os.path.join(dir_path, path)
        reader = PdfReader(file_path)
        print(f"Processing '{path}' - Pages: {len(reader.pages)}")
        tempstart =0
        tempstop = 12
        extract_images(reader, output_dir, tempstart, tempstop)
        # extract_sections(reader, tempstart, tempstop)

        # page = reader.pages[0:12].extract_text(visitor_text=visitor_footer)
        # footer_text = "".join(footer_parts)
        # print(footer_text)



def visitor_footer(text, cm, tm, font_dict, font_size):
    # Multiply text matrix (tm) and current transformation matrix (cm)
    txt2user = mult(tm, cm)
    y = txt2user[5]  # Vertical position on the page

    # Keep text located in the bottom 50 points of the page
    if 0 < y < 50:
        footer_parts.append(text)

    # print(f"Pages: {len(reader.pages)}")
    # text = reader.pages[0].extract_text()
    # print(text[:7000])




    # page = reader.pages[2]

    # for i, image_file_object in enumerate(page.images):
    #     file_name = "out-image-" + str(i) + "-" + image_file_object.name
    #     image_file_object.image.save(file_name)



    # check if current path is a PDF file
    # if path.endswith(".pdf"):
    #     count += 1
    #     # the code os.path.join combines args into past based on the operating system / for linus \ for windows
    #     file_path = os.path.join(dir_path, path)
    #     reader = PdfReader(file_path)
    #     print(f"File: {file_path}, Pages: {len(reader.pages)}")

def extract_images(reader, output_dir, page_start, page_stop):
    global count
    for page_num, page in enumerate(reader.pages[page_start:page_stop]):
        for image_file_object in page.images:
            try:
                count += 1
                # image_file_object.name includes the proper extension (e.g., 'Im1.jpg' or 'Im2.png')
                out_filename = f"{count}_p{page_num + 1}_{image_file_object.name}"
                out_path = os.path.join(output_dir, out_filename)

                with open(out_path, "wb") as fp:
                    fp.write(image_file_object.data)

                print(f"Saved: {out_filename}")
            except Exception as exception:
                print(f"Error on page {page_num + 1} image '{image_file_object.name}': {exception}")


# only run this if the pdf page numbers are settup to be sectioned instead of pages
# detect before calling or something else
def extract_sections(reader, page_start, page_stop):
    page = reader.pages[page_start:page_stop].extract_text()
    section_num = 0
    print(section_num)




if __name__ == "__main__":
    main()
