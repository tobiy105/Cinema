from flask import render_template, request,redirect,url_for,flash, request
from flask_login import login_user
from app import app,db,bcrypt
from .forms import CustomerRegisterForm, CustomerLoginFrom, CustomerMovieForm
from .model import Register
import requests

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

#route for movie search (view movie details)
@app.route('/customer/viewMovieDetails', methods = ['GET', 'POST'])
def viewMovieDetails():
    response = None
    url = "https://imdb8.p.rapidapi.com/title/auto-complete"
    headers = {
    'x-rapidapi-key': "356f657f36msh048f021d349390fp17271fjsne23da7801c20",
    'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    form = CustomerMovieForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        querystring = {"q":title}
        response = requests.request("GET", url, headers = headers, params = querystring)
        #flash(f'Response: {response.text}')
        
        #to query details need to extract value from the id field, starting "tt" eg: "tt944947"
        foundID = False

        for i in range(0, len(response.text)):
            if foundID:
                break
            if response.text[i] == '"':
                #flash('Found a "')
                for j in range(i + 1, len(response.text)):
                    if response.text[j] == '"':
                        #flash('Found another "')
                        #flash(f'Substring    {response.text[i + 1 : i + 3]}')
                        if response.text[i + 1 : i + 3] == "tt": #if the susbtring is an id
                            id = response.text[i + 1 : j] #get the movie id
                            foundID = True
                            #flash(f'ID: {id}')
                        break

        #now that we have the ID given by the IMDB database, we can query again for movie details
        #this id can be used for querying in general

        url = "https://imdb8.p.rapidapi.com/title/get-overview-details"

        querystring = {"tconst":id,"currentCountry":"GB"}

        headers = {
            'x-rapidapi-key': "356f657f36msh048f021d349390fp17271fjsne23da7801c20",
            'x-rapidapi-host': "imdb8.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        #flash(f'Response: {response.text}')

        foundTitle = False
        foundRunningTime = False
        foundPlot = False
        foundCertificates = False

        for i in range(0, len(response.text)):
            if response.text[i] == '"':
                for j in range(i + 1, len(response.text)):
                    if response.text[j] == '"':
                        field = response.text[i + 1 : j]
                        if field == "title" and not foundTitle: #the returned string has multiple fields called title
                            if response.text[j + 1] == ':' and response.text[j + 2] == '"':
                                for k in range(j + 3, len(response.text)):
                                    if response.text[k] == '"': #end of title field value
                                        title = response.text[j + 3 : k]
                                        foundTitle = True
                                        flash(f'Found Title: {title}')
                                        break
                        elif field == "runningTimeInMinutes" and not foundRunningTime:
                            for k in range (j + 3, len(response.text)):
                                if response.text[k] == ',': #end of running time field
                                    runningTime =  response.text[j + 2 : k]
                                    foundRunningTime = True
                                    flash(f'Found Running Time: {runningTime}')
                                    break
                        elif field == "plotSummary" and not foundPlot:
                            for k in range(j + 1, len(response.text)):
                                if response.text[k : k + 4] == "text":
                                    for x in range(k + 7, len(response.text)):
                                        if (response.text[x] == '"'):
                                            plotSummary = response.text[k + 7 : x]
                                            foundPlot = True
                                            flash(f'Found Plot Summary: {plotSummary}')
                                            break
                                    break
                        elif field == "certificate" and not foundCertificates:
                            for k in range(j + 3, len(response.text)):
                                if response.text[k] == '"':
                                    certificate = response.text[j + 3 : k]
                                    foundCertificates = True
                                    flash(f'Found Certificate: {certificate}')
                                    break

    return render_template('customer/viewMovieDetails.html', form = form)