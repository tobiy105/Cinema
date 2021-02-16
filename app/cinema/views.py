from flask import render_template,session, request,redirect,url_for,flash,current_app
from app import app,db,photos, search
from .models import Category,Addticket
from .forms import Addtickets
import secrets
import os

#route for home
@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    tickets = Addticket.query.filter(Addticket.stock > 0).order_by(Addticket.id.desc()).paginate()

    return render_template('cinema/index.html', tickets=tickets)

#query search for categories
def categories():
    categories = Category.query.join(Addticket,(Category.id == Addticket.category_id)).all()
    return categories

#route for result of finding a ticket by using search word
@app.route('/result')
def result():
    searchword = request.args.get('q')
    tickets = Addticket.query.msearch(searchword, fields=['name','desc'] , limit=10)
    return render_template('cinema/result.html',tickets=tickets,categories=categories())

#route for displaying a tickets found from word search
@app.route('/ticket/<int:id>')
def single_page(id):
    ticket = Addticket.query.get_or_404(id)
    return render_template('cinema/single_page.html',ticket=ticket,categories=categories())

#route for displaying a tickets with a category
@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page',1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_ticket = Addticket.query.filter_by(category=get_cat).paginate(page=page, per_page=8)
    return render_template('cinema/index.html',get_cat_ticket=get_cat_ticket,categories=categories(),get_cat=get_cat)

#route for adding categories
@app.route('/addcat',methods=['GET','POST'])
def addcat():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    if request.method =="POST":
        getcat = request.form.get('category')
        category = Category(name=getcat)
        db.session.add(category)
        flash(f'The category {getcat} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('cinema/addcategory.html', title='Add category')

#route for updating category
@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))

    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method =="POST":
        updatecat.name = category
        flash(f'The category {updatecat.name} was changed to {category}','success')
        db.session.commit()
        return redirect(url_for('categories'))
    category = updatecat.name
    return render_template('cinema/addcategory.html', title='Update cat',updatecat=updatecat)

#route for deleting category
@app.route('/deletecat/<int:id>', methods=['GET','POST'])
def deletecat(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        flash(f"The category {category.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"The category {category.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))

#route for adding tickets
@app.route('/addticket', methods=['GET','POST'])
def addticket():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    form = Addtickets(request.form)
 
    categories = Category.query.all()
    if request.method=="POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data

        desc = form.description.data
       
        category = request.form.get('category')
       
        newticket = Addticket(name=name,price=price,discount=discount,stock=stock,desc=desc,category_id=category)
        db.session.add(newticket)
        flash(f'The ticket {name} was added in database','success')
        print(newticket.name)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('cinema/addticket.html', form=form, title='Add a Ticket', categories=categories)

#route for updating ticket
@app.route('/updateticket/<int:id>', methods=['GET','POST'])
def updateticket(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    form = Addtickets(request.form)
    ticket = Addticket.query.get_or_404(id)
    
    categories = Category.query.all()
    
    category = request.form.get('category')
    if request.method =="POST":
        ticket.name = form.name.data
        ticket.price = form.price.data
        ticket.discount = form.discount.data
        ticket.stock = form.stock.data

        ticket.desc = form.description.data
        ticket.category_id = category

        flash('The ticket was updated','success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.name.data = ticket.name
    form.price.data = ticket.price
    form.discount.data = ticket.discount
    form.stock.data = ticket.stock
    form.category.data = ticket.category
    form.description.data = ticket.desc
   
    category = ticket.category.name
    return render_template('cinema/addticket.html', form=form, title='Update Ticket',getticket=ticket, categories=categories)

#route for deleting ticket
@app.route('/deleteticket/<int:id>', methods=['POST'])
def deleteticket(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    ticket = Addticket.query.get_or_404(id)
    if request.method =="POST":
        
        db.session.delete(ticket)
        db.session.commit()
        flash(f'The ticket {ticket.name} was delete from your record','success')
        return redirect(url_for('admin'))
    flash(f'Can not delete the ticket','success')
    return redirect(url_for('admin'))