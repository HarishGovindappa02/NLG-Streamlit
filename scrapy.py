import os
import glob
import textwrap
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def txt_to_pdf(input_file, output_file):
    # Read the text from the .txt file
    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()

    # Wrap the text content to fit within the cell width
    cell_width = 450
    text_wrapped = "\n".join(textwrap.wrap(text, width=cell_width))

    # Split the wrapped text into lines to create table data
    table_data = [[line] for line in text_wrapped.split("\n")]

    # Create a SimpleDocTemplate object with specified page size (letter)
    doc = SimpleDocTemplate(output_file, pagesize=letter)

    # Create a Table with the table data
    table = Table(table_data, colWidths=[cell_width], rowHeights=None, style=[("ALIGN", (0, 0), (-1, -1), "LEFT")])

    # Set table style (optional)
    table.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("FONTSIZE", (0, 0), (-1, -1), 10),  # Adjust the font size as needed
    ]))

    # Build the PDF document with the table
    doc.build([table])

def convert_txt_files_to_pdf(input_folder, output_folder):
    # Get a list of all .txt files in the input folder and its subfolders
    txt_files = glob.glob(os.path.join(input_folder, "**", "*.txt"), recursive=True)

    # Loop through each .txt file and convert to .pdf
    for txt_file in txt_files:
        # Determine the output PDF file path
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(txt_file))[0] + ".pdf")

        # Convert the .txt file to .pdf
        txt_to_pdf(txt_file, output_file)



# Usage example
input_folder_path = "path/to/input/folder"
output_folder_path = "path/to/output/folder"
convert_txt_files_to_pdf(input_folder_path, output_folder_path)


# Usage example
input_folder_path = "Jobs_Text_Bengaluru"
output_folder_path = "scrapy"
convert_txt_files_to_pdf(input_folder_path, output_folder_path)
