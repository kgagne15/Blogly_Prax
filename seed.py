from models import db, User, Post
from app import app

db.drop_all()
db.create_all()

jordan = User(first_name="Jordan", last_name="Gagne", image_url="https://doggowner.com/wp-content/uploads/2020/08/brown-dog-names-cover-image.jpg")
alyssa = User(first_name="Alyssa", last_name="Gagne", image_url="https://i.pinimg.com/originals/00/3b/f0/003bf01bd170cb73302bfd16c804ee81.jpg")
chase = User(first_name="Chase", last_name="Gagne", image_url="https://theferretsquad.com/wp-content/uploads/2019/09/What-to-Expect-with-a-Full-Grown-Ferret-Post-Image.jpg?189db0&189db0")

db.session.add_all([jordan, alyssa, chase])
db.session.commit()

post1 = Post(title="Post One", content="This is the first post ever!", user_id=1)
post2 = Post(title="Post Two", content="This is the second post ever!", user_id=2)

db.session.add_all([post1, post2])
db.session.commit()