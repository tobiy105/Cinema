from flask import render_template, session, request, redirect, url_for, flash
from flask_login import logout_user, login_user
from app import app, db, bcrypt, Message, mail
from .forms import CustomerRegisterForm, CustomerLoginFrom
from .models import Register, CustomerOrder
from app.cinema.models import Ticket
from datetime import datetime
from config import config, STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY
import secrets
import datetime
import stripe
import pdfkit


buplishable_key = STRIPE_PUBLIC_KEY
stripe.api_key = STRIPE_SECRET_KEY

# route for payment for the customer
@app.route('/payment', methods=['POST'])
def payment():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )
    charge = stripe.Charge.create(
        customer=customer.id,
        description='Cinema',
        amount=amount,
        currency='gbp',
    )
    orders = CustomerOrder.query.filter_by(customer_id=session['customer_id'], invoice=invoice).order_by(
        CustomerOrder.id.desc()).first()
    orders.status = 'Paid'
    db.session.commit()
    flash(f'The order payment has been successful!', 'success')
    flash(f'Thank you shopping with us!', 'success')
    return redirect(url_for('orders', invoice=invoice))

# route for register with the customer account
@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,
                            password=hash_password)
        db.session.add(register)
        flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form)


# route for login with the customer account
@app.route('/customer/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginFrom()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['customer_id'] = user.id
            login_user(user)
            flash('You are login now!', 'success')
            return redirect(url_for('home'))
        flash('Incorrect email and password', 'danger')
        return redirect(url_for('customerLogin'))
    return render_template('customer/login.html', form=form)


# route for updating the customer account
@app.route('/updatecustomer/<int:id>', methods=['GET', 'POST'])
def updatecustomer(id):
    if 'customer_id' not in session:
        flash('Login first please', 'danger')
        return redirect(url_for('customerLogin'))

    updatecustomer = Register.query.get_or_404(id)
    form = CustomerRegisterForm(request.form)
    if request.method == "POST":
        updatecustomer.name = form.name.data
        updatecustomer.username = form.username.data
        updatecustomer.email = form.email.data
        hash_password = bcrypt.generate_password_hash(form.password.data)
        updatecustomer.password = hash_password
        flash(f'The  {updatecustomer.name} profile was updated', 'success')
        db.session.commit()
        return redirect(url_for('home'))
    form.name.data = updatecustomer.name
    form.username.data = updatecustomer.username
    form.email.data = updatecustomer.email
    form.password.data = updatecustomer.password
    return render_template('customer/register.html', form=form, title='Update User', updatecustomer=updatecustomer)

@app.route('/customer/logout')
def customer_logout():
    logout_user()
    del session['customer_id']
    return redirect(url_for('home'))

# deleting some of basket sessions
def updateshoppingbasket():
    for key, shopping in session['ShoppingBasket'].items():
        session.modified = True
    return updateshoppingbasket

# route for getting the order for the customer account
@app.route('/getorder')
def get_order():
    if 'customer_id' not in session:
        flash('Login first please', 'danger')
        return redirect(url_for('customerLogin'))

    if 'customer_id' in session:
        customer_id = session['customer_id']
        invoice = secrets.token_hex(5)
        updateshoppingbasket
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['ShoppingBasket'])
            db.session.add(order)
            db.session.commit()
            session.pop('ShoppingBasket')
            flash('Your order has been sent successfully', 'success')
            return redirect(url_for('orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash('Some thing went wrong while get order', 'danger')
            return redirect(url_for('getBasket'))

# route for getting the order invoice for the customer account
@app.route('/orders/<invoice>')
def orders(invoice):
    if 'customer_id' in session:
        grandTotal = 0
        subTotal = 0
        customer_id = session['customer_id']
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(
            CustomerOrder.id.desc()).first()
        for _key, ticket in orders.orders.items():
            discount = (ticket['discount'] / 100) * float(ticket['price'])
            subTotal += float(ticket['price']) * int(ticket['quantity'])
            subTotal -= discount
            # url link for qrcode
            url = "http://127.0.0.1:5000/" + str(ticket['id'])
            grandTotal = ("%.2f" % (1.00 * float(subTotal)))

        if orders.status =='Paid':
            for _key, ticket in orders.orders.items():
                ticket_id = ticket['id']
                tick = Ticket.query.get_or_404(ticket_id)
                tick.taken = True
                tick.date_created =datetime.datetime.utcnow()
                db.session.commit()

            #here is where pdf is printed
            ticketTemplate = render_template('customer/pdf.html', invoice=invoice, subTotal=subTotal,
                                             grandTotal=grandTotal,
                                             customer=customer, orders=orders, url=url)
            ticketPdf = pdfkit.from_string(ticketTemplate, False, configuration=config)
            user = Register.query.filter_by(id=customer_id).first()
            #here is where the email is sent
            email = user.email
            emailTo = [email]
            sendTicket = Message('Cinema', recipients=emailTo)
            sendTicket.body = "Hi, \n Here is your ticket(s). \n Thank you for ordering!! \n Hope you enjoy your movie exprience."
            sendTicket.attach("ticket.pdf", "application/pdf", ticketPdf)
            mail.send(sendTicket)

    else:
        flash('Login first please', 'danger')
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html', invoice=invoice, subTotal=subTotal, grandTotal=grandTotal,
                           customer=customer, orders=orders)
