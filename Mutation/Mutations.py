from model.Models import Post, User

from datetime import date
from ariadne import convert_kwargs_to_snake_case

from SQL.sql import Database

from Schemas.schemas import UserSchema

@convert_kwargs_to_snake_case
def create_post_resolver(obj, info, title, description,parent_id):
    try:
        today = date.today()
        post = Post(
            title=title, description=description, created_at=today.strftime("%b-%d-%Y"),parent_id=parent_id
        )
        Database().insert(post)

        payload = {
            "success": True,
            "post": post.to_dict()
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }
    return payload




@convert_kwargs_to_snake_case
def update_post_resolver(obj, info, id, title, description):
    try:
        post = Post.query.get(id)
        if post:
            post.title = title
            post.description = description
        Database().insert(post)
        payload = {
            "success": True,
            "post": post.to_dict()
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": ["item matching id {id} not found"]
        }
    return payload





@convert_kwargs_to_snake_case
def create_user_resolver(obj, info, input):
    try:
        userschema = UserSchema(many=True)
        print(input)
        uservalue = userschema.load(input)
        
        Database().insertmany(uservalue)
        payload = {
            "success": True,
            "post": input
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": ["item matching id {id} not found"]
        }
    return payload