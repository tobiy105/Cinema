from flask import render_template,session, request,redirect,url_for,flash,current_app,make_response
from flask_login import login_required, current_user, logout_user, login_user
from app import app,db,photos, search,bcrypt,login_manager
from .forms import Employee, EmployeeLoginFrom, EmployeeRegisterForm
from .models import Employee
from app.cinema.models import Addticket, Category

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
    form = EmployeeRegisterForm()
    if form.validate_on_submit():
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
    form = EmployeeLoginFrom()
    if form.validate_on_submit():
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


@app.route('/employee/logout')
def employee_logout():
    logout_user()
    return redirect(url_for('home'))

