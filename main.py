file_path = '/Users/alv/Documents/Scripts/PDFtoHTML/mgb_catalog_web.pdf'
from pdf2image import convert_from_path
import pytesseract
import re

# First, convert PDF to images
images = convert_from_path(file_path)

# Define a regex pattern for your codes
pattern = re.compile(r'\d{3}-\d{3}')

# Define the offset (in pixels) for the clickable area
offset = 10

# Then process each image
for i, image in enumerate(images):
    # Save the image to a file
    filename = f'page{i}.png'
    image.save(filename)

    print(f'<img src="{filename}" usemap="#map{i}" alt="Page {i}">')
    print(f'<map name="map{i}">')

    # Use OCR to find text in the image
    d = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    # For each detected text region
    for j in range(len(d['text'])):
        # If the region contains a match to the pattern
        matched_text = pattern.search(d['text'][j])
        if matched_text:
            # Get the bounding box of the text region
            left = d['left'][j] - offset
            top = d['top'][j] - offset
            width = d['width'][j] + (2 * offset)
            height = d['height'][j] + (2 * offset)

            # Create an id for the area
            id = f"part_num_{matched_text.group().replace('-', '_')}"

            # Write out an HTML image map or some other HTML structure
            # that makes this region clickable
            print(f'<area id="{id}" shape="rect" coords="{left},{top},{left + width},{top + height}" href="your_link.html">')
            print(f'<div id="{id}_div" class="clickable_area" style="position:absolute; left:{left}px; top:{top}px; width:{width}px; height:{height}px;"></div>')

    print('</map>')

    if i == 5:
        break
