import unittest
from app import app, db

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        pass

    #test that the page loads correctly
    def test_viewMovieDetails_loads(self):
        tester = app.test_client(self)
        response = tester.get('/customer/viewMovieDetails', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    #test that the returned information is correct
    def test_viewMovieDetails(self):
        tester = app.test_client(self)
        response = tester.post('/customer/viewMovieDetails', data = dict(title="Star Wars A New Hope"), follow_redirects=True)
        self.assertIn(b'Star Wars: Episode IV - A New Hope', response.data)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()