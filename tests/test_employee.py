import unittest
from app import app, db, bcrypt

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        pass

    def test_register_employee(self):
        client = app.test_client(self)
        response = client.post('/employee/register', data = dict(name='test_cus', username='Employee',
                               email='custumer@gmail.com', password='pass888'),
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_employee(self):
        hash_password = bcrypt.generate_password_hash('pass888')
        client = app.test_client(self)
        response = client.post('/employee/login', data = dict(email='custumer@gmail.com', password=hash_password), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_employee_no_email(self):
        hash_password = bcrypt.generate_password_hash('pass888')
        client = app.test_client(self)
        response = client.post('/employee/login', data = dict(email='', password=hash_password), follow_redirects=False)
        self.assertEqual(response.status_code, 200)

    def test_login_employee_no_password(self):
        hash_password = bcrypt.generate_password_hash('pass888')
        client = app.test_client(self)
        response = client.post('/employee/login', data = dict(email='custumer@gmail.com', password=''), follow_redirects=False)
        self.assertEqual(response.status_code, 200)

    def test_login_employee_no_fields(self):
        hash_password = bcrypt.generate_password_hash('pass888')
        client = app.test_client(self)
        response = client.post('/employee/login', data = dict(email='', password=''), follow_redirects=False)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()