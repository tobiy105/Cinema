import decimal

from flask import render_template, request, redirect, url_for
from app import app, db
from .forms import PayWithCashForm, SelectScreeningForm, SelectTicketForm
from app.cinema.models import Screening, Ticket, Movies
from sqlalchemy import asc

from ..employee.models import EmployeeOrder


class Cash:
    def __init__(self, n50, n20, n10, n5, c200, c100, c50, c20, c10, c5, c2,
                 c1):
        self.n50 = n50
        self.n20 = n20
        self.n10 = n10
        self.n5 = n5
        self.c200 = c200
        self.c100 = c100
        self.c50 = c50
        self.c20 = c20
        self.c10 = c10
        self.c5 = c5
        self.c2 = c2
        self.c1 = c1

    def valueofcash(self):
        return self.n50 * 5000 + self.n20 * 2000 + self.n10 * 1000 + self.n5 * 500 + self.c200 * 200 + self.c100 * 100 \
               + self.c50 * 50 + self.c20 * 20 + self.c10 * 10 + self.c5 * 5 + self.c2 * 2 \
               + self.c1 * 1

    def to_string(self):
        return str(self.n50).join(',').join(str(self.n20)).join(',').join(str(self.n10)).join(',').join(str(self.n5)).\
            join(',').join(str(self.c200)).join(',').join(str(self.c100)).join(',').join(str(self.c50)).join(',').\
            join(str(self.c20)).join(',').join(str(self.c10)).join(',').join(str(self.c5)).join(',').\
            join(str(self.c2)).join(',').join(str(self.c1))

class Till:
    def __init__(self, cash):
        self.cash = cash

    def __removeCashFromTill(cash):
        return 0

    def changeCash(self, amount):
        toReturn = Cash(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        errorNotEnoughChange = 0
        while amount > 0 and errorNotEnoughChange == 0:
            if amount >= 5000 and self.cash.n50 > 0:
                toReturn.n50 = toReturn.n50 + 1
                amount = amount - 5000
            elif amount >= 2000 and self.cash.n20 > 0:
                toReturn.n20 = toReturn.n20 + 1
                amount = amount - 2000
            elif amount >= 1000 and self.cash.n10 > 0:
                toReturn.n10 = toReturn.n10 + 1
                amount = amount - 1000
            elif amount >= 500 and self.cash.n5 > 0:
                toReturn.n5 = toReturn.n5 + 1
                amount = amount - 500
            elif amount >= 200 and self.cash.c200 > 0:
                toReturn.c200 = toReturn.c200 + 1
                amount = amount - 200
            elif amount >= 100 and self.cash.c100 > 0:
                toReturn.c100 = toReturn.c100 + 1
                amount = amount - 100
            elif amount >= 50 and self.cash.c50 > 0:
                toReturn.c50 = toReturn.c50 + 1
                amount = amount - 50
            elif amount >= 20 and self.cash.c20 > 0:
                toReturn.c20 = toReturn.c20 + 1
                amount = amount - 20
            elif amount >= 10 and self.cash.c10 > 0:
                toReturn.c10 = toReturn.c10 + 1
                amount = amount - 10
            elif amount >= 5 and self.cash.c5 > 0:
                toReturn.c5 = toReturn.c5 + 1
                amount = amount - 5
            elif amount >= 2 and self.cash.c2 > 0:
                toReturn.c2 = toReturn.c2 + 1
                amount = amount - 2
            elif amount >= 1 and self.cash.c1 > 0:
                toReturn.c1 = toReturn.c1 + 1
                amount = amount - 1
            else:
                errorNotEnoughChange = errorNotEnoughChange + 1
        return errorNotEnoughChange, toReturn  # if errorNotEnoughChange = 1 then


    def cashPayment(self, amount, payment):
        cashCheck = cashPaymentCheck(amount, payment)
        if cashCheck == 0:
            return 0, Cash(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)#no change
        elif cashCheck < 0:
            return 1, Cash(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)#not enough
        elif cashCheck > 0:
            enoughChange, toReturn = self.changeCash(float(amount))
            if enoughChange == 0:
                return 0, toReturn
        return 2, Cash(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) #not enough change


@app.route('/till/screeningSelect', methods=['GET', 'POST'])
def selectFilm():
    form = SelectScreeningForm(request.form)
    form.screening.choices = [(screen.id, (screen.movie, screen.date)) for screen in Screening.query.order_by(asc(
        Screening.date), asc(Screening.startTime)).all()]
    if request.method == "POST":
        return redirect(url_for('ticketSelect', screen_id=form.screening.data))
    return render_template('till/screeningSelect.html', form=form)


@app.route('/till/ticketSelect/<screen_id>', methods=['GET', 'POST'])
def ticketSelect(screen_id):
    form = SelectTicketForm(request.form)
    screening = Screening.query.filter_by(id=screen_id).first()
    tickets = []
    for i in range(1, screening.seats):
        tickets.append((i, i))
    ticketsTaken = Ticket.query.filter_by(screen_id=screen_id).all()
    for ticket in ticketsTaken:
        if ticket.taken:
            tickets[ticket.seatNo] = (0, 0)
    form.ticket.choices = tickets
    if request.method == "POST":
        return createTicket(screening, form.ticket.data, form.discount.data)
    return render_template('till/ticketSelect.html', form=form)

def createTicket(screening, seat, discount):
    movie = Movies.query.filter_by(id=screening.movie_id).first()
    amount = movie.price * decimal.Decimal(discount)
    return redirect(url_for('showTill', amount=amount))




def cashPaymentCheck(amount, cash):
    value = cash.valueofcash()
    dif = float(amount) - value
    if dif > 0:
        return -1
    elif dif == 0:
        return 0
    elif dif < 0:
        return 1

def loadTill():
    till = open('app/till/till.csv', 'r')
    dataS = till.readline()
    data = dataS.split(',')
    cash = Cash(int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), int(data[6]), int(data[7]),
                        int(data[8]), int(data[9]), int( data[10]), int(data[11]))
    return cash

def saveToTill(cash):
    till = open('app/till/till.csv', 'w')
    till.write("10,10,10,10,10,10,10,10,10,10,10,10")