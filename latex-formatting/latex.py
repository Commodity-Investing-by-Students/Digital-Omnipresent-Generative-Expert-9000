import re
import os

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTImage, LTFigure, LTPage
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
    latex_content.append("\\title{Commodity Weekly Update}")
    latex_content.append("\\author{By DOGE-9000}")
    latex_content.append("\\date{October 2023}")
    latex_content.append("\\begin{document}")
    latex_content.append("\\maketitle")


def add_end(latex_content):
    latex_content.append("\\end{document}")

IMAGE_FOLDER = "image_folder"

def save_image_or_figure(element, image_counter, image_folder):
    """Save the image data from LTImage or image within LTFigure object to a file in image_folder."""
    if isinstance(element, LTFigure):
        # LTFigure objects can contain images, text, or other figures
        # Here we look for nested LTImage objects within
        for child in element:
            if isinstance(child, LTImage):
                return save_image_or_figure(child, image_counter, image_folder)
    elif isinstance(element, LTImage):
        # Save the image as before
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        image_filename = f"image_{image_counter}.png"  # Or .jpg if applicable
        image_path = os.path.join(image_folder, image_filename)
        with open(image_path, 'wb') as f:
            f.write(element.stream.get_rawdata())
        return image_filename
    return None

def extract_images_from_element(element, image_counter, image_folder):
    """Recursively traverse the PDF element tree to extract images."""
    if isinstance(element, LTImage):
        # Direct image found, save it
        return save_image_or_figure(element, image_counter, image_folder)
    elif isinstance(element, LTFigure):
        # Figure found, look for nested images
        for child in element:
            result = extract_images_from_element(child, image_counter, image_folder)
            if result:  # If an image is found within the figure
                return result
    elif isinstance(element, LTPage):
        # Page found, look for images or figures in all sub-elements
        for child in element:
            result = extract_images_from_element(child, image_counter, image_folder)
            if result:  # If an image is found within the page
                return result
    # No image found in this element
    return None

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
    image_counter = 0

    for page_layout in extract_pages(pdf_path):
        for element in page_layout:

            image_filename = extract_images_from_element(element, image_counter, IMAGE_FOLDER)
            if image_filename:  # If an image was found and saved
                add_image(latex_content, image_filename)
                prev_line_type = LineType.IMAGE
                image_counter += 1

            if isinstance(element, (LTImage, LTFigure)):  # Check for both image and figure
                image_filename = save_image_or_figure(element, image_counter, IMAGE_FOLDER)
                if image_filename:  # If an image was found and saved
                    add_image(latex_content, image_filename)
                    prev_line_type = LineType.IMAGE
                    image_counter += 1

            if isinstance(element, LTTextContainer): # For remaining text elements

                for text_line in element:

                    line = ''.join([char.get_text() for char in text_line])
                    font_sizes = [char.size for char in text_line if isinstance(char, LTChar)]

                    if is_heading(line, font_sizes):
                        latex_content.append(f"\\section{{{line}}}")
                        latex_content.append("\n")    
                        prev_line_type = LineType.HEADING

                    elif is_text(line, prev_line_type):

                        if prev_line_type == LineType.TEXT:
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

            latex_content.append("\n")    

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

