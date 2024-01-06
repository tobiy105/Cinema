from flask import render_template, session, request, redirect, url_for, flash
from app import app,db, bcrypt, Message, mail
from .forms import Employee, EmployeeLoginFrom, EmployeeRegisterForm, PayWithCashForm
from .models import Employee, EmployeeOrder
from app.cinema.models import Ticket, Movies, Screening
from app.till.views import *
from config import config
from datetime import date
from datetime import datetime
import datetime
import sys
import secrets
import pdfkit

@app.route('/till/<invoice>?<amount>', methods=['GET', 'POST'])
def showTill(invoice, amount):
    form = PayWithCashForm(request.form)
    if request.method == "POST":
        payment = Cash(form.n50.data, form.n20.data, form.n10.data, form.n5.data, form.c200.data, form.c100.data, form.
                       c50.data, form.c20.data, form.c10.data, form.c5.data, form.c2.data, form.c1.data)
        till = Till(loadTill())
        flag, change = till.cashPayment(amount, payment)
        if flag == 0:  #success
            saveToTill(till.cash)
            return redirect(url_for('employeePayment', invoice=invoice, cash=change.to_string_q()), code=307) #should go to payment confimed
        elif flag == 1:  #error not enough money
            return render_template('till/till.html', form=form, flag=1, amount=amount)
        elif flag == 2:  ##error not enough change
            return render_template('till/till.html', form=form, flag=2, amount=amount)
    return render_template('till/till.html', form=form, flag=0, amount=amount)


# route for payment for the customer
@app.route('/employee/payment/<invoice>/<cash>', methods=['POST'])
def employeePayment(invoice, cash):
    emp_id = session['employee_id']
    orders = EmployeeOrder.query.filter_by(employee_id=emp_id, invoice=invoice).order_by(
        EmployeeOrder.id.desc()).first()
    orders.status = 'Paid'
    db.session.commit()
    flash(f'The order payment has been successful!', 'success')
    flash(f'Thank you shopping with us!', 'success')
    return redirect(url_for('employee_orders', invoice=invoice, cash=cash))


#Employee page
@app.route('/employee')
def employee():
    if 'employee_id' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('employeeLogin'))

    movies = Movies.query.all()
    return render_template('employee/index.html', movies=movies)


# route for register with the employee account
@app.route('/employee/register', methods=['GET', 'POST'])
def employee_register():
    form = EmployeeRegisterForm(request.form)
    if request.method == 'POST' and form.validate():

        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Employee(name=form.name.data, username=form.username.data, email=form.email.data,
                            password=hash_password)
        db.session.add(register)
        flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('employeeLogin'))
    return render_template('employee/register.html', form=form)


