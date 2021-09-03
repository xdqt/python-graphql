from __main__ import mas

from model.Models import Post,User

from marshmallow_sqlalchemy.fields  import Nested


class PostSchema(mas.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True
        include_relationships = True
        
class UserSchema(mas.SQLAlchemyAutoSchema):
    posts = Nested(PostSchema, many=True)
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        


