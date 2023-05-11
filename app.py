# Go-To buy flask e-commerce website

from flask import Flask, render_template, request, redirect, url_for, session, flash
# import mysql connector
from flask_mysqldb import MySQL
from flask_login import current_user
from flask import jsonify


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'go_to_buy'
app.config['SECRET_KEY'] = 'thisissecret'

db = MySQL(app)

# Routes
@app.route('/')
def index():
    # fetch all products
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('index.html', products=products)

# /view_product/<int:id>
@app.route('/view_product/<int:id>')
def view_product(id):
    # fetch product
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id=%s", [id])
    product = cur.fetchone()
    cur.close()
    return render_template('view_product.html', product=product)

# register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # fetch form data
        userDetails = request.form
        name = userDetails['username']
        email = userDetails['email']
        password = userDetails['password']
        # create cursor
        cur = db.connection.cursor()
        # execute query
        cur.execute("INSERT INTO users(username, email, password) VALUES(%s, %s, %s)", (name, email, password))
        # commit to DB
        db.connection.commit()
        # close connection
        cur.close()
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # fetch form data
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']
        # create cursor
        cur = db.connection.cursor()
        # execute query
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        # close connection
        cur.close()
        if user:
            # create session
            session['logged_in'] = True
            session['email'] = user[2]
            session['username'] = user[1]
            session['user_id'] = user[0]
            flash('You are now logged in', 'success')
            return redirect(url_for('index'))
        else:
            error = 'Invalid login'
            return render_template('login.html', error=error)
    return render_template('login.html')

# logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# /add_to_cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if request.method == 'POST':
        # fetch form data from json
        product_id = request.json['product_id']
        quantity = request.json['quantity']
        # get looged in user id
        user_id = session['user_id']
        # Check cart table for existing product or not
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM cart WHERE product_id=%s AND user_id=%s", (product_id, user_id))
        product = cur.fetchone()
        if product:
            # update cart table
            cur.execute("UPDATE cart SET quantity=%s WHERE product_id=%s AND user_id=%s", (quantity, product_id, user_id))
            db.connection.commit()
            cur.close()
            flash('Cart updated', 'success')
            #  return json success response
            return jsonify({'success': True})

        else:
            # insert into cart table
            cur.execute("INSERT INTO cart(product_id, user_id, quantity) VALUES(%s, %s, %s)", (product_id, user_id, quantity))
            db.connection.commit()
            cur.close()
            flash('Product added to cart', 'success')
            #  return json success response
            return jsonify({'success': True})

        
# /get_cart_count
@app.route('/get_cart_count')
def get_cart_count():
    # get looged in user id
    user_id = session['user_id']
    # create cursor
    cur = db.connection.cursor()
    # execute query
    cur.execute("SELECT * FROM cart WHERE user_id=%s", [user_id])
    cart = cur.fetchall()
    # close connection
    cur.close()
    # return json response
    return jsonify({'cart_count': len(cart)})

# cart
@app.route('/cart')
def cart():
    # get looged in user id
    user_id = session['user_id']
    # create cursor
    cur = db.connection.cursor()
    # execute query
    # get product_id from cart and get the product details from products table
    cur.execute("SELECT cart.quantity, products.* FROM cart JOIN products ON cart.product_id=products.id WHERE cart.user_id=%s", [user_id])
    cart = cur.fetchall()
    # close connection
    cur.close()
    # make cart a dictionary
    cart = dict(enumerate(cart))
    # calculate total
    total = sum(item[5] * item[0] for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)
    

if __name__ == '__main__':
    app.run(debug=True)
