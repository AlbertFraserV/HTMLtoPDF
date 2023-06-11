base_path = '/Users/alv/Documents/Scripts/PDFtoHTML'
pdf_dir = f'{base_path}/pdfs'
from pdf2image import convert_from_path
import pytesseract
import re
import os
import cv2
import numpy as np

for filename in os.listdir(pdf_dir):

    if filename.endswith('.pdf'):
        # First, convert PDF to images
        file_path = os.path.join(pdf_dir, filename)
        images = convert_from_path(file_path)

        # Define a regex pattern for your codes
        pattern_part_num = re.compile(r'\d{3}-\d{3}')
        pattern_table_of_contents = re.compile("Table of Contents", re.IGNORECASE)

        # Define the offset (in pixels) for the clickable area
        offset = 15

        with open(f'{base_path}/html/{filename.split(".")[0]}.html', 'w') as f:
            if not os.path.exists(f'{base_path}/html/images_{filename.split(".")[0]}'):
                os.mkdir(f'{base_path}/html/images_{filename.split(".")[0]}')
            f.write('<html>\n<body>\n')
            # Then process each image
            for i, image in enumerate(images):
                # Save the image to a file
                
                page_path = f'{base_path}/html/images_{filename.split(".")[0]}/page{i}.png'
                image.save(page_path)

                f.write(f'<img id="page_num_{i}" src="{page_path}" usemap="#map{i}" alt="Page {i}">')
                f.write(f'<map name="map{i}">')

                d = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

                text = d['text']
                page_numbers = {}
                try:
                    table_start = text.index('Table')
                    table_of_contents = i
                    table_end = text.index('Privacy')
                    table_text = text[table_start:table_end]
                    page_number_pattern = re.compile(r'^(\d+)(-\d+)?(?!\w)')
                    # Iterate over the pages
                    for words in table_text:
                        match = page_number_pattern.match(words)
                        if match:
                            # The first group captured by the pattern is the first number
                            first_number = int(match.group(1))
                            full_match = match.group(0)
                            page_numbers[full_match] = first_number
                    print(page_numbers)
                except ValueError:
                    pass

                # For each detected text region
                for j in range(len(d['text'])):
                    #Create Page anchors if it's a table of contents
                    if page_numbers and d['text'][j] in page_numbers:
                        left = d['left'][j] - offset
                        top = d['top'][j] - offset
                        width = d['width'][j] + (2 * offset)
                        height = d['height'][j] + (2 * offset)

                        # Create an id for the area
                        id = f"page_num_{d['text'][j]}"
                        page_jump = int(page_numbers[d['text'][j]]) + i - 1

                        # Write out an HTML image map or some other HTML structure
                        # that makes this region clickable
                        f.write(f'<area shape="rect" coords="{left},{top},{left + width},{top + height}" href="#page_num_{page_jump}">')
                        f.write(f'<div class="clickable_area" style="position:absolute; left:{left}px; top:{top}px; width:{width}px; height:{height}px;"></div>')

                    # If the region contains a match to the pattern
                    matched_part_num_text = pattern_part_num.search(d['text'][j])
                    if matched_part_num_text and matched_part_num_text.group() not in page_numbers:
                        # Get the bounding box of the text region
                        left = d['left'][j] - offset
                        top = d['top'][j] - offset
                        width = d['width'][j] + (2 * offset)
                        height = d['height'][j] + (2 * offset)

                        # Create an id for the area
                        id = f"part_num_{matched_part_num_text.group().replace('-', '_')}"

                        # Write out an HTML image map or some other HTML structure
                        # that makes this region clickable
                        f.write(f'<area id="{id}" shape="rect" coords="{left},{top},{left + width},{top + height}" href="your_link.html">')
                        f.write(f'<div id="{id}_div" class="clickable_area" style="position:absolute; left:{left}px; top:{top}px; width:{width}px; height:{height}px;"></div>')
                
                f.write('</map>')
            f.write("""
                <div id="modal" style="display: none; position: fixed; z-index: 1; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.4);">
                <div style="background-color: #fefefe; margin: 15% auto; padding: 20px; border: 1px solid #888; width: 30%;">
                    <h2>Enter Details</h2>
                    <label for="quantity">Quantity:</label><br>
                    <input type="text" id="quantity" name="quantity"><br>
                    <label for="invoice">Invoice #:</label><br>
                    <input type="text" id="invoice" name="invoice"><br>
                    <label for="part">Part #:</label><br>
                    <input type="text" id="part" name="part" readonly><br>
                    <button id="submitBtn">Submit</button>
                    <button id="cancelBtn">Cancel</button>
                </div>
            </div>
            """)
            f.write("""
                <div id="jumpBox">
                    <input type="number" id="pageNumber" min="1">
                    <button onclick="jumpToPage()">Jump</button>
                </div>
            """)
            f.write("""
                <style>
                    /* In a <style> tag in your HTML */
                    .clickable_area {
                        border: 2px solid transparent;
                        transition: border-color 0.3s ease;
                    }
                    .clickable_area:hover {
                        border-color: red;
                    }
                    #jumpBox {
                        position: fixed;
                        bottom: 10px;
                        right: 10px;
                        padding: 10px 20px;
                        background-color: lightgrey;
                        border: 1px solid black;
                    }
                    .pageNumber {
                        z-index: 1000;
                    }
                    #partButton {
                        font-size: 20px; /* Adjust the font size */
                        padding: 10px 20px; /* Adjust the padding: top/bottom and left/right */
                        cursor: pointer;
                    }
                </style>
                <script>
                function showModal(event) {
                    event.preventDefault();  // Prevent navigation
                    var partNumber = event.target.id.split("_").slice(2).join("-");  // Get the part number from the id
                    document.getElementById('part').value = partNumber;  // Set the Part # in the modal
                    document.getElementById('modal').style.display = "block";  // Show the modal
                    document.getElementById('quantity').value = 1;
                }

                document.querySelectorAll('area').forEach(function(area) {
                    area.addEventListener('click', function(event) {
                        showModal(event);
                    });
                });

                // Close the modal when the Close button is clicked
                document.getElementById('cancelBtn').addEventListener('click', function() {
                    document.getElementById('modal').style.display = "none";
                });

                //Submit info to DB
                document.getElementById('submitBtn').addEventListener('click', function() {
                    const quantity = document.getElementById('quantity').value;
                    const invoice_num = document.getElementById('invoice').value;
                    const part_num = document.getElementById('part').value;
                    url = "http://127.0.0.1:5000/insertpart?invoice_num=" + invoice_num + "&part_num=" + part_num + "&quantity=" + quantity;
                    fetch(url)
                    .then(response => response.text())
                    .then(data => console.log(data))
                    .catch((error) => console.error('Error:', error));
                    document.getElementById('modal').style.display = "none";
                });

            """)
            f.write("""
                function jumpToPage() {
                    // Get the page number from the input field
                    var pageNumber = document.getElementById("pageNumber").value;
                    // Jump to the corresponding img element (assuming the ids are set up correctly)
            """)
            f.write(f"var realPage = parseInt(pageNumber) + {table_of_contents} - 1;")
            f.write("""
                    var pageElement = document.getElementById("page_num_" + realPage);
            """)        
            f.write("""
                    if (pageElement) {
                        pageElement.scrollIntoView();
                    }
                }
            """)