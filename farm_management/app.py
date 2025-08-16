from flask import Flask, render_template, request, redirect
import mysql.connector

# Initialize Flask app
app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="prathika",  # Replace with your MySQL password
    database="farm_management"
)

# Home Page Route
@app.route('/')
def home():
    return render_template('index.html')

# Farmer Registration Route
@app.route('/farmer_register', methods=['GET', 'POST'])
def farmer_register():
    if request.method == 'POST':
        name = request.form['name']
        aadhaar = request.form['aadhaar']
        phone = request.form['phone']
        farming_type = request.form['farming_type']
        address = request.form['address']

        cursor = db.cursor()
        cursor.execute("INSERT INTO farmer (name, aadhaar, phone, farming_type, address) VALUES (%s, %s, %s, %s, %s)",
                       (name, aadhaar, phone, farming_type, address))
        db.commit()
        cursor.close()

        return redirect('/farmer_details')  # Redirect to farmer details page after registration
    return render_template('farmer_register.html')

# Farmer Details Route (Display all registered farmers)
@app.route('/farmer_details')
def farmer_details():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM farmer")
    farmers = cursor.fetchall()
    cursor.close()
    return render_template('farmer_details.html', farmers=farmers)


# Update Farmer Route
@app.route('/update_farmer', methods=['POST'])
def update_farmer():
    id = request.form['id']
    name = request.form['name']
    aadhaar = request.form['aadhaar']
    phone = request.form['phone']
    farming_type = request.form['farming_type']
    address = request.form['address']

    print(f"Received: {id}, {name}, {aadhaar}, {phone}, {farming_type}, {address}")  # Debugging


    cursor = db.cursor()
    cursor.execute(
        """
        UPDATE farmer 
        SET name = %s, aadhaar = %s, phone = %s, farming_type = %s, address = %s 
        WHERE id = %s
        """,
        (name, aadhaar, phone, farming_type, address, id)
    )
    db.commit()
    cursor.close()
    return '', 204  # No content (success response)




# Delete Farmer Route
@app.route('/delete_farmer', methods=['POST'])
def delete_farmer():
    id = request.form['id']
    cursor = db.cursor()
    cursor.execute("DELETE FROM farmer WHERE id = %s", (id,))
    db.commit()
    cursor.close()
    return '', 204  # No content




# Sell Agro Products Route
@app.route('/sell_agro_products', methods=['GET', 'POST'])
def sell_agro_products():
    if request.method == 'POST':
        product_name = request.form['product_name']
        description = request.form['description']
        price = request.form['price']
        email = request.form['email']

        cursor = db.cursor()
        cursor.execute("INSERT INTO produc (product_name, description, price, email) VALUES (%s, %s, %s, %s)",
                       (product_name, description, price, email))
        db.commit()
        cursor.close()

        return redirect('/agro_products')  # Redirect to agro products page after posting
    return render_template('sell_agro_products.html')

# Display Agro Products Route
@app.route('/agro_products')
def agro_products():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produc")
    products = cursor.fetchall()
    cursor.close()
    return render_template('agro_products.html', products=products)




# Route to display farmer registration and deletion records
@app.route('/farmer_records')
def farmer_records():
    cursor = db.cursor()
    cursor.execute("SELECT name, aadhaar, phone, action, timestamp FROM farmer_records ORDER BY timestamp DESC")
    records = cursor.fetchall()
    cursor.close()
    return render_template('records.html', records=records)


# Run the app
if __name__ == '__main__':
    app.run(debug=True) 