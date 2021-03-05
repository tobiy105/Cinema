from flask import render_template,session, request,redirect,url_for,flash,current_app
from app import app,db,photos, search
from .models import Addticket, Movies, Screening
from .forms import Addtickets, SearchMovieForm, Movie, Screen
import requests
import secrets
import os

#route for home
@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    tickets = Addticket.query.filter(Addticket.stock > 0).order_by(Addticket.id.desc()).paginate()

    return render_template('cinema/index.html', tickets=tickets)
#
#query search for movie
def movie():
    movie = Movies.query.join(Screening, (Movies.id == Screening.movie_id)).all()
    return movie

#route for home
@app.route('/movies')
def movies():

    movies = Movies.query.all()

    return render_template('cinema/movies.html', movies=movies)

#route for adding screen
@app.route('/addscreen', methods=['GET','POST'])
def addscreen():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    form = Screen(request.form)
    movies = Movies.query.all()

    if request.method=="POST":
        startTime = form.startTime.data
        endTime = form.endTime.data
        date = form.date.data
        theatre = form.theatre.data
        seats = form.seats.data
        movie_id = request.form.get('movie')


        addscreen = Screening(startTime=startTime,endTime=endTime,date=date,theatre=theatre,seats=seats,movie_id=movie_id)
        db.session.add(addscreen)
        flash(f'The Screen was added in database','success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('cinema/addscreen.html', form=form, title='Add a Product' ,movies=movies)



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


#route for adding movies
@app.route('/addmovie', methods=['GET','POST'])
def addmovie():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    form = Movie(request.form)


    data = ""
    response = None
    url = "https://imdb8.p.rapidapi.com/title/auto-complete"
    headers = {
        'x-rapidapi-key': "356f657f36msh048f021d349390fp17271fjsne23da7801c20",
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    form1 = SearchMovieForm(request.form)
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


                        if response.text[i + 1: i + 9] == "imageUrl":  # if the susbtring is an id

                            for k in range(j + 3, len(response.text)):
                                if response.text[k] == '"':  # end of title field value
                                    url = response.text[j + 3: k]
                                    foundUrls = True
                                    data=url
                                    form.image.data=data

                                    break
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
                                    form.duration.data = runningTime

                                    break

                        elif field == "year" and not foundYear:
                            for k in range(j + 3, len(response.text)):
                                if response.text[k] == '}':  # end of running time field
                                    year = response.text[j + 2: k]
                                    foundYear = True
                                    form.releaseDate.data = year

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
        duration = form.duration.data
        releaseDate = form.releaseDate.data
        plot = form.plot.data
        genres = form.genres.data
        certificate = form.certificate.data
        ratingReason = form.ratingReason.data
        image = form.image.data
        newMovie = Movies(title=title,duration=duration,releaseDate=releaseDate,
                              plot=plot,genres=genres,certificate=certificate,ratingReason=ratingReason, image=image)
        db.session.add(newMovie)
        flash(f'The ticket {title} was added in database','success')
        db.session.commit()
        return redirect(url_for('movies'))
    return render_template('cinema/addmovie.html', form1=form1, form=form,data=data, title='Add a Movie')

# route for updating ticket
@app.route('/updatemovie/<int:id>', methods=['GET', 'POST'])
def updatemovie(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    form = Movie(request.form)
    movie = Movies.query.get_or_404(id)

    if request.method == "POST":
        movie.title = form.title.data
        movie.duration = form.duration.data
        movie.plot = form.plot.data
        movie.genres = form.genres.data
        movie.certificate = form.certificate.data
        movie.ratingReason = form.ratingReason.data
        movie.releaseDate = form.releaseDate.data
        flash('The ticket was updated', 'success')
        db.session.commit()
        return redirect(url_for('movies'))
    form.title.data = movie.title
    form.duration.data = movie.duration
    form.releaseDate.data = movie.releaseDate
    form.plot.data = movie.plot
    form.genres.data = movie.genres
    form.certificate.data = movie.certificate
    form.ratingReason.data = movie.ratingReason
    form.image.data = movie.image
    form1 = form
    return render_template('cinema/addmovie.html', form1=form1, form=form, title='Update Ticket', getmovie=movie)

# route for deleting ticket
@app.route('/deletemovie/<int:id>', methods=['POST'])
def deletemovie(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    movie = Movies.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(movie)
        db.session.commit()
        flash(f'The ticket {movie.title} was delete from your record', 'success')
        return redirect(url_for('movies'))
    flash(f'Can not delete the movie', 'success')
    return redirect(url_for('admin'))

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

    form1 = SearchMovieForm(request.form)
    if request.method == 'POST' and form1.validate():
        title = form1.title.data
        querystring = {"q": title}
        response = requests.request("GET", url, headers=headers, params=querystring)
        # to query details need to extract value from the id field, starting "tt" eg: "tt944947"
        foundID = False

        for i in range(0, len(response.text)):
            if foundID:
                break
            if response.text[i] == '"':
                for j in range(i + 1, len(response.text)):
                    if response.text[j] == '"':
                        if response.text[i + 1: i + 3] == "tt":  # if the susbtring is an id
                            id = response.text[i + 1: j]  # get the movie id
                            foundID = True
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
    form.date.data = ticket.date
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
    data =""
    response = None
    url = "https://imdb8.p.rapidapi.com/title/auto-complete"
    headers = {
        'x-rapidapi-key': "356f657f36msh048f021d349390fp17271fjsne23da7801c20",
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    form = SearchMovieForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        querystring = {"q": title}
        response = requests.request("GET", url, headers=headers, params=querystring)

        # to query details need to extract value from the id field, starting "tt" eg: "tt944947"
        foundID = False
        foundUrls = False

        for i in range(0, len(response.text)):
            if foundID:
                break
            if response.text[i] == '"':

                for j in range(i + 1, len(response.text)):
                    if response.text[j] == '"':

                        if response.text[i + 1: i + 3] == "tt":  # if the susbtring is an id
                            id = response.text[i + 1: j]  # get the movie id
                            foundID = True

                        if response.text[i + 1: i + 9] == "imageUrl":  # if the susbtring is an id

                            for k in range(j + 3, len(response.text)):
                                if response.text[k] == '"':  # end of title field value
                                    url = response.text[j + 3: k]
                                    foundUrls = True
                                    data = url

                                    break
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
                                        flash(f'Found Title: {title}')
                                        break
                        elif field == "runningTimeInMinutes" and not foundRunningTime:
                            for k in range(j + 3, len(response.text)):
                                if response.text[k] == ',':  # end of running time field
                                    runningTime = response.text[j + 2: k]
                                    foundRunningTime = True
                                    flash(f'Found Running Time: {runningTime}')
                                    break

                        elif field == "year" and not foundYear:
                            for k in range(j + 3, len(response.text)):
                                if response.text[k] == '}':  # end of running time field
                                    year = response.text[j + 2: k]
                                    foundYear = True
                                    flash(f'Found Year: {year}')
                                    break

                        elif field == "plotSummary" and not foundPlot:
                            for k in range(j + 1, len(response.text)):
                                if response.text[k: k + 4] == "text":
                                    for x in range(k + 7, len(response.text)):
                                        if (response.text[x] == '"'):
                                            plotSummary = response.text[k + 7: x]
                                            foundPlot = True
                                            flash(f'Found Plot Summary: {plotSummary}')
                                            break
                                    break

                        elif field == "certificate" and not foundCertificates:
                            for k in range(j + 3, len(response.text)):
                                if response.text[k] == '"':
                                    certificate = response.text[j + 3: k]
                                    foundCertificates = True
                                    flash(f'Found Certificate: {certificate}')
                                    break

                        elif field == "ratingReason" and not foundRatingReason:
                            for k in range(j + 3, len(response.text)):
                                if response.text[k] == '"':
                                    ratingReason = response.text[j + 3: k]
                                    foundRatingReason = True
                                    flash(f'Found reason for rating: {ratingReason}')
                                    break

                        elif field == "genres" and not foundGenres:
                            for k in range(j + 5, len(response.text)):
                                if response.text[k] == ']':
                                    genres = response.text[j + 4: k]
                                    genres=genres.replace('"','')
                                    genres=genres.replace(',',', ')
                                    foundGenres = True
                                    flash(f'Found genres: {genres}')
                                    break

    return render_template('cinema/viewMovieDetails.html', form=form, data=data)