from flask import render_template,session, request,redirect,url_for,flash,current_app,make_response
from flask_login import login_required, current_user, logout_user, login_user
from app import app,db,photos, search,bcrypt,login_manager
from .forms import Employee, EmployeeLoginFrom, EmployeeRegisterForm
from .models import Employee
from app.cinema.models import Addticket

#Employee page
@app.route('/employee')
def employee():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    page = request.args.get('page', 1, type=int)
    tickets = Addticket.query.filter(Addticket.stock > 0).order_by(Addticket.id.desc()).paginate()

    return render_template('employee/index.html', title='Admin Page', tickets=tickets)

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
            login_user(user)
            flash('You are login now!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('employee'))
        flash('Incorrect email and password', 'danger')
        return redirect(url_for('employeeLogin'))

    return render_template('employee/login.html', form=form)


# route for updating the employee account
@app.route('/updateemployee/<int:id>', methods=['GET', 'POST'])
def updateemployee(id):
    if 'email' not in session:
        flash('Login first please', 'danger')
        return redirect(url_for('login'))

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

# #route for creating admin account
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm(request.form)
#     if request.method == 'POST' and form.validate():
#         hash_password = bcrypt.generate_password_hash(form.password.data)
#         user = User(name=form.name.data, username=form.username.data, email=form.email.data,
#                     password=hash_password)
#         db.session.add(user)
#         db.session.commit()
#         flash(f'Welcome {form.name.data} Thanks for registering', 'success')
#         return redirect(url_for('login'))
#     return render_template('admin/register.html', form=form, title='Registration Page')
#
# #route for login with the admin account
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm(request.form)
#     if request.method == "POST" and form.validate():
#         user = User.query.filter_by(email = form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             session['email'] = form.email.data
#             flash(f'Welcome {form.email.data} You are logged in now', 'success')
#             return redirect(request.args.get('next') or url_for('admin'))
#         else:
#             flash('Wrong Password please try again', 'danger')
#             return redirect(url_for('login'))
#
#
#     return render_template('admin/login.html', form=form, title='Login Page')
#
# #route for updating admin account
# @app.route('/updateuser/<int:id>',methods=['GET','POST'])
# def updateuser(id):
#     if 'email' not in session:
#         flash('Login first please','danger')
#         return redirect(url_for('login'))
#
#     updateuser = User.query.get_or_404(id)
#     form = RegistrationForm(request.form)
#     if request.method =="POST":
#         updateuser.name = form.name.data
#         updateuser.username = form.username.data
#         updateuser.email = form.email.data
#         hash_password = bcrypt.generate_password_hash(form.password.data)
#         updateuser.password = hash_password
#         flash(f'The  {updateuser.name} profile was updated','success')
#         db.session.commit()
#         return redirect(url_for('admin'))
#     form.name.data = updateuser.name
#     form.username.data = updateuser.username
#     form.email.data = updateuser.email
#     form.password.data = updateuser.password
#     return render_template('admin/register.html',form=form, title='Update User',updateuser=updateuser)

