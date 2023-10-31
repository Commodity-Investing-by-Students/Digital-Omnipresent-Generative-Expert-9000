import re

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

HEADING_FONT_SIZE = 14  # You can adjust this value based on your PDFs

def is_heading(line, font_sizes):
    return all(size > HEADING_FONT_SIZE for size in font_sizes)

def is_text(line):
    return not line.startswith("[IMG]")  # Assuming "[IMG]" indicates an embedded image

def is_image(line):
    return line.startswith("[IMG]")

def is_citation(line, prev_line_type):
    return bool(re.match(r"^\[\d+\]", line) or prev_line_type == "is_citation")

def add_beginnig(latex_content):
    latex_content.append("\\documentclass{article}")
    latex_content.append("\\usepackage{graphicx}")
    latex_content.append("\\title{Soybean Weekly Update}")
    latex_content.append("\\author{By DOGE-9000}")
    latex_content.append("\\date{October 2023}")
    latex_content.append("\\begin{document}")
    latex_content.append("\\maketitle")


def add_end(latex_content):
    latex_content.append("\\end{document}")


def read_through_pdf(pdf_path):
    
    latex_content = []
    add_beginnig(latex_content)
    prev_line_type = None

    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    line = ''.join([char.get_text() for char in text_line])
                    font_sizes = [char.size for char in text_line if isinstance(char, LTChar)]

                    if is_heading(line, font_sizes):
                        latex_content.append(f"\\section{{{line}}}")
                        prev_line_type = "heading"
                        
                    elif is_image(line):
                        latex_content.append(f"\\includegraphics{{{line[5:]}}}")  # Assuming after "[IMG]" is the image path
                        prev_line_type = "image"

                    elif is_citation(line, prev_line_type):
                        if prev_line_type == "citation":
                            prev_line_type = "citation"
                            latex_content.append(line)
                            #latex_content.append(f"\\cite{{{line[1:-1]}}}")
                            #prev_line_type = "citation"
                        else:
                            latex_content.append("\\section{{Sources}}")
                            latex_content[-1] += ' ' + line
                            prev_line_type = "citation"
                        
                    elif is_text(line):
                        if prev_line_type == "text":
                            latex_content[-1] += ' ' + line # Continue the existing paragraph without starting a new line
                            prev_line_type = "text"
                        else:
                            latex_content.append(line)
                            prev_line_type = "text"
    
    add_end(latex_content)
    return '\n'.join(latex_content)

def main():
    
    inputfile = input("Please input .pdf file: ")
    pdf_content = read_through_pdf(inputfile)
    
    with open('output.tex', 'w', encoding='utf-8') as file:
        file.write(pdf_content)

if __name__ == "__main__":
    main()
