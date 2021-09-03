from __main__ import app,db



        
        
class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    posts = db.relationship('Post',uselist=True)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.title,
            "post": [item.to_dict() for item in self.posts],
        }
        
        
class Post(db.Model):
    __tablename__="post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": str(self.created_at.strftime('%d-%m-%Y'))
        }
        