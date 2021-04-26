import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, bcrypt, photos
from flask_wtf.file import FileField

from app.cinema.models import Addticket, Category
from app.admin.forms import RegistrationForm, LoginForm
from app.admin.models import User
import io

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        pass

    def test_category(self):
        client = app.test_client(self)
        response = client.post('/addcat', data=dict(name='test_c'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_product(self):

        client = app.test_client(self)
        response = client.post('/addticket', data=dict(name="food", price=2, discount=0, stock=10,
                               category="test_c", desc="help",  category_id=1), follow_redirects=True)
        print(response)
        self.assertEqual(response.status_code, 200)


    #
    # def test_product_no_cat(self):
    #     data1 = FileField('Users\tobiy\OneDrive\Pictures\food.png')
    #     data2 = FileField('Users\tobiy\OneDrive\Pictures\food2.png')
    #     data3 = FileField('Users\tobiy\OneDrive\Pictures\food3.png')
    #     client = app.test_client(self)
    #     response = client.post('/addproduct', data=dict(name="2food", price=2, discount=0, stock=10,
    #                            allergy="nuts", desc="help", category_id='', brand_id=1, image_1=data1,
    #                            image_2=data2, image_3=data3), follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_product_no_fields(self):
    #     client = app.test_client(self)
    #     response = client.post('/addproduct', data=dict(name="", price='', discount='', stock='',
    #                            allergy="", desc="", category_id='', brand_id='', image_1='',
    #                            image_2='', image_3=''), follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()