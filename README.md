# MossMotorsCatalogueToHTML

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
