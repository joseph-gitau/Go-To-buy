# Go-To buy flask e-commerce website

from flask import Flask, render_template, request, redirect, url_for, session, flash
# import mysql connector
from flask_mysqldb import MySQL
from flask_login import current_user
from flask import jsonify
import json


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

# /remove_item_from_cart
@app.route('/remove_item_from_cart', methods=['POST'])
def remove_item_from_cart():
    if request.method == 'POST':
        # fetch form data from json
        product_id = request.json['product_id']
        # get looged in user id
        user_id = session['user_id']
        # create cursor
        cur = db.connection.cursor()
        # execute query
        cur.execute("DELETE FROM cart WHERE product_id=%s AND user_id=%s", (product_id, user_id))
        db.connection.commit()
        # close connection
        cur.close()
        flash('Product removed from cart', 'success')
        #  return json success response
        return jsonify({'success': True})
    
    
# /checkout
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # Calculate total
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
    return render_template('checkout.html', cart=cart, total=total)

# /checkout-now
@app.route('/checkout-now', methods=['POST'])
def checkout_now():
    if request.method == 'POST':
        # fetch form data from request
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        card_number = request.form['card_number']
        card_expiry = request.form['expiry_date']
        card_cvv = request.form['cvv']
        total = request.form['total']

        # get looged in user id
        user_id = session['user_id']
        # verify the data
        if name == '' or email == '' or address == '' or card_number == '' or card_expiry == '' or card_cvv == '' or total == '':
            # redirect back to checkout page with flash message
            flash('Please fill all the fields', 'danger')
            return redirect(url_for('checkout'))
        # verify card data
        if len(card_number) != 16 or len(card_expiry) != 5 or len(card_cvv) != 3:
            # redirect back to checkout page with flash message
            flash('Invalid card details', 'danger')
            return redirect(url_for('checkout'))
        
        # add order to orders table
        cur = db.connection.cursor()
        cur.execute("INSERT INTO orders(user_id, total, name, email, address, card_number, card_expiry, card_cvv) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (user_id, total, name, email, address, card_number, card_expiry, card_cvv))
        db.connection.commit()
        cur.close()
        # get order id
        cur = db.connection.cursor()
        cur.execute("SELECT id FROM orders WHERE user_id=%s ORDER BY id DESC LIMIT 1", [user_id])
        order_id = cur.fetchone()
        cur.close()
        # add order items to order_items table
        # Get cart items from cart table and add them to order_items table
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM cart WHERE user_id=%s", [user_id])
        cart = cur.fetchall()
        cur.close()
        # add cart items to order_items table
        for item in cart:
            cur = db.connection.cursor()
            cur.execute("INSERT INTO order_items(order_id, product_id, quantity) VALUES(%s, %s, %s)", (order_id, item[2], item[3]))
            db.connection.commit()
            cur.close()
        

        # delete cart items
        cur = db.connection.cursor()
        cur.execute("DELETE FROM cart WHERE user_id=%s", [user_id])
        db.connection.commit()
        cur.close()
        # redirect to orders success page
        flash('Order placed successfully', 'success')
        return redirect(url_for('orders'))
    
    
# /orders
@app.route('/orders')
def orders():
    # get looged in user id
    user_id = session['user_id']
    # create cursor
    cur = db.connection.cursor()
    # Get order_id, created_at from orders table, product_id and quantity from order_items table, product name, price, image from products table then join them
    cur.execute("SELECT orders.id, orders.created_at, order_items.product_id, order_items.quantity, products.p_name, products.price, products.p_image FROM orders JOIN order_items ON orders.id=order_items.order_id JOIN products ON order_items.product_id=products.id WHERE orders.user_id=%s", [user_id])
    orders = cur.fetchall()
    # close connection
    cur.close()
    # make orders a dictionary
    orders = dict(enumerate(orders))
    return render_template('orders.html', orders=orders)
    

if __name__ == '__main__':
    app.run(debug=True)
