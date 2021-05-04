from flask import render_template, session, request, redirect, url_for, flash, make_response
from app import app, db, bcrypt
from app.cinema.models import Ticket, Movies, Screening
from app.customers.models import CustomerOrder
from .forms import RegistrationForm, LoginForm, CompareMovieForm, MovieSalesData
from .models import User
from datetime import datetime, timedelta
import json

#Admin page
@app.route('/admin')
def admin():
    if 'login_email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=session['login_email']).first()
    user_id = user.id

    tickets = Ticket.query.all()
    for ticket in tickets:
        ticket.screen.startTime

    return render_template('admin/index.html', title='Admin Page',  user_id=user_id, tickets=tickets)

@app.route('/admin/logout')
def admin_logout():

    del session['login_email']
    return redirect(url_for('home'))


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
            session['login_email'] = form.email.data

            flash(f'Welcome {form.email.data} You are logged in now', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong Password please try again', 'danger')
            return redirect(url_for('login'))


    return render_template('admin/login.html', form=form, title='Login Page')

#route for updating admin account
@app.route('/updateuser/<int:id>',methods=['GET','POST'])
def updateuser(id):
    if 'login_email' not in session:
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

def oneWeekLess(dateMax,currentDate):
    for i in range(7):
        newdate = dateMax - timedelta(days = i)
        if newdate.day == currentDate.day and newdate.month == currentDate.month and newdate.year == currentDate.year:
            print(newdate)
            return True

    return False



def ticketsPerMovie(movieId):
    if 'login_email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    count = 0
    screenings = Screening.query.filter_by(movie_id=movieId)
    for screen in screenings:
        tickets = Ticket.query.filter_by(screen_id=screen.id)
        for ticket in tickets:
            if oneWeekLess(datetime.today(), ticket.date_created):
                if ticket.taken == True:
                    count = count + 1
    return count
    


#route for comparing movies
@app.route('/cmpmovies',methods=['GET','POST'])
def cmpmovies():
    if 'login_email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))

    form = CompareMovieForm(request.form)
    movies = Movies.query.all()
    movie1 = request.form.get('movie1')
    movie2 = request.form.get('movie2')

    if request.method == "POST":
        print(movie1)
        print(movie2)
        movob = Movies.query.get_or_404(int(movie1))
        title1 = movob.title
        movob2 = Movies.query.get_or_404(int(movie2))
        title2 = movob2.title
        count1 = ticketsPerMovie(movie1)
        count2 = ticketsPerMovie(movie2)


        return render_template('admin/cmpresults.html',form=form, title = 'Compare Results', movie1 = title1, movie2 = title2, count1 = count1, count2 = count2,)


    return render_template('admin/cmpmovies.html', form=form, title='Compare Movies',movies=movies)

def allTimeSales():
    if 'login_email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))

    tickets = Ticket.query.all()
    sales = 0
    for ticket in tickets:
        if ticket.taken == True:
            sales += ticket.price
    return sales


def movieEarnings(id):
    if 'login_email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    sales = 0
    screenings = Screening.query.filter_by(movie_id = id)
    for screen in  screenings:
        tickets = Ticket.query.filter_by(screen_id = screen.id)
        for ticket in  tickets:
            if ticket.taken == True:
                sales += ticket.price
    return sales

def earningsWeekly():
    if 'login_email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    tickets = Ticket.query.all()
    print(tickets)

    startDate = datetime.today()
    print(startDate)
    currentDate = datetime.today()
    print(currentDate)
    weeklyEarnings = []
    takenTickets = []

    for ticket in tickets:
        if ticket.date_created < startDate and ticket.taken == True:
            startDate = ticket.date_created
            takenTickets.append(ticket)

    print(len(tickets))
    while len(takenTickets) > 0:
        toRemove = []
        weekSales = 0
        for ticket in takenTickets:
            if oneWeekLess(currentDate, ticket.date_created) == True:
                weekSales += ticket.price
                toRemove.append(ticket)
                print('here')
        print('here2')
        for item in toRemove:
            takenTickets.remove(item)
            print("removing", len(tickets))
        print("weekSales", weekSales)
        print(len(tickets))
        currentDate = currentDate - timedelta(days = 7)
        weeklyEarnings.append([currentDate,weekSales])

        print(currentDate)
    return weeklyEarnings


#route for movie sales
@app.route('/moviesales',methods=['GET','POST'])
def moviesales():
    if 'login_email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))

    movies = Movies.query.all()

    overallSales = allTimeSales()
    week = earningsWeekly()
    week1 = 0
    week2 = 0
    week3 = 0
    week4 = 0
    if len(week) > 0 & len(week) < 2:
        week1 = week[0][1]
    elif len(week) > 1 & len(week) < 3:
        week2 = week[1][1]
    elif len(week) > 2 & len(week) < 4:
        week3 = week[2][1]
    elif len(week)>= 4:
        week4 = week[3][1]

    form = MovieSalesData(request.form)
    if request.method == "POST":

        movieId = request.form.get('movie')
        print("before")

        movie = Movies.query.get_or_404(int(movieId))
        sales = movieEarnings(movieId)

        return render_template('admin/salesresults.html',form=form, title = 'Sales Results', movieTitle=movie.title, movieSales=sales)
    return render_template('admin/moviesales.html', form=form, title='Movie Sales Data', movies=movies ,overallSales=overallSales, week=week, week1=week1, week2=week2, week3=week3, week4=week4)