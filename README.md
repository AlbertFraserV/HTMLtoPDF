# MossMotorsInvoiceGenerator

This repo is a small project which is intended to take a PDF catalogue from Moss Motors and convert it into HTML so that the part numbers can be selected and added to a MySQL database to generate invoices. 

## Setup Instructions

Follow the steps below to set up and run the AutoTech catalog web application:

1. **Set up a Python virtual environment:**
The requirements.txt file lists all Python libraries that your project depends on. You should install them in a virtual environment.
To create a virtual environment, open a terminal in your project's directory and run:

```
python3 -m venv env
```

To activate the environment and install the required packages, run:

```
source env/bin/activate
pip install -r requirements.txt
```

2. **Organize your PDFs:**
The application needs the PDF files you want to convert. Place all your PDF files in a new directory named pdfs in the root of your project.

```
mkdir pdfs
```

3. **Create an HTML directory:**
The application will convert your PDFs into HTML files and save them in this directory. In the root of your project, create a new directory named html.

```
mkdir html
```

4. **Configure database connection details:**
Open app.py in a text editor. Look for the following line and replace 'user', 'host', 'password', 'database', and '3306' with your actual database username, password, host, database name, and port, respectively:

```
conn = mysql.connector.connect(user='root', host='host', password='', database='database', port=3306)
```

Also, modify the **INSERT INTO** statement according to your table structure. The example given is:
```
cursor.execute(f"INSERT INTO invoices (invoice_number, quantity, item_number) VALUES({invoice_num}, '{part_num}', '{quantity}');")
```

5. **Run generateHTML.py:**
This script will generate HTML files from your PDFs. To run the script, use:

```
python generateHTML.py
```

Now, your application is set up and ready to use. If you have any issues or need further clarification, please refer to the official Python, MySQL, and Flask documentation, or ask for help on forums like Stack Overflow. Enjoy your AutoTech catalog web application!

## How to use

### Interacting with Part Numbers

* **Selecting a Part Number:** Click on any part number in the catalog. This action opens a dialog box.
* **Auto-filled Part Number:** When the dialog box opens, the part number you clicked on is automatically filled in the Part Number field. This auto-fill feature saves you time by eliminating the need to manually enter the part number.

### Managing Invoices

* **Entering an Invoice Number:** The first time you use the application after a page load, you'll need to manually enter an invoice number. After you've entered it once, the application will remember the invoice number for the rest of the session. This means you won't have to re-enter it unless you want to change it.

### Adjusting Quantity

* **Changing Quantity:** The quantity field in the dialog box defaults to 1. If you need more than one of a particular part, simply change the quantity in this field.

### Manual Entry Box

* **Unclear Part Numbers:** If a part number hasn't been parsed correctly, you can manually bring up the dialog box. To do this, click the designated box.

### Jump Page Button

* **Navigating the Catalog:** If you want to quickly move to a different page in the catalog, use the Jump Page button. This feature allows you to navigate the catalog according to the Table of Contents.


Now that you understand the functionalities of the AutoTech Catalog web application, you're all set to start using it. Enjoy the ease and convenience that this application brings to managing your parts catalog!

## Project Todo

Here's a list of potential enhancements. While these items are not immediately required for the current project scope, they represent potential future improvements that could extend the functionality and usability of the application:

* **Setup Script:** Develop a setup script to streamline the initial configuration of the application for users.
* **Generalize Application:** Modify the application to be more broadly applicable beyond the Moss Motors catalog. Consider incorporating a setting to accommodate different part/item number formats.
* **UI Enhancements:** Improve the aesthetic and usability of the buttons. Consider introducing more UI customization options within the HTML file to further improve user experience.
* **Part/Item Number to Diagram Linking:** Explore the feasibility of linking part numbers to diagrams. The current state of the Moss Motors PDFs might present some challenges with this feature, given the blurry text of the diagrams.
