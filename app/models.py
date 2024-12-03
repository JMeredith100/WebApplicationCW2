from app import db

# This is the 'UserLikes' table. It creates a many-to-many relationship
# between the 'User' table and 'Posts' table.
user_likes = db.Table('user_likes',
                      db.Column('user_id', db.Integer, db.ForeignKey('db_users.id', ondelete="CASCADE")),
                      db.Column('post_id', db.Integer, db.ForeignKey('db_posts.id', ondelete="CASCADE"))
                      )

# These are the fields the User Table contains
class DBUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True)
    password = db.Column(db.String(50))
    dob = db.Column(db.Date, nullable=False)
    posts = db.relationship('DBPosts', backref='dbusers', lazy='dynamic')

    liked_posts = db.relationship('DBPosts', secondary=user_likes, backref='liked_by')

    def __repr__(self):
        return '{}{}'.format(self.id, self.username)


# These are the fields the Posts Table contains
class DBPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    content = db.Column(db.String(500))
    date = db.Column(db.Date, nullable=False)
    likes = db.Column(db.Integer, default=0)

    author_id = db.Column(db.Integer, db.ForeignKey('db_users.id'))

    def __repr__(self):
        return '{}{}{}'.format(self.id, self.title, self.likes)