# route for login with the employee account
@app.route('/employee/login', methods=['GET', 'POST'])
def employeeLogin():
    form = EmployeeLoginFrom(request.form)
    if request.method == "POST" and form.validate():
        user = Employee.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['employee_id'] = user.id
            flash('You are login now!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('employee'))
        flash('Incorrect email and password', 'danger')
        return redirect(url_for('employeeLogin'))

    return render_template('employee/login.html', form=form)


# route for updating the employee account
@app.route('/updateemployee/<int:id>', methods=['GET', 'POST'])
def updateemployee(id):
    if 'employee_id' not in session:
        flash('Login first please', 'danger')
        return redirect(url_for('employeeLogin'))

    updateemployee = Employee.query.get_or_404(id)
    form = EmployeeRegisterForm(request.form)
    if request.method == "POST":
        updateemployee.name = form.name.data
        updateemployee.username = form.username.data
        updateemployee.email = form.email.data
        hash_password = bcrypt.generate_password_hash(form.password.data)
        updateemployee.password = hash_password

        flash(f'The  {updateemployee.name} profile was updated', 'success')
        db.session.commit()
        return redirect(url_for('employee'))
    form.name.data = updateemployee.name
    form.username.data = updateemployee.username
    form.email.data = updateemployee.email
    form.password.data = updateemployee.password

    return render_template('employee/register.html', form=form, title='Update User', updateemployee=updateemployee)


#route for displaying a tickets found from word search
@app.route('/employee/ticket/<int:id>', methods=['GET', 'POST'])
def employee_single_page(id):
    movie = Movies.query.get_or_404(id)
    screens = Screening.query.filter_by(movie_id=id)
    session['movie'] = id
    today = date.today()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")
    weekNo = datetime.date(int(year), int(month), int(day)).isocalendar()[1]

    mon = datetime.datetime.strptime(f'{year}-W{weekNo}-1', "%Y-W%W-%w").date()
    tue = datetime.datetime.strptime(f'{year}-W{weekNo}-2', "%Y-W%W-%w").date()
    wed = datetime.datetime.strptime(f'{year}-W{weekNo}-3', "%Y-W%W-%w").date()
    thur = datetime.datetime.strptime(f'{year}-W{weekNo}-4', "%Y-W%W-%w").date()
    fri = datetime.datetime.strptime(f'{year}-W{weekNo}-5', "%Y-W%W-%w").date()
    sat = datetime.datetime.strptime(f'{year}-W{weekNo}-6', "%Y-W%W-%w").date()
    sun = datetime.datetime.strptime(f'{year}-W{weekNo}-0', "%Y-W%W-%w").date()


    num = 0
    if request.method == "POST":
        num = int(request.form.get('number'))
        mon = datetime.datetime.strptime(f'{year}-W{weekNo + num}-1', "%Y-W%W-%w").date()
        tue = datetime.datetime.strptime(f'{year}-W{weekNo + num}-2', "%Y-W%W-%w").date()
        wed = datetime.datetime.strptime(f'{year}-W{weekNo + num}-3', "%Y-W%W-%w").date()
        thur = datetime.datetime.strptime(f'{year}-W{weekNo + num}-4', "%Y-W%W-%w").date()
        fri = datetime.datetime.strptime(f'{year}-W{weekNo + num}-5', "%Y-W%W-%w").date()
        sat = datetime.datetime.strptime(f'{year}-W{weekNo + num}-6', "%Y-W%W-%w").date()
        sun = datetime.datetime.strptime(f'{year}-W{weekNo + num}-0', "%Y-W%W-%w").date()

    time_9 = "09:00:00"
    time9 = datetime.datetime.strptime(time_9, "%H:%M:%S")
    time_12 = "12:00:00"
    time12 = datetime.datetime.strptime(time_12, "%H:%M:%S")
    time_15 = "15:00:00"
    time15 = datetime.datetime.strptime(time_15, "%H:%M:%S")
    time_18 = "18:00:00"
    time18 = datetime.datetime.strptime(time_18, "%H:%M:%S")

    return render_template('employee/single_page.html',movie=movie, screens=screens, time9=time9, time12=time12, time15=time15, time18=time18,
                           mon=mon, tue=tue, wed=wed, thur=thur, fri=fri, sat=sat, sun=sun, num=num, today=today)


#route for displaying a tickets found from word search
@app.route('/employee/seats/<int:id>', methods=['GET','POST'])
def employee_seats_page(id):
    screen = Screening.query.get_or_404(id)
    tickets = Ticket.query.filter_by(screen_id=id)
    session['screen'] = id
    arr = []

    for i in range(screen.seats):
        arr.append(i)
        for ticket in tickets:
            if i == ticket.seatNo and ticket.taken==True:
                arr.remove(i)

    return render_template('employee/seats.html',screen=screen, tickets=tickets, arr=arr)

# deleting some of basket sessions
def employeeupdateshoppingbasket():
    for key, shopping in session['ShoppingBasket'].items():
        session.modified = True
    return employeeupdateshoppingbasket

# route for getting the order for the customer account
@app.route('/employee/getorder')
def employee_get_order():
    if 'employee_id' not in session:
        flash('Login first please', 'danger')
        return redirect(url_for('employeeLogin'))

    if 'employee_id' in session:
        employee_id = session['employee_id']
        invoice = secrets.token_hex(5)
        employeeupdateshoppingbasket
        try:
            order = EmployeeOrder(invoice=invoice, employee_id=employee_id, orders=session['ShoppingBasket'])
            print('invoice ' + str(invoice) + ' empid ' + str(employee_id), file=sys.stderr)
            db.session.add(order)
            db.session.commit()
            session.pop('ShoppingBasket')
            flash('Your order has been sent successfully', 'success')
            cash = Cash(0,0,0,0,0,0,0,0,0,0,0,0,)
            return redirect(url_for('employee_orders', invoice=invoice, cash = cash.to_string()))
        except Exception as e:
            print(e)
            flash('Some thing went wrong while get order', 'danger')
            return redirect(url_for('getEmployeeBasket'))

@app.route('/employee/logout')
def employee_logout():
    del session['employee_id']
    return redirect(url_for('employee'))

# route for getting the order invoice for the customer account
@app.route('/employee/orders/<invoice>/<cash>')
def employee_orders(invoice, cash):
    if 'employee_id' in session:
        grandTotal = 0
        subTotal = 0
        employee_id = session['employee_id']
        customer = Employee.query.filter_by(id=employee_id).first()
        orders = EmployeeOrder.query.filter_by(employee_id=employee_id, invoice=invoice).order_by(
            EmployeeOrder.id.desc()).first()
        for _key, ticket in orders.orders.items():
            discount = (ticket['discount'] / 100) * float(ticket['price'])
            subTotal += float(ticket['price']) * int(ticket['quantity'])
            subTotal -= discount
            url = "http://127.0.0.1:5000/" + str(ticket['id'])
            grandTotal = ("%.2f" % (1.00 * float(subTotal)))

        if orders.status =='Paid':
            p = Cash(0,0,0,0,0,0,0,0,0,0,0,0,)
            cash = p.fromString(cash, '?')
            for _key, ticket in orders.orders.items():
                ticket_id = ticket['id']
                tick = Ticket.query.get_or_404(ticket_id)
                tick.taken = True
                tick.date_created = datetime.datetime.utcnow()
                db.session.commit()

            #here is where pdf is printed
            ticketTemplate = render_template('customer/pdf.html', invoice=invoice, subTotal=subTotal,
                                             grandTotal=grandTotal,
                                             customer=customer, orders=orders, url=url)
            ticketPdf = pdfkit.from_string(ticketTemplate, False, configuration=config)
            user = Employee.query.filter_by(id=employee_id).first()
            email = user.email
            emailTo = [email]

            sendTicket = Message('Cinema Ticket(s)', recipients=emailTo)
            sendTicket.body = "Hi, \n Here is your ticket. \n Thank you for ordering!"
            sendTicket.attach("ticket.pdf", "application/pdf", ticketPdf)
            mail.send(sendTicket)
    else:
        flash('Login first please', 'danger')
        return redirect(url_for('employeeLogin'))
    return render_template('employee/order.html', invoice=invoice, subTotal=subTotal, grandTotal=grandTotal,
                           customer=customer, orders=orders, cash=cash)
