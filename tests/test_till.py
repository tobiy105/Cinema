import unittest

from app.till.views import *


class TestCase(unittest.TestCase):
    def test_value_of_cash(self):
        cash = Cash(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1) #one of each note/coin = 88.88 or 8888
        self.assertEqual(cash.valueofcash(), 8888)

    def test_to_string(self):
        cash = Cash(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        self.assertEqual(cash.to_string(), '1,1,1,1,1,1,1,1,1,1,1,1')

    def test_remove(self):
        cash = Cash(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        cash.remove(Cash(1,0,0,0,0,0,0,0,0,0,1,0))
        self.assertEqual(cash.to_string(), '0,1,1,1,1,1,1,1,1,1,0,1')

    def test_add(self):
        cash = Cash(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        cash.remove(Cash(1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0))
        self.assertEqual(cash.to_string(), '2,1,1,1,1,1,1,1,2,1,1,1')

    def test_from_string(self):
        cash = Cash(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        s = cash.to_string()
        self.assertEqual(cash.fromString(s, ',').to_string(), s)


    def test_change_cash(self):
        cash = Cash(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        till = Till(cash)
        amount = 500
        e, c = till.changeCash(amount)
        self.assertEqual(e, 0)
        tc = Cash(0,0,0,1,0,0,0,0,0,0,0,0)
        self.assertEqual(c.to_string(), tc.to_string())

    def test_cash_payment(self):
        till = Till(cash=Cash(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
        amount = 500
        payment = Cash(0,0,1,0,0,0,0,0,0,0,0,0)
        e, c = till.cashPayment(amount, payment)
        self.assertEqual(e, 0)
        t = Cash(0,0,0,1,0,0,0,0,0,0,0,0)
        self.assertEqual(c.to_string(), t.to_string())

    def test_cash_payment_check(self):
        cash = Cash(1,1,0,0,0,0,0,5,0,0,0,0) # 7100
        a = cashPaymentCheck(8000 , cash)
        b = cashPaymentCheck(7100 , cash)
        c = cashPaymentCheck(500 , cash)
        self.assertEqual(a, 1)
        self.assertEqual(b, 0)
        self.assertEqual(c, -1)
