from flask import render_template, session, request, redirect, url_for, flash, current_app
from app import db, app
from app.cinema.models import Addticket
from app.cinema.views import  categories
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
        category = request.form.get('category')
        ticket = Addticket.query.filter_by(id=ticket_id).first()

        if request.method == "POST":
            DictItems = {ticket_id: {'name': ticket.name, 'price': float(ticket.price), 'discount': ticket.discount,
                                      'quantity': quantity, 'category': ticket.category}}
            if 'ShoppingBasket' in session:
                print(session['ShoppingBasket'])
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
def getCart():
    if 'ShoppingBasket' not in session or len(session['ShoppingBasket']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key, ticket in session['ShoppingBasket'].items():
        discount = (ticket['discount'] / 100) * float(ticket['price'])
        subtotal += float(ticket['price']) * int(ticket['quantity'])
        subtotal -= discount
        tax = ("%.2f" % (.06 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    return render_template('cinema/basket.html', tax=tax, grandtotal=grandtotal, brands=brands(),
                           categories=categories())


# route for updating the Basket
@app.route('/updatebasket/<int:code>', methods=['POST'])
def updatebasket(code):
    if 'ShoppingBasket' not in session or len(session['ShoppingBasket']) <= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        category = request.form.get('category')
        try:
            session.modified = True
            for key, item in session['ShoppingBasket'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['category'] = category
                    flash('Item is updated!')
                    return redirect(url_for('getBasket'))
        except Exception as e:
            print(e)
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
        return redirect(url_for('getBasket'))


# route for clearing the basket
@app.route('/clearbasket')
def clearbasket():
    try:
        session.pop('ShoppingBasket', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
