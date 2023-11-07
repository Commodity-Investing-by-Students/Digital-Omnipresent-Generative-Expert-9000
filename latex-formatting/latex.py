import re
import os

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTImage
from enum import Enum, auto

HEADING_FONT_SIZE = 14  

from enum import Enum, auto

class LineType(Enum):
    TEXT = auto()
    HEADING = auto()
    IMAGE = auto()
    CITATION = auto()
    END = auto() 


def is_heading(line, font_sizes):
    return all(size > HEADING_FONT_SIZE for size in font_sizes)

def is_text(line, prev_line_type) :
    return not (line.startswith("[IMG]") or prev_line_type == "is_citation")  # Assuming "[IMG]" indicates an embedded image

def is_citation(line, prev_line_type):
    return bool(re.match(r"^\[\d+\]", line) or prev_line_type == "is_citation")

def add_beginning(latex_content):
    latex_content.append("\\documentclass{article}")
    latex_content.append("\\usepackage{graphicx}")
    latex_content.append("\\title{Soybean Weekly Update}")
    latex_content.append("\\author{By DOGE-9000}")
    latex_content.append("\\date{October 2023}")
    latex_content.append("\\begin{document}")
    latex_content.append("\\maketitle")


def add_end(latex_content):
    latex_content.append("\\end{document}")

IMAGE_FOLDER = "image_folder"

def save_image(lt_image, image_counter):
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)
    # Construct the filename
    image_filename = f"image_{image_counter}.png"  # Or .jpg if applicable
    image_path = os.path.join(IMAGE_FOLDER, image_filename)
    # Save the image data
    with open(image_path, 'wb') as f:
        f.write(lt_image.stream.get_rawdata())
    return image_filename

def add_image(latex_content, image_filename):
    """Write the LaTeX code to include the image in the document."""
    latex_content.append("\\begin{figure}")
    latex_content.append(f"\\includegraphics[width=\\textwidth]{{{os.path.join(IMAGE_FOLDER, image_filename)}}}")
    latex_content.append("\\end{figure}")

def escape_percent_signs(latex_content):
    return latex_content.replace('%', '\\%')

def read_through_pdf(pdf_path):
    
    latex_content = []
    add_beginning(latex_content)
    prev_line_type = LineType.TEXT

    for page_layout in extract_pages(pdf_path):
        for element in page_layout:

            if isinstance(element, LTImage): # For Image Detection
                image_filename = save_image(element, image_counter)
                add_image(latex_content, image_filename)
                prev_line_type = LineType.IMAGE
                image_counter += 1

            if isinstance(element, LTTextContainer): # For remaining text elements

                for text_line in element:

                    line = ''.join([char.get_text() for char in text_line])
                    font_sizes = [char.size for char in text_line if isinstance(char, LTChar)]

                    if is_heading(line, font_sizes):
                        latex_content.append(f"\\section{{{line}}}")
                        prev_line_type = LineType.HEADING

                    elif line.strip() == '': # Ghetto solution to petty problem
                        latex_content.append(" '\\\\ \n    '")
                        print("Blank Detected")

                    elif is_text(line, prev_line_type):
                        if (line.strip() == ''):
                            latex_content.append(" '\\\\ \n    '")
                            print("Blank Detected")
                            prev_line_type = LineType.TEXT
                        elif prev_line_type == LineType.TEXT:
                            latex_content[-1] += ' ' + line # Continue the existing paragraph without starting a new line
                            prev_line_type = LineType.TEXT
                        else:
                            latex_content.append(line)
                            prev_line_type = LineType.TEXT

                    elif is_citation(line, prev_line_type):
                        if prev_line_type != LineType.CITATION:
                            latex_content.append("\\section{{Sources}}")
                        latex_content.append(f"\\cite{{{line[1:-1]}}}")
                        prev_line_type = LineType.CITATION
                        
    add_end(latex_content)
    return '\n'.join(latex_content)

def convert(pdf_filename):
    pdf_content = read_through_pdf(pdf_filename)
    pdf_content = escape_percent_signs(pdf_content)
    tex_filename = os.path.splitext(pdf_filename)[0] + ".tex"

    with open(tex_filename, 'w', encoding='utf-8') as file:
        file.write(pdf_content)
    
    return tex_filename

if __name__ == "__main__":
    inputfile = input("Please input .pdf file: ")
    output_tex = convert(inputfile)
    print(f"Conversion complete. LaTeX file saved as: {output_tex}")

"""elif line == '' and prev_line_type == LineType.TEXT:
latex_content.append("\n")  # Add 2 blank lines to create a paragraph in LaTeX
latex_content.append("\n")
#print("Blank Detected")
"""