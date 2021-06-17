
# Found some part of the solution from here: https://stackoverflow.com/questions/2925484/place-image-over-pdf
from reportlab.pdfgen import canvas # Use "pip install reportlab"
from PyPDF2 import PdfFileWriter, PdfFileReader # Use "pip install pypdf2"

# Define targets
input_file = "input.pdf"
output_file = input_file.replace(".pdf", "_signed.pdf")

# Create PDF Reader and Writer
output = PdfFileWriter()
input = PdfFileReader(open(input_file, "rb"))

# Get number of pages in input document
page_count = input.getNumPages()
# Go through all the input file pages to add a watermark to them
for page_number in range(page_count):

    # Get the individual page
    curr_page = input.getPage(page_number)
    # Get dimensions of that page
    dims = curr_page.mediaBox # https://stackoverflow.com/questions/6230752/extracting-page-sizes-from-pdf-in-python

    # Create the watermark from an image using reportlab
    c = canvas.Canvas('watermark.pdf', pagesize=(dims[2],dims[3]))
    c.drawImage('watermark.png', round(dims[2]/2-100), 10)
    c.save()

    print(f"Watermarking page {page_number} of {page_count}")
    # Get the watermark file you just created
    watermark = PdfFileReader(open("watermark.pdf", "rb"))
    # Merge
    curr_page.mergePage(watermark.getPage(0))
    # Add page from input file to output document
    output.addPage(curr_page)


# Finally, write "output" to the actual output file
with open(output_file, "wb") as f:
    output.write(f)
