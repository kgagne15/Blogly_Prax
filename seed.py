from models import db, User, Post, Tag, PostTag
from app import app

db.drop_all()
db.create_all()

jordan = User(first_name="Jordan", last_name="Gagne", image_url="https://doggowner.com/wp-content/uploads/2020/08/brown-dog-names-cover-image.jpg")
alyssa = User(first_name="Alyssa", last_name="Gagne", image_url="https://i.pinimg.com/originals/00/3b/f0/003bf01bd170cb73302bfd16c804ee81.jpg")
chase = User(first_name="Chase", last_name="Gagne", image_url="https://theferretsquad.com/wp-content/uploads/2019/09/What-to-Expect-with-a-Full-Grown-Ferret-Post-Image.jpg?189db0&189db0")

db.session.add_all([jordan, alyssa, chase])
db.session.commit()

post1 = Post(title="Blue Jays", content="The Blue Jays are the best team ever", user_id=1)
post2 = Post(title="Renaissance", content="Can't wait to hear Beyonce's new album!", user_id=2)
post3 = Post(title="New Record", content="The Blue Jays beat the Red Sox 28-5!!!", user_id=1)

db.session.add_all([post1, post2, post3])
db.session.commit()

tag1 = Tag(name="Sports")
tag2 = Tag(name="Baseball")
tag3 = Tag(name="Music")
tag4 = Tag(name="Art")

db.session.add_all([tag1, tag2, tag3, tag4])
db.session.commit()

post_tag1 = PostTag(post_id=1, tag_id=1)
post_tag2 = PostTag(post_id=2, tag_id=3)
post_tag3 = PostTag(post_id=2, tag_id=4)
post_tag4 = PostTag(post_id=3, tag_id=1)
post_tag5 = PostTag(post_id=3, tag_id=2)

db.session.add_all([post_tag1, post_tag2, post_tag3, post_tag4, post_tag5])
db.session.commit()