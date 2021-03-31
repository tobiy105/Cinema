from flask import render_template, request, redirect, url_for
from app import app
from .forms import PayWithCashForm




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

        # toReturn is garbage


    def cashPayment(self, amount, payment):
        cashCheck = cashPaymentCheck(amount, payment)
        if cashCheck == 0:
            return 0, Cash(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)#no change
        elif cashCheck < 0:
            return 1, Cash(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)#not enough
        elif cashCheck > 0:
            enoughChange, toReturn = self.changeCash(int(amount))
            if enoughChange == 0:
                return 0, toReturn
        return 2, Cash(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) #not enough change

@app.route('/till/ticketSelect')
def selectFilm():
    return render_template('till/ticketSelect.html')


@app.route('/till/<amount>', methods=['GET', 'POST'])
def showTill(amount):
    form = PayWithCashForm(request.form)
    if request.method == "POST":
        payment = Cash(form.n50.data, form.n20.data, form.n10.data, form.n5.data, form.c200.data, form.c100.data, form.c50.data, form.c20.data, form.c10.data,form.c5.data, form.c2.data, form.c1.data)
        cash = Cash(10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10)
        till = Till(cash)
        flag, change = till.cashPayment(amount, payment)
        if flag == 0:  #success
            return redirect(url_for ('admin')) #should go to payment confimed
        elif flag == 1:  #error not enough money
            return render_template('till/till.html', form=form, flag=1, amount=amount)
        elif flag == 2:  #error not enough change
            return render_template('till/till.html', form=form, flag=2, amount=amount)
    return render_template('till/till.html', form=form, flag=0, amount=amount)

def cashPaymentCheck(amount, cash):
    value = cash.valueofcash()
    dif = int(amount) - value
    if dif > 0:
        return -1
    elif dif == 0:
        return 0
    elif dif < 0:
        return 1