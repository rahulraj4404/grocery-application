from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for sessions

# Mock data for products and users
products = [
    {"id": 1, "name": "Apple", "price": 1.0},
    {"id": 2, "name": "Banana", "price": 0.5},
    {"id": 3, "name": "Carrot", "price": 0.75},
]

users = {
    "user@example.com": {"password": "password", "cart": []}
}

# Routes
@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            session['user'] = email
            return redirect(url_for('index'))
        return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email not in users:
            users[email] = {"password": password, "cart": []}
            session['user'] = email
            return redirect(url_for('index'))
        return 'Email already registered', 400
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    email = session['user']
    users[email]['cart'].append(product_id)
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    if 'user' not in session:
        return redirect(url_for('login'))
    email = session['user']
    user_cart = [products[p_id - 1] for p_id in users[email]['cart']]
    return render_template('cart.html', cart=user_cart)

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'user' not in session:
        return redirect(url_for('login'))
    email = session['user']
    users[email]['cart'] = []  # Clear the cart after checkout
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)
