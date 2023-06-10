from flask import Flask, request
import mysql.connector
app = Flask(__name__)

@app.route('/insertpart')
def home():
    invoice_num = request.args.get('invoice_num')
    part_num = request.args.get('part_num')
    quantity = request.args.get('quantity')
    conn = mysql.connector.connect(user='root', host='localhost', database='autotech', port=3307)
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO invoices (Inv_no, Qty, Item) VALUES({invoice_num}, '{part_num}', '{quantity}');")
    conn.commit()
    cursor.close()
    return "done"


if __name__ == '__main__':
    app.run(debug=True)