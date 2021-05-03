from flask import render_template,session, request,redirect,url_for,flash,current_app
from app import app,db,photos, search
from .models import Addticket
from .forms import Addtickets, MovieForm
import requests
import secrets
import os

#route for home
@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    tickets = Addticket.query.filter(Addticket.stock > 0).order_by(Addticket.id.desc()).paginate()

    return render_template('cinema/index.html', tickets=tickets)


#route for result of finding a ticket by using search word
@app.route('/result')
def result():
    searchword = request.args.get('q')
    tickets = Addticket.query.msearch(searchword, fields=['title','genres','price'] , limit=10)
    return render_template('cinema/result.html',tickets=tickets)

#route for displaying a tickets found from word search
@app.route('/ticket/<int:id>')
def single_page(id):
    ticket = Addticket.query.get_or_404(id)
    return render_template('cinema/single_page.html',ticket=ticket)


#route for adding tickets
@app.route('/addticket', methods=['GET','POST'])
def addticket():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    form = Addtickets(request.form)

    response = None
    url = "https://imdb8.p.rapidapi.com/title/auto-complete"
    headers = {
        'x-rapidapi-key': "356f657f36msh048f021d349390fp17271fjsne23da7801c20",
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    form1 = MovieForm(request.form)
    if request.method == 'POST' and form1.validate():
        title = form1.title.data
        querystring = {"q": title}
        response = requests.request("GET", url, headers=headers, params=querystring)
        # flash(f'Response: {response.text}')

        # to query details need to extract value from the id field, starting "tt" eg: "tt944947"
        foundID = False

        for i in range(0, len(response.text)):
            if foundID:
                break
            if response.text[i] == '"':
                # flash('Found a "')
                for j in range(i + 1, len(response.text)):
                    if response.text[j] == '"':
                        # flash('Found another "')
                        # flash(f'Substring    {response.text[i + 10: i + 20]}')
                        if response.text[i + 1: i + 3] == "tt":  # if the susbtring is an id
                            id = response.text[i + 1: j]  # get the movie id
                            foundID = True
                            # flash(f'ID: {id}')
                        break

        # now that we have the ID given by the IMDB database, we can query again for movie details
        # this id can be used for querying in general

        url = "https://imdb8.p.rapidapi.com/title/get-overview-details"

        querystring = {"tconst": id, "currentCountry": "GB"}

        headers = {
            'x-rapidapi-key': "356f657f36msh048f021d349390fp17271fjsne23da7801c20",
            'x-rapidapi-host': "imdb8.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        # flash(f'Response: {response.text}')

        foundTitle = False
        foundRunningTime = False
        foundPlot = False
        foundCertificates = False
        foundYear = False
        foundRatingReason = False
        foundGenres = False


        for i in range(0, len(response.text)):
            if response.text[i] == '"':
                for j in range(i + 1, len(response.text)):
                    if response.text[j] == '"':
                        field = response.text[i + 1: j]


                        if field == "title" and not foundTitle:  # the returned string has multiple fields called title
                            if response.text[j + 1] == ':' and response.text[j + 2] == '"':
                                for k in range(j + 3, len(response.text)):
                                    if response.text[k] == '"':  # end of title field value
                                        title = response.text[j + 3: k]
                                        foundTitle = True
                                        form.title.data=title

                                        break
                        elif field == "runningTimeInMinutes" and not foundRunningTime:
                            for k in range(j + 3, len(response.text)):
                                if response.text[k] == ',':  # end of running time field
                                    runningTime = response.text[j + 2: k]
                                    foundRunningTime = True
                                    form.time.data = runningTime

                                    break

                        elif field == "year" and not foundYear:
                            for k in range(j + 3, len(response.text)):
                                if response.text[k] == '}':  # end of running time field
                                    year = response.text[j + 2: k]
                                    foundYear = True
                                    form.date.data = year

                                    break

                        elif field == "plotSummary" and not foundPlot:
                            for k in range(j + 1, len(response.text)):
                                if response.text[k: k + 4] == "text":
                                    for x in range(k + 7, len(response.text)):
                                        if (response.text[x] == '"'):
                                            plotSummary = response.text[k + 7: x]
                                            foundPlot = True
                                            form.plot.data = plotSummary

                                            break
                                    break

                        elif field == "certificate" and not foundCertificates:
                            for k in range(j + 3, len(response.text)):
                                if response.text[k] == '"':
                                    certificate = response.text[j + 3: k]
                                    foundCertificates = True
                                    form.certificate.data = certificate

                                    break

                        elif field == "ratingReason" and not foundRatingReason:
                            for k in range(j + 3, len(response.text)):
                                if response.text[k] == '"':
                                    ratingReason = response.text[j + 3: k]
                                    foundRatingReason = True
                                    form.ratingReason.data = ratingReason

                                    break

                        elif field == "genres" and not foundGenres:
                            for k in range(j + 5, len(response.text)):
                                if response.text[k] == ']':
                                    genres = response.text[j + 4: k]
                                    genres = genres.replace('"', '')
                                    genres = genres.replace(',', ', ')
                                    foundGenres = True
                                    form.genres.data = genres

                                    break



    if request.method=="POST" and form.validate():
        title = form.title.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        time = form.time.data
        date = form.date.data
        plot = form.plot.data
        genres = form.genres.data
        certificate = form.certificate.data
        ratingReason = form.ratingReason.data

        newticket = Addticket(title=title,price=price,discount=discount,stock=stock,time=time,date=date,
                              plot=plot,genres=genres,certificate=certificate,ratingReason=ratingReason)
        db.session.add(newticket)
        flash(f'The ticket {title} was added in database','success')

        db.session.commit()
        return redirect(url_for('admin'))


    return render_template('cinema/addticket.html',form1=form1, form=form, title='Add a Ticket')

#route for updating ticket
@app.route('/updateticket/<int:id>', methods=['GET','POST'])
def updateticket(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    form = Addtickets(request.form)
    ticket = Addticket.query.get_or_404(id)
    

    

    if request.method =="POST" :
        ticket.title = form.title.data
        ticket.price = form.price.data
        ticket.discount = form.discount.data
        ticket.stock = form.stock.data
        ticket.time = form.time.data
        ticket.date = form.date.data
        ticket.plot = form.plot.data
        ticket.genres = form.genres.data
        ticket.certificate = form.certificate.data
        ticket.ratingReason = form.ratingReason.data


        flash('The ticket was updated','success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.title.data = ticket.title
    form.price.data = ticket.price
    form.discount.data = ticket.discount
    form.stock.data = ticket.stock
    form.time.data = ticket.time
    form.date.data= ticket.date
    form.plot.data = ticket.plot
    form.genres.data = ticket.genres
    form.certificate.data = ticket.certificate
    form.ratingReason.data = ticket.ratingReason
    form1=form


    return render_template('cinema/addticket.html',form1=form1, form=form, title='Update Ticket',getticket=ticket)

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
        flash(f'The ticket {ticket.title} was delete from your record','success')
        return redirect(url_for('admin'))
    flash(f'Can not delete the ticket','success')
    return redirect(url_for('admin'))


# route for movie search (view movie details)
@app.route('/customer/viewMovieDetails', methods=['GET', 'POST'])
def viewMovieDetails():
    response = None
    url = "https://imdb8.p.rapidapi.com/title/auto-complete"
    headers = {
        'x-rapidapi-key': "356f657f36msh048f021d349390fp17271fjsne23da7801c20",
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    form = MovieForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        querystring = {"q": title}
        response = requests.request("GET", url, headers=headers, params=querystring)
        # flash(f'Response: {response.text}')

        # to query details need to extract value from the id field, starting "tt" eg: "tt944947"
        foundID = False

        for i in range(0, len(response.text)):
            if foundID:
                break
            if response.text[i] == '"':
                # flash('Found a "')
                for j in range(i + 1, len(response.text)):
                    if response.text[j] == '"':
                        # flash('Found another "')
                        # flash(f'Substring    {response.text[i + 10: i + 20]}')
                        if response.text[i + 1: i + 3] == "tt":  # if the susbtring is an id
                            id = response.text[i + 1: j]  # get the movie id
                            foundID = True
                            # flash(f'ID: {id}')
                        break

        # now that we have the ID given by the IMDB database, we can query again for movie details
        # this id can be used for querying in general

        url = "https://imdb8.p.rapidapi.com/title/get-overview-details"

        querystring = {"tconst": id, "currentCountry": "GB"}

        headers = {
            'x-rapidapi-key': "356f657f36msh048f021d349390fp17271fjsne23da7801c20",
            'x-rapidapi-host': "imdb8.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        # flash(f'Response: {response.text}')

        foundTitle = False
        foundRunningTime = False
        foundPlot = False
        foundCertificates = False
        foundYear = False
        foundRatingReason = False
        foundGenres = False
        foundUrls = False

        for i in range(0, len(response.text)):
            if response.text[i] == '"':
                for j in range(i + 1, len(response.text)):
                    if response.text[j] == '"':
                        field = response.text[i + 1: j]

                        if field == "urls" and not foundUrls:  # the returned string has multiple fields called title
                            if response.text[1 + 1] == ':' and response.text[j + 2] == '"':
                                for k in range(j + 3, len(response.text)):
                                    if response.text[k] == '"':  # end of title field value
                                        urls = response.text[j + 3: k]
                                        foundUrls = True
                                        #flash(f'Found urls: {urls}')
                                        break
                        if field == "title" and not foundTitle:  # the returned string has multiple fields called title
                            if response.text[j + 1] == ':' and response.text[j + 2] == '"':
                                for k in range(j + 3, len(response.text)):
                                    if response.text[k] == '"':  # end of title field value
                                        title = response.text[j + 3: k]
                                        foundTitle = True
                                        flash(f'Title: {title}')
                                        break
                        elif field == "runningTimeInMinutes" and not foundRunningTime:
                            for k in range(j + 3, len(response.text)):
                                if response.text[k] == ',':  # end of running time field
                                    runningTime = response.text[j + 2: k]
                                    foundRunningTime = True
                                    flash(f'Running Time: {runningTime}')
                                    break
                        elif field == "year" and not foundYear:
                            for k in range(j + 3, len(response.text)):
                                if response.text[k] == '}':  # end of running time field
                                    year = response.text[j + 2: k]
                                    foundYear = True
                                    flash(f'Year: {year}')
                                    break
                        elif field == "plotSummary" and not foundPlot:
                            for k in range(j + 1, len(response.text)):
                                if response.text[k: k + 4] == "text":
                                    for x in range(k + 7, len(response.text)):
                                        if (response.text[x] == '"'):
                                            plotSummary = response.text[k + 7: x]
                                            foundPlot = True
                                            flash(f'Plot Summary: {plotSummary}')
                                            break
                                    break
                        elif field == "certificate" and not foundCertificates:
                            for k in range(j + 3, len(response.text)):
                                if response.text[k] == '"':
                                    certificate = response.text[j + 3: k]
                                    foundCertificates = True
                                    flash(f'Certificate: {certificate}')
                                    break

                        elif field == "ratingReason" and not foundRatingReason:
                            for k in range(j + 3, len(response.text)):
                                if response.text[k] == '"':
                                    ratingReason = response.text[j + 3: k]
                                    foundRatingReason = True
                                    flash(f'Reason for Rating: {ratingReason}')
                                    break
                        elif field == "genres" and not foundGenres:
                            for k in range(j + 5, len(response.text)):
                                if response.text[k] == ']':
                                    genres = response.text[j + 4: k]
                                    genres=genres.replace('"','')
                                    genres=genres.replace(',',', ')
                                    foundGenres = True
                                    flash(f'Genres: {genres}')
                                    break
    
        url = "https://imdb8.p.rapidapi.com/title/get-top-crew"
        response = requests.request("GET", url, headers=headers, params=querystring)
        foundDirector = False
        director = ""

        for i in range(0, len(response.text)):
            if response.text[i] == '"' and not foundDirector:
                for j in range(i + 1, len(response.text)):
                    if response.text[j] == '"':
                        field = response.text[i + 1: j]
                        if field == "name":
                            for k in range(j + 3, len(response.text)):
                                if response.text[k] == '"':
                                    director = response.text[j + 3 : k]
                                    foundDirector = True
                                    flash(f'Director: {director}')
                                    break
                        else:
                            break

    return render_template('cinema/viewMovieDetails.html', form=form)
