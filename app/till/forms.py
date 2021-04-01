from wtforms import Form, SubmitField, IntegerField, SelectField


class PayWithCashForm(Form):
    n50 = IntegerField('Amount of £50 notes', default=0)
    n20 = IntegerField('Amount of £20 notes', default=0)
    n10 = IntegerField('Amount of £10 notes', default=0)
    n5 = IntegerField('Amount of £5 notes', default=0)
    c200 = IntegerField('Amount of £2 coins', default=0)
    c100 = IntegerField('Amount of £1 coins', default=0)
    c50 = IntegerField('Amount of 50p coins', default=0)
    c20 = IntegerField('Amount of 20p coins', default=0)
    c10 = IntegerField('Amount of 10p coins', default=0)
    c5 = IntegerField('Amount of 5p coins', default=0)
    c2 = IntegerField('Amount of 2p coins', default=0)
    c1 = IntegerField('Amount of 1p coins', default=0)
    submit = SubmitField('Pay')


class SelectScreeningForm(Form):
    screening = SelectField('Screening', choices=[], default=0)
    submit = SubmitField('Select')


class SelectTicketForm(Form):
    ticket = SelectField('Ticket', choices=[], default=0)
    discount = SelectField('Discount', choices=[('c', 'Child'), ('t', 'Teen'), ('a', 'Adult'), ('e', 'Elderly')])
    submit = SubmitField('Select')

