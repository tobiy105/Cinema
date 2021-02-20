from flask import render_template,session, request,redirect,url_for,flash,current_app,make_response
from flask_login import login_required, current_user, logout_user, login_user
from app import app,db,photos, search,bcrypt,login_manager
from .forms import CustomerRegisterForm, CustomerLoginFrom
from .models import Register,CustomerOrder

import secrets


import stripe

buplishable_key ='pk_test_51IAqthELWQ2Csz14QllKVva5f6nfQRoiB0W2SGtwmnR8gEk4GrefCjnuHX6V0uSB6fEnSkrHMYA3gpFmUgKlY5is00QtCl8Fja'
stripe.api_key ='sk_test_51IAqthELWQ2Csz14C6JDogJdEY7AEimddb7a9DxTPw7Hl1e0XXqjfYNyYPEck3AxKNLZVCVCtwnAKVA0WBXllizZ00ZGlC0YR1'

#route for payment for the customer
@app.route('/payment',methods=['POST'])
@login_required
def payment():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
      email=request.form['stripeEmail'],
      source=request.form['stripeToken'],
    )
    charge = stripe.Charge.create(
      customer=customer.id,
      description='Sobola Food',
      amount=amount,
      currency='gbp',
    )
    orders =  CustomerOrder.query.filter_by(customer_id = current_user.id,invoice=invoice).order_by(CustomerOrder.id.desc()).first()
    orders.status = 'Paid'
    db.session.commit()
    flash(f'The order payment has been successful!', 'success')
    flash(f'Thank you shopping with us!', 'success')
    return redirect(url_for('orders',invoice=invoice))


#route for register with the customer account
@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password)
        db.session.add(register)
        flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form)

#route for login with the customer account
@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    form = CustomerLoginFrom()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are login now!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Incorrect email and password','danger')
        return redirect(url_for('customerLogin'))
            
    return render_template('customer/login.html', form=form)


# route for updating the customer account
@app.route('/updatecustomer/<int:id>', methods=['GET', 'POST'])
def updatecustomer(id):
    if 'email' not in session:
        flash('Login first please', 'danger')
        return redirect(url_for('login'))

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
    return redirect(url_for('home'))


# deleting some of basket sessions
def updateshoppingbasket():
    for key, shopping in session['ShoppingBasket'].items():
        session.modified = True
        del shopping['image']
        del shopping['category']
    return updateshoppingbasket


# route for getting the order for the customer account
@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
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
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(
            CustomerOrder.id.desc()).first()
        for _key, ticket in orders.orders.items():
            discount = (ticket['discount'] / 100) * float(ticket['price'])
            subTotal += float(ticket['price']) * int(ticket['quantity'])
            subTotal -= discount
            tax = ("%.2f" % (.06 * float(subTotal)))
            grandTotal = ("%.2f" % (1.06 * float(subTotal)))

    else:
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html', invoice=invoice, tax=tax, subTotal=subTotal, grandTotal=grandTotal,
                           customer=customer, orders=orders)


# route for getting the order invoice for the customer account
#Need to change it allow pdf to print off

@app.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        if request.method == "POST":
            customer = Register.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(
                CustomerOrder.id.desc()).first()
            for _key, ticket in orders.orders.items():
                discount = (ticket['discount'] / 100) * float(ticket['price'])
                subTotal += float(ticket['price']) * int(ticket['quantity'])
                subTotal -= discount
                tax = ("%.2f" % (.06 * float(subTotal)))
                grandTotal = float("%.2f" % (1.06 * subTotal))

    return request(url_for('orders'))







