from flask import render_template, request,redirect,url_for,flash, session
from flask_login import login_user
from app import app,db,bcrypt
from .forms import CustomerRegisterForm, CustomerLoginFrom, TSF
from .model import Register

@app.route('/')
def home():

    return render_template('customer/index.html')

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

@app.route('/customer/movie', methods=['GET','POST'])
def movieSelection():
    movietitle = []
    movieprice = []
    moviediscount = []
    movietime = []
    moviedate = []
    movieplot = []
    moviegenre = []
    moviecertificate = []
    movierating = []
    for movies in cinema.models.Addticket.query.all():
        movietitle.append(movies.title)
        movieprice.append(movies.price)
        moviediscount.append(movies.discount)
        movietime.append(movies.time)
        moviedate.append(movies.date)
        movieplot.append(movies.plot)
        moviegenre.append(movies.genre)
        moviecertificate.append(movies.certificate)
        movierating.append(movies.ratingReason)
    if request.method == 'POST':
        if request.form.get('chosenTime'):
            session['movie'] = {movietime[0],movieprice[0],moviediscount[0],moviedate[0],movietime[0]}
            return redirect('/customer/ticket')
    return render_template('/customer/movie.html',
        movietitle = movietitle,
        movieprice = movieprice,
        movietime = movietime,
        moviedate = moviedate,
        movieplot = movieplot,
        moviegenre = moviegenre,
        movierating = movierating,
        moviecertificate = moviecertificate,
        title = 'Movie Selection')


#route to allow customers to select what type of ticket they want and the amount of tickets they want.
@app.route('/customer/ticket', methods=['GET','POST'])
def ticketSelection():
    session['movie'] = 'Tron'
    form = TSF()
    priceDiscount = 0.99
    childPrice = round(priceDiscount * 9.00,2)
    teenPrice = round(priceDiscount * 10.00,2)
    adultPrice = round(priceDiscount * 11.00,2)
    elderlyPrice = round(priceDiscount * 9.00,2)
    flash('Hello World')
    #Assuming we are using sessions to carry over the specific movie the customer wants to this route (remove if we are not)
    if 'movie' in session:
        flash('Inside movie')
        movie = session['movie']
        if request.method == 'POST':
            flash('Inside post')
            if request.form.get('Confirm'):
                flash('Indise confirm')
                if form.child.data == 0 and form.teen.data == 0 and form.adult.data == 0 and form.elderly.data == 0:
                    flash('Inside checks')
                    flash('No tickets have been selected. Please select the tickets you would like for the movie.')
                    return redirect('/customer/ticket')
                if form.child.data != 0:
                    childTicket = form.child.data
                else:
                    childTicket = 0
                if form.teen.data != 0:
                    teenTicket = form.teen.data
                else:
                    teenTicket = 0
                if form.adult.data != 0:
                    adultTicket = form.adult.data
                else:
                    adultTicket = 0
                if form.elderly.data != 0:
                    elderlyTicket = form.elderly.data
                else:
                    elderlyTicket = 0
                session['ticketChosen'] = {{movie},{childTicket},{teenTicket},{adultTicket},{elderlyTicket}}
                flash('The tickets have been added to your basket. Proceed to payment when ready.')
                return redirect('/')
    return render_template('customer/tickets.html',
        childPrice = childPrice,
        teenPrice = teenPrice,
        adultPrice = adultPrice,
        elderlyPrice = elderlyPrice,
        form = form,
        title='Ticket Selection')