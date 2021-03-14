from flask import render_template
from app import app
from .forms import PayWithCashForm

@app.route('/till', methods=['GET', 'POST'])
def showTill():
    form = PayWithCashForm()
    return render_template('till/till.html', form=form)

