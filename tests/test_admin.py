import unittest
from app import app, db, bcrypt
from app.admin.views import oneWeekLess
import datetime

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        pass

    def test_register_message(self):
        hash_password = bcrypt.generate_password_hash('pass')
        client = app.test_client(self)
        response = client.post('/register', data = dict(name='test', username='Tests',
                               email='email2@gmail.com', password=hash_password), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        hash_password = bcrypt.generate_password_hash('pass')
        client = app.test_client(self)
        response = client.post('/login', data = dict(email='email2@gmail.com', password=hash_password), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_no_email(self):
        hash_password = bcrypt.generate_password_hash('pass')
        client = app.test_client(self)
        response = client.post('/login', data = dict(email='', password=hash_password), follow_redirects=False)
        self.assertEqual(response.status_code, 200)

    def test_login_no_password(self):
        hash_password = bcrypt.generate_password_hash('pass')
        client = app.test_client(self)
        response = client.post('/login', data = dict(email='email2@gmail.com', password=''), follow_redirects=False)
        self.assertEqual(response.status_code, 200)

    def test_login_no_fields(self):
        hash_password = bcrypt.generate_password_hash('pass')
        client = app.test_client(self)
        response = client.post('/login', data = dict(email='', password=''), follow_redirects=False)
        self.assertEqual(response.status_code, 200)

    def test_one_week_less(self):
        maxDate = datetime.date(2021,6,14)
        current1 = datetime.date(2021,6,12)
        current2 = datetime.date(2021,6,15)
        current3 = datetime.date(2021,6,7)
        test1 = oneWeekLess(maxDate,current1)
        test2 = oneWeekLess(maxDate,current2)
        test3 = oneWeekLess(maxDate,current3)
        self.assertEqual(test1, True)
        self.assertEqual(test2, False)
        self.assertEqual(test3, False)


    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()