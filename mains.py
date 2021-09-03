from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML

from flask import request, jsonify


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@127.0.0.1:5432/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
mas = Marshmallow(app)


from Query.Queries import listPosts_resolver,getPost_resolver,listUsers_resolver

from Mutation.Mutations import create_post_resolver,update_post_resolver

db.create_all()


query = ObjectType("Query")

query.set_field("listPosts", listPosts_resolver)

query.set_field("getPost", getPost_resolver)

query.set_field("listUsers", listUsers_resolver)


mutation = ObjectType("Mutation")

mutation.set_field("createPost",create_post_resolver)

mutation.set_field("updatePost",update_post_resolver)


type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query,mutation,snake_case_fallback_resolvers
)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)