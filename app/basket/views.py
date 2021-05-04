from flask import render_template, session, request, redirect, url_for, flash, current_app
from app import db, app
from app.cinema.models import Ticket

import json


def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))


# route for adding tickets to the Basket
@app.route('/addbasket', methods=['POST'])
def AddBasket():

    try:
        ticket_id = request.form.get('ticket_id')
        quantity = int(request.form.get('quantity'))

        ticket = Ticket.query.filter_by(id=ticket_id).first()
        title = ticket.screen.movie.title
        if request.method == "POST":
            DictItems = {ticket_id: {'id': ticket.id,'title': title, 'price': float(ticket.price), 'discount': ticket.discount,
                                      'quantity': quantity,'seatNo': ticket.seatNo }}
            if 'ShoppingBasket' in session:

                if ticket_id in session['ShoppingBasket']:
                    for key, item in session['ShoppingBasket'].items():
                        if int(key) == int(ticket_id):
                            session.modified = True

                            item['quantity'] += 1

                else:
                    session['ShoppingBasket'] = MagerDicts(session['ShoppingBasket'], DictItems)
                    return redirect(request.referrer)
            else:
                session['ShoppingBasket'] = DictItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


# Basket page
@app.route('/basket')
def getBasket():
    if 'ShoppingBasket' not in session or len(session['ShoppingBasket']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key, ticket in session['ShoppingBasket'].items():
        discount = (ticket['discount'] / 100) * float(ticket['price'])
        subtotal += float(ticket['price']) * int(ticket['quantity'])
        subtotal -= discount

        grandtotal = ("%.2f" % (1.00 * float(subtotal)))
    return render_template('cinema/basket.html', grandtotal=grandtotal)

# Basket page
@app.route('/employee/basket')
def getEmployeeBasket():
    if 'ShoppingBasket' not in session or len(session['ShoppingBasket']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key, ticket in session['ShoppingBasket'].items():
        discount = (ticket['discount'] / 100) * float(ticket['price'])
        subtotal += float(ticket['price']) * int(ticket['quantity'])
        subtotal -= discount

        grandtotal = ("%.2f" % (1.00 * float(subtotal)))
    return render_template('employee/basket.html', grandtotal=grandtotal)



# route for updating the Basket
@app.route('/updatebasket/<int:code>', methods=['POST'])
def updatebasket(code):
    if 'ShoppingBasket' not in session or len(session['ShoppingBasket']) <= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')

        try:
            session.modified = True
            for key, item in session['ShoppingBasket'].items():
                if int(key) == code:
                    item['quantity'] = quantity

                    flash('Item is updated!')
                    if 'employee_id' in session:
                        return redirect(url_for('getEmployeeBasket'))
                    return redirect(url_for('getBasket'))
        except Exception as e:
            print(e)
            if 'employee_id' in session:
                return redirect(url_for('getEmployeeBasket'))
            return redirect(url_for('getBasket'))

# route for deleting the Basket
@app.route('/adult/<int:id>')
def adult(id):
    if 'ShoppingBasket' not in session or len(session['ShoppingBasket']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, ticket in session['ShoppingBasket'].items():
            if int(key) == id:
                ticket['discount'] = 0
                if 'employee_id' in session:
                    return redirect(url_for('getEmployeeBasket'))
                return redirect(url_for('getBasket'))
    except Exception as e:
        print(e)
        if 'employee_id' in session:
            return redirect(url_for('getEmployeeBasket'))
        return redirect(url_for('getBasket'))

# route for deleting the Basket
@app.route('/child/<int:id>')
def child(id):
    if 'ShoppingBasket' not in session or len(session['ShoppingBasket']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, ticket in session['ShoppingBasket'].items():
            if int(key) == id:
                ticket['discount'] = 20
                if 'employee_id' in session:
                    return redirect(url_for('getEmployeeBasket'))
                return redirect(url_for('getBasket'))
    except Exception as e:
        print(e)
        if 'employee_id' in session:
            return redirect(url_for('getEmployeeBasket'))
        return redirect(url_for('getBasket'))

# route for deleting the Basket
@app.route('/teen/<int:id>')
def teen(id):
    if 'ShoppingBasket' not in session or len(session['ShoppingBasket']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, ticket in session['ShoppingBasket'].items():
            if int(key) == id:
                ticket['discount'] = 10

                return redirect(url_for('getBasket'))
    except Exception as e:
        print(e)
        if 'employee_id' in session:
            return redirect(url_for('getEmployeeBasket'))
        return redirect(url_for('getBasket'))

# route for deleting the Basket
@app.route('/elderly/<int:id>')
def elderly(id):
    if 'ShoppingBasket' not in session or len(session['ShoppingBasket']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, ticket in session['ShoppingBasket'].items():
            if int(key) == id:
                ticket['discount'] = 15
                if 'employee_id' in session:
                    return redirect(url_for('getEmployeeBasket'))
                return redirect(url_for('getBasket'))
    except Exception as e:
        print(e)
        if 'employee_id' in session:
            return redirect(url_for('getEmployeeBasket'))
        return redirect(url_for('getBasket'))

# route for deleting the Basket
@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'ShoppingBasket' not in session or len(session['ShoppingBasket']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['ShoppingBasket'].items():
            if int(key) == id:
                session['ShoppingBasket'].pop(key, None)
                return redirect(url_for('getBasket'))
    except Exception as e:
        print(e)
        if 'employee_id' in session:
            return redirect(url_for('getEmployeeBasket'))
        return redirect(url_for('getBasket'))


# route for clearing the basket
@app.route('/clearbasket')
def clearbasket():
    try:
        session.pop('ShoppingBasket', None)
        if 'employee_id' in session:
            return redirect(url_for('employee'))
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
        if 'employee_id' in session:
            return redirect(url_for('getEmployeeBasket'))
