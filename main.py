from app import app,db
from Query.Queries import listPosts_resolver,getPost_resolver,listUsers_resolver,getPostFilters

from Mutation.Mutations import create_post_resolver,update_post_resolver,create_user_resolver

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML

from flask import request, jsonify

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies,get_jwt_identity,get_jwt

db.create_all()

jwt = JWTManager(app)

query = ObjectType("Query")

query.set_field("listPosts", listPosts_resolver)

query.set_field("getPost", getPost_resolver)

query.set_field("listUsers", listUsers_resolver)

query.set_field('getPostByFilters',getPostFilters)


mutation = ObjectType("Mutation")

mutation.set_field("createPost",create_post_resolver)

mutation.set_field("updatePost",update_post_resolver)

mutation.set_field("createUser",create_user_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query,mutation,snake_case_fallback_resolvers
)

@app.route("/graphql", methods=["GET"])
@jwt_required()
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
@jwt_required()
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code



@app.route("/login_without_cookies", methods=["POST"])
def login_without_cookies():
    # You can use the additional_claims argument to either add
    # custom claims or override default claims in the JWT.
    additional_claims = {"aud": "some_audience", "foo": "bar"}
    access_token = create_access_token("test", additional_claims=additional_claims)
    return jsonify(access_token=access_token)





@app.route("/logout_with_cookies", methods=["POST"])
def logout_with_cookies():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@app.route("/protected", methods=["GET", "POST"])
@jwt_required()
def protected():
    claims = get_jwt()
    return jsonify(foo=claims["foo"])
    # current_user = get_jwt_identity()
    # return jsonify(logged_in_as=current_user), 200









if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)