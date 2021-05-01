from flask import render_template,session, request,redirect,url_for,flash,current_app
from app import app,db,photos, search
from .models import Ticket, Movies, Screening, Catagory
from .forms import Tickets, SearchMovieForm, Movie, Screen, TSF
import requests
import datetime
from datetime import date
import secrets
import os
import qrcode

#route for home 
@app.route('/')
def home():
    movies = Movies.query.all()
    return render_template('cinema/index.html', movies=movies)

#query search for movie
def movie():
    movie = Movies.query.join(Screening, (Movies.id == Screening.movie_id)).all()
    return movie

#query search for screen
def screen():
    screen = Screening.query.join(Ticket, (Screening.id == Ticket.screen_id)).all()
    return screen

#route for movies
@app.route('/movies')
def movies():

    movies = Movies.query.all()

    return render_template('cinema/movies.html', movies=movies)

#route for screens
@app.route('/screen')
def screens():
    screens = Screening.query.all()
    return render_template('cinema/screen.html', screens=screens)

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
        movie = Movies.query.get_or_404(movie_id)
        for i in range(seats):
            price = movie.price
            if i >= 14 and i < 20:
                price = float(price) * 1.25

            discount = 0
            seatNo = i
            num = Screening.query.all()
            screenID = len(num)
            screen_id = screenID
            newticket = Ticket(price=price, discount=discount, seatNo=seatNo, screen_id=screen_id)

            db.session.add(newticket)
            session['ticket_id'] = newticket.id
            flash(f'The ticket with seat number {seatNo} was added in database', 'success')
            db.session.commit()


        return redirect(url_for('screens'))

    return render_template('cinema/addscreen.html', form=form, title='Add a Product' ,movies=movies)

