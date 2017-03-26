import os
from flask import Flask, render_template, request
import stripe

stripe_keys = {
  'secret_key': os.environ['SECRET_KEY'],
  'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', key=stripe_keys['publishable_key'])

@app.route('/chargebox', methods=['POST'])
def chargebox():
    # Amount in cents
    amount = 1200

    customer = stripe.Customer.create(
        email=request.form['email'],
        source=request.form['stripeToken'],
        metadata={"name": request.form['cardholder-name']}
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        metadata={"delivery_location": request.form['dormroom'], "delivery_date": request.form['delivery']},
        description='Munchies - 1 Box'
    )

    # console.log('here')

    return render_template('charge.html', amount=amount)

@app.route('/chargeboxes', methods=['POST'])
def chargeboxes():
    # Amount in cents
    amount = 2000

    customer = stripe.Customer.create(
        email=request.form['email'],
        source=request.form['stripeToken'],
        metadata={"name": request.form['cardholder-name']}
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        metadata={"delivery_location": request.form['dormroom'], "delivery_date": request.form['delivery']},
        description='Munchies - 2 Boxes'
    )

    return render_template('charge.html', amount=amount)

@app.url_defaults
def hashed_url_for_static_file(endpoint, values):
    if 'static' == endpoint or endpoint.endswith('.static'):
        filename = values.get('filename')
        if filename:
            if '.' in endpoint:  # has higher priority
                blueprint = endpoint.rsplit('.', 1)[0]
            else:
                blueprint = request.blueprint  # can be None too

            if blueprint:
                static_folder = app.blueprints[blueprint].static_folder
            else:
                static_folder = app.static_folder

            param_name = 'h'
            while param_name in values:
                param_name = '_' + param_name
            values[param_name] = static_file_hash(os.path.join(static_folder, filename))
            
def static_file_hash(filename):
  return int(os.stat(filename).st_mtime)

if __name__ == '__main__':
    app.run(debug=True)
