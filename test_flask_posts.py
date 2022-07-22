from csv import unregister_dialect
from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class PostViewsTestCase(TestCase):
    def setUp(self):
        
        Post.query.delete()
        
        user = User(first_name="TestUser", last_name="Smith", image_url="https://mahanmedical.com/image/cache/product/test-1000x1000.jpg")
        post = Post(title='TestPost', content="This is a test post", user_id=1)

        db.session.add(user)
        db.session.commit()
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.user = user
        self.post = post
        self.post_id = post.id

    def tearDown(self):
        db.session.rollback()

    def test_posts_page(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestPost', html)
            self.assertIn(self.post.content, html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {"new-title": "TestPost2", "new-content": "Test Post 2", "user_id": 1}
            resp = client.post(f'/users/{self.user_id}/posts/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestPost2', html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(Post.query.get(self.post_id), None)