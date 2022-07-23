from csv import unregister_dialect
from unittest import TestCase
from app import app
from models import db, User, Post, Tag, PostTag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class PostViewsTestCase(TestCase):
    def setUp(self):
        Tag.query.delete()

        user = User(first_name="TestUser", last_name="Smith", image_url="https://mahanmedical.com/image/cache/product/test-1000x1000.jpg")
        post = Post(title='TestPost', content="This is a test post", user_id=1)
        tag = Tag(name="TestTag")

        db.session.add(user)
        db.session.commit()
        db.session.add(post)
        db.session.commit()
        db.session.add(tag)
        db.session.commit()


        self.user_id = user.id
        self.user = user
        self.post = post
        self.post_id = post.id
        self.tag = tag
        self.tag_id = tag.id

    def tearDown(self):
        db.session.rollback()

    def test_tags_page(self):
        with app.test_client() as client:
            resp = client.get("/tags")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestTag', html)
            

    def test_add_tag(self):
        with app.test_client() as client:
            d = {"new-tag": "TestTag2"}
            resp = client.post('/tags/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestTag2', html)
    
    def test_delete_tag(self):
        with app.test_client() as client:
            resp = client.post(f'/tags/{self.tag_id}/delete', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(Tag.query.get(self.tag_id), None)