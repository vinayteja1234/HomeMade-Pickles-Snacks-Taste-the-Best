from flask import Flask, render_template, request, redirect, url_for, session
import boto3
import traceback

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# DynamoDB configuration for AWS EC2
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1'
)

users_table = dynamodb.Table('Users')


@app.route('/')
def index():
    return render_template('index.html')


@app.context_processor
def inject_cart_count():
    cart = session.get('cart', {})
    count = sum(item['quantity'] for item in cart.values())
    return dict(cart_count=count)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')


@app.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart_items.values())
    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = request.form.get('item_id')
    name = request.form.get('name')
    price = float(request.form.get('price'))

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    if item_id in cart:
        cart[item_id]['quantity'] += 1
    else:
        cart[item_id] = {
            'name': name,
            'price': price,
            'quantity': 1
        }

    session.modified = True
    return redirect(request.referrer or url_for('home'))


@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('cart'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        try:
            response = users_table.get_item(
                Key={'username': username}
            )

            if 'Item' not in response:
                return render_template('login.html', error="Invalid Username or Password")

            user = response['Item']

            if user['password'] == password:
                session['user'] = username
                return redirect(url_for('home'))
            else:
                return render_template('login.html', error="Invalid Username or Password")

        except Exception as e:
            error_details = traceback.format_exc()
            print(error_details)
            return render_template('login.html', error="Database error")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            response = users_table.get_item(
                Key={'username': username}
            )

            if 'Item' in response:
                return render_template('signup.html', error="Username already exists")

            users_table.put_item(
                Item={
                    'username': username,
                    'email': email,
                    'password': password
                }
            )

            return redirect(url_for('login'))

        except Exception as e:
            error_details = traceback.format_exc()
            print(error_details)
            return render_template('signup.html', error="Database error")

    return render_template('signup.html')


@app.route('/veg_pickles')
def veg_pickles():
    return render_template('veg_pickles.html')


@app.route('/non_veg_pickles')
def non_veg_pickles():
    return render_template('non_veg_pickles.html')


@app.route('/snacks')
def snacks():
    return render_template('snacks.html')


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
