from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add sample user."""

        User.query.delete()
        user = User(first_name="TestUser", last_name="Smith", image_url="https://mahanmedical.com/image/cache/product/test-1000x1000.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user
    
    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()
    
    def test_show_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser', html)
        
    def test_details_page(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser', html)
            self.assertIn(self.user.last_name, html)
    
    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestUser2", "last_name": "Johnson", "image_url": "https://oskoproduction.com/wp-content/uploads/2017/12/test_img.png"}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUser2", html)
    
    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(User.query.get(self.user_id), None)
