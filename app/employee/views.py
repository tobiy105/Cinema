from flask import render_template,session, request,redirect,url_for,flash,current_app,make_response
from flask_login import login_required, current_user, logout_user, login_user
from app import app,db,photos, search,bcrypt,login_manager
from .forms import Employee, EmployeeLoginFrom, EmployeeRegisterForm, PayWithCashForm
from .models import Employee
from app.cinema.models import Ticket, Movies, Screening
import datetime
from datetime import date
#Employee page
@app.route('/employee')
def employee():
    if 'employee_id' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

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



