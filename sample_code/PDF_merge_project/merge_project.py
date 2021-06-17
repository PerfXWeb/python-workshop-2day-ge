
# Found some part of the solution here: https://stackoverflow.com/questions/22795091/how-to-append-pdf-pages-using-pypdf2/29871560
from PyPDF2 import PdfFileReader, PdfFileWriter # Use "pip install pypdf2"
import os # Already pre-installed, no need to install anything

# Define targets
directory = "PDFs" # this directory has to already exist
output_file = "PDF_merged.pdf"

# Create PDF Writer
output = PdfFileWriter()

# Go through every file in our directory
for filename in os.listdir(directory):
    # Check if the file is a PDF file
    if ".pdf" in filename.lower():
        # Get the PDF file as a variable
        input = PdfFileReader(open(os.path.join(directory,filename), 'rb'))
        # Get number of pages in input document
        page_count = input.getNumPages()
        # Go through every page in the file individually
        for page_number in range(page_count):
            print(f"Appending {filename} page {page_number+1} of {page_count}")
            # Append the current page of the current file
            output.addPage(input.getPage(page_number))

# Finally, write "output" to the actual output file
with open(output_file, "wb") as f:
    output.write(f)