# route for updating ticket
@app.route('/updatescreen/<int:id>', methods=['GET', 'POST'])
def updatescreen(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    form = Screen(request.form)
    screen = Screening.query.get_or_404(id)
    screens = Screening.query.all()
    movies = Movies.query.all()
    movie = request.form.get('movie')
    if request.method == "POST":
        screen.startTime = form.startTime.data
        screen.endTime = form.endTime.data
        screen.date = form.date.data
        screen.theatre = form.theatre.data
        screen.seats = form.seats.data
        screen.movie_id = movie

        flash('The screen was updated', 'success')
        db.session.commit()
        return redirect(url_for('screens'))
    form.startTime.data = screen.startTime
    form.endTime.data = screen.endTime
    form.date.data = screen.date
    form.theatre.data = screen.theatre
    form.seats.data = screen.seats
    movie=screen.movie.title

    return render_template('cinema/addscreen.html',form=form, title='Update Ticket', getscreen=screen)

# route for deleting ticket
@app.route('/deletescreen/<int:id>', methods=['POST'])
def deletescreen(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    screen = Screening.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(screen)
        db.session.commit()
        flash(f'The ticket {screen.id} was delete from your record', 'success')
        return redirect(url_for('screens'))
    flash(f'Can not delete the screen', 'success')
    return redirect(url_for('screens'))


#route for result of finding a ticket by using search word
@app.route('/result')
def result():
    searchword = request.args.get('q')
    movies = Movies.query.msearch(searchword, fields=['title','genres'], limit=10)
    return render_template('cinema/result.html',movies=movies)

#route for displaying a tickets found from word search
@app.route('/ticket/<int:id>')
def single_page(id):
    movie = Movies.query.get_or_404(id)
    screens = Screening.query.filter_by(movie_id=id)
    session['movie'] = id
    for screen in screens:
        day = datetime.datetime.strptime(str(screen.date), '%Y-%m-%d').weekday()

        time_9 = "09:00:00"
        time9 = datetime.datetime.strptime(time_9, "%H:%M:%S")

        time_12 = "12:00:00"
        time12 = datetime.datetime.strptime(time_12, "%H:%M:%S")
        time_15 = "15:00:00"
        time15 = datetime.datetime.strptime(time_15, "%H:%M:%S")
        time_18 = "18:00:00"
        time18 = datetime.datetime.strptime(time_18, "%H:%M:%S")



    return render_template('cinema/single_page.html',movie=movie, screens=screens, day=day, time9=time9, time12=time12, time15=time15, time18=time18)

#route for confirm ticket
@app.route('/corfirmqrcode/', methods=['GET','POST'])
def corfirmqrcode(id):
    print(id)

    ticket = "Ticket.query.get_or_404(id)"
    taken = ticket.taken
    paid = ""
    if taken == True:
        paid = "Paid for the ticket"

    return render_template('employee/corfirmqrcode.html',ticket=ticket, taken=taken)

#route for displaying a tickets found from word search
@app.route('/seats/<int:id>', methods=['GET','POST'])
def seats_page(id):

    screen = Screening.query.get_or_404(id)
    tickets = Ticket.query.filter_by(screen_id=id)
    session['screen'] = id
    arr = []

    for i in range(screen.seats):
        arr.append(i)
        for ticket in tickets:

            if i == ticket.seatNo and ticket.taken==True:
                arr.remove(i)

    if request.method == "POST":
        print("open")

        return render_template('cinema/seats.html', screen=screen, tickets=tickets, arr=arr)
    return render_template('cinema/seats.html',screen=screen, tickets=tickets, arr=arr)

#route to allow customers to select what type of ticket they want and the amount of tickets they want.
@app.route('/customer/ticket/<int:id>', methods=['GET','POST'])
def ticketSelection(id):
    movieID = session['movie']
    screenID = session['screen']
    movie = Movies.query.get_or_404(movieID)
    screen = Screening.query.get_or_404(screenID)
    session['screen'] = id
    form = TSF(request.form)

    price = float(movie.price)

    childPrice = round(price * 0.80,2)
    teenPrice = round(price * 0.90,2)
    adultPrice = round(price * 1.00,2)
    elderlyPrice = round(price * 0.80,2)

    #Assuming we are using sessions to carry over the specific movie the customer wants to this route (remove if we are not)
    if 'movie' in session:
        if request.method == 'POST' and  form.validate():
            if request.form.get('child') == None and request.form.get('teen') == None and request.form.get('adult') == None and request.form.get('elderly') == None:
                flash('No tickets have been selected. Please select the tickets you would like for the movie.')
                return redirect(url_for('ticketSelection',id=screen.id))
            if request.form.get('child') != None:
                childTicket = request.form.get('child')
            else:
                childTicket = 0
            if request.form.get('teen') != None:
                teenTicket = request.form.get('teen')
            else:
                teenTicket = 0
            if request.form.get('adult') != None:
                adultTicket = request.form.get('adult')
            else:
                adultTicket = 0
            if request.form.get('elderly') != None:
                elderlyTicket = request.form.get('elderly')
            else:
                elderlyTicket = 0
            addTickets = Catagory(child=childTicket,teen=teenTicket,adult=adultTicket,elderly=elderlyTicket)
            db.session.add(addTickets)
            totalTickets = childTicket + teenTicket + adultTicket + elderlyTicket
            session['child'] = childTicket
            session['teen'] = teenTicket
            session['adult'] = adultTicket
            session['elderly'] = elderlyTicket
            session['total'] = totalTickets
            flash('The tickets have been added to your basket. Proceed to payment when ready.')
            return redirect(url_for('seats_page',id=screen.id))

    return render_template('cinema/tickets.html',
        childPrice = childPrice,
        teenPrice = teenPrice,
        adultPrice = adultPrice,
        elderlyPrice = elderlyPrice,
        form = form,
        title='Ticket Selection')



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
        price = form.price.data
        newMovie = Movies(title=title,duration=duration,releaseDate=releaseDate,
                              plot=plot,genres=genres,certificate=certificate,ratingReason=ratingReason,price=price,image=image)
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
        movie.price = form.price.data
        flash('The movie was updated', 'success')
        db.session.commit()
        return redirect(url_for('movies'))
    form.title.data = movie.title
    form.duration.data = movie.duration
    form.releaseDate.data = movie.releaseDate
    form.plot.data = movie.plot
    form.genres.data = movie.genres
    form.certificate.data = movie.certificate
    form.ratingReason.data = movie.ratingReason
    form.price.data = movie.price
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
        flash(f'The movie {movie.title} was delete from your record', 'success')
        return redirect(url_for('movies'))
    flash(f'Can not delete the movie', 'success')
    return redirect(url_for('admin'))

#route for adding tickets
@app.route('/addticket/<int:id>', methods=['GET','POST'])
def addticket(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    form = Tickets(request.form)
    screenings = Screening.query.all()
    movieID = session['movie']
    screenID = session['screen']
    movie = Movies.query.get_or_404(movieID)
    screen = Screening.query.get_or_404(1)
    seatNo = session['seatNo']
    _price = float(movie.price)


    if id == 1:
        discount = 20
        _price = round(_price * 0.80, 2)
    elif id == 2:
        discount = 10
        _price = round(_price * 0.90, 2)
    elif id == 3:
        discount = 0
        _price = round(_price * 1.00, 2)
    elif id == 4:
        discount = 20
        _price = round(_price * 0.80, 2)

    if request.method == "POST":

        price = movie.price
        discount =discount
        seatNo = seatNo
        screen_id = screenID
        newticket = Ticket(price=price,discount=discount,seatNo=seatNo,screen_id=screen_id)

        db.session.add(newticket)
        session['ticket_id'] = newticket.id
        flash(f'The ticket with seat number {seatNo} was added in database','success')
        db.session.commit()
        return redirect(url_for('corfirmticket',id=newticket.id))
    return render_template('cinema/addticket.html',title='Add a Ticket',movie=movie,screen=screen,seatNo=seatNo, _price=_price)

#route for confirm ticket
@app.route('/corfirmticket/<int:id>', methods=['GET','POST'])
def corfirmticket(id):
    ticket = Ticket.query.get_or_404(id)

    return render_template('cinema/confirm.html',ticket=ticket)

#route for updating ticket
@app.route('/updateticket/<int:id>', methods=['GET','POST'])
def updateticket(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    form = Tickets(request.form)
    ticket = Ticket.query.get_or_404(id)

    if request.method =="POST" :

        ticket.price = form.price.data
        ticket.discount = form.discount.data
        ticket.seatNo = form.seatNo.data

        flash('The ticket was updated','success')
        db.session.commit()
        return redirect(url_for('admin'))

    form.price.data = ticket.price
    form.discount.data = ticket.discount
    form.seatNo.data = ticket.seatNo
    form1=form
    return render_template('cinema/addticket.html',form1=form1, form=form, title='Update Ticket',getticket=ticket)

#route for deleting ticket
@app.route('/deleteticket/<int:id>', methods=['POST'])
def deleteticket(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    ticket = Ticket.query.get_or_404(id)
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
