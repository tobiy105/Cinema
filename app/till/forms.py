from wtforms import Form, SubmitField, IntegerField

class PayWithCashForm(Form):
    n50 = IntegerField('Amount of £50 notes')
    n20 = IntegerField('Amount of £20 notes')
    n10 = IntegerField('Amount of £10 notes')
    n5 = IntegerField('Amount of £5 notes')
    c200 = IntegerField('Amount of £2 coins')
    c100 = IntegerField('Amount of £1 coins')
    c50 = IntegerField('Amount of 50p coins')
    c20 = IntegerField('Amount of 20p coins')
    c10 = IntegerField('Amount of 10p coins')
    c5 = IntegerField('Amount of 5p coins')
    c2 = IntegerField('Amount of 2p coins')
    c1 = IntegerField('Amount of 1p coins')
    submit = SubmitField('Pay')