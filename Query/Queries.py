from model.Models import Post,User
from ariadne import convert_kwargs_to_snake_case
from SQL.sql import Database
from Schemas.schemas import UserSchema,PostSchema
from sqlalchemy import and_

@convert_kwargs_to_snake_case
def getPost_resolver(obj, info, title,parent_id):
    try:
        # post = Database().query(Post,Post.id==id)
        post = Database().querybyPrimaryKey(Post,id)
        postschema = PostSchema()
        
        payload = {
            "success": True,
            "post": postschema.dump(post)
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": ["Post item matching {id} not found"]
        }
    return payload



@convert_kwargs_to_snake_case
def getPostFilters(obj, info, title,parent_id):
    try:
        # post = Database().query(Post,Post.id==id)
        post = Database().queryand(Post,and_(Post.title==title,Post.parent_id==parent_id))
        postschema = PostSchema(many=True)
        
        payload = {
            "success": True,
            "post": postschema.dump(post)
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": ["Post item matching {id} not found"]
        }
    return payload









def listUsers_resolver(obj, info):
    try:
        value = User.query.all()
        userschema = UserSchema(many=True)

        post = userschema.dump(value)
        print(post)
        payload = {
            "success": True,
            "post": post
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload




def listPosts_resolver(obj, info):
    try:
        postschema = PostSchema(many=True)
        
        value = Post.query.all()
        posts = postschema.dump(value)
        payload = {
            "success": True,
            "post": posts
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload