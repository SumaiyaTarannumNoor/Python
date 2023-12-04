from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class ArtModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Art(name = {self.name}, views = {self.views}, price ={self.price})"


art_put_args = reqparse.RequestParser()
art_put_args.add_argument("name", type=str, help="Name of the artwork.")
art_put_args.add_argument("views", type=int, help="Views of the artwork.")
art_put_args.add_argument("price", type=int, help="Price of the artwork.")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'price': fields.Integer
}

class Art(Resource):
    @marshal_with(resource_fields)
    def get(self, art_id):
        result = ArtModel.query.filter_by(id=art_id).first()
        if not result:
            abort(404, message="Artwork with this ID doesn't exists. Try another...")
        return result

    @marshal_with(resource_fields)
    def put(self, art_id):
        args = art_put_args.parse_args()
        result = ArtModel.query.filter_by(id=art_id).first()
        if result:
            abort(409, message="Art ID exists.")
        art = ArtModel(id=art_id, name = args['name'], views = args['views'], price = args['price'])
        db.session.add(art)
        db.session.commit()
        return art, 201
    
    @marshal_with(resource_fields)
    def delete(self, art_id):
        args = art_put_args.parse_args()
        result = ArtModel.query.filter_by(id=art_id).first()
        if not result:
            abort(404, message="Artwork with this ID doesn't exists. Try another...")
        db.session.delete()
        db.session.commit()
        return '', 204


api.add_resource(Art, "/art/<int:art_id>")

if __name__ == "__main__":
    app.run(debug=True)