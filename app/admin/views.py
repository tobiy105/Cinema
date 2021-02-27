from flask import render_template, session, request, redirect, url_for, flash, make_response
from app import app, db, bcrypt
from app.cinema.models import Addticket
from .forms import RegistrationForm, LoginForm
from .models import User

#Admin page
@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id

    tickets = Addticket.query.all()
    print(tickets)

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

