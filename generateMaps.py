base_path = '/Users/alv/Documents/Scripts/PDFtoHTML'
pdf_dir = f'{base_path}/pdfs'
from pdf2image import convert_from_path
import pytesseract
import re
import os

for filename in os.listdir(pdf_dir):

    if filename.endswith('.pdf'):
        # First, convert PDF to images
        file_path = os.path.join(pdf_dir, filename)
        images = convert_from_path(file_path)

        # Define a regex pattern for your codes
        pattern = re.compile(r'\d{3}-\d{3}')

        # Define the offset (in pixels) for the clickable area
        offset = 10

        with open(f'{base_path}/html/{filename.split(".")[0]}.html', 'w') as f:
            if not os.path.exists(f'{base_path}/html/images_{filename.split(".")[0]}'):
                os.mkdir(f'{base_path}/html/images_{filename.split(".")[0]}')
            f.write('<html>\n<body>\n')
            # Then process each image
            for i, image in enumerate(images):
                # Save the image to a file
                
                page_path = f'{base_path}/html/images_{filename.split(".")[0]}/page{i}.png'
                image.save(page_path)

                f.write(f'<img src="{page_path}" usemap="#map{i}" alt="Page {i}">')
                f.write(f'<map name="map{i}">')

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
                <style>
                    /* In a <style> tag in your HTML */
                    .clickable_area {
                        border: 2px solid transparent;
                        transition: border-color 0.3s ease;
                    }
                    .clickable_area:hover {
                        border-color: red;
                    }
                </style>
                <script>
                document.querySelectorAll('area').forEach(function(area) {
                    area.addEventListener('click', function(event) {
                        event.preventDefault();  // Prevent navigation
                        var partNumber = event.target.id.split("_").slice(2).join("-");  // Get the part number from the id
                        document.getElementById('part').value = partNumber;  // Set the Part # in the modal
                        document.getElementById('modal').style.display = "block";  // Show the modal
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

                </script>
            """)