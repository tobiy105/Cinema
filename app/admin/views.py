from flask import render_template, session, request, redirect, url_for, flash, make_response
from app import app, db, bcrypt
from app.cinema.models import Ticket, Movies, Screening
from app.customers.models import CustomerOrder
from .forms import RegistrationForm, LoginForm, CompareMovieForm, MovieSalesData
from .models import User
from datetime import date
import json

#Admin page
@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id

    tickets = Ticket.query.all()
    for ticket in tickets:
        ticket.screen.startTime

    return render_template('admin/index.html', title='Admin Page',  user_id=user_id, tickets=tickets)

#route for creating admin account
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data} Thanks for registering', 'success')
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form, title='Registration Page')

#route for login with the admin account
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():

        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data

            flash(f'Welcome {form.email.data} You are logged in now', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong Password please try again', 'danger')
            return redirect(url_for('login'))


    return render_template('admin/login.html', form=form, title='Login Page')

#route for updating admin account
@app.route('/updateuser/<int:id>',methods=['GET','POST'])
def updateuser(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))

    updateuser = User.query.get_or_404(id)
    form = RegistrationForm(request.form)
    if request.method =="POST":
        updateuser.name = form.name.data
        updateuser.username = form.username.data
        updateuser.email = form.email.data
        hash_password = bcrypt.generate_password_hash(form.password.data)
        updateuser.password = hash_password
        flash(f'The  {updateuser.name} profile was updated','success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.name.data = updateuser.name
    form.username.data = updateuser.username
    form.email.data = updateuser.email
    form.password.data = updateuser.password
    return render_template('admin/register.html',form=form, title='Update User',updateuser=updateuser)

#route for comparing movies
@app.route('/cmpmovies',methods=['GET','POST'])
def cmpmovies():
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))

    form = CompareMovieForm(request.form)
    movies = Movies.query.all()
    print(request.method)
    movie1 = request.form.get('movie1')
    movie2 = request.form.get('movie2')
    date = date.today()
    if request.method == "POST":
        print("BANANANANANANANANANANANA")
        print(movie1)
        return redirect(url_for('admin'))


    print(movies)
    return render_template('admin/cmpmovies.html', form=form, title='Compare Movies',movies=movies)




"""
#this needs to be added to
@app.route('/cmpmovies/results', methods=['GET','POST'])
def cmpresults():
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))

    form = CompareMovieForm(request.form)
    #movie = Movie.query.get_or_404(id)

    #join_query = session.query(Movies, Screening, Addticket).join(Movie,Movie.id == Screening.movie_id).join(Screening, Screening.id == Addticket.screen)
    
    return render_template('admin/cmpresults', form=form, title=cmpresults())
"""
#route for movie sales
@app.route('/moviesales',methods=['GET','POST'])
def moviesales():
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))

    movies = Movies.query.all()

    form = MovieSalesData(request.form)
    if request.method == "POST":
        movie = form.movie.data
        week = form.date.data

    return render_template('admin/moviesales.html', form=form, title='Movie Sales Data', movies=movies)