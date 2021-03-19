from flask import Flask, request, render_template, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cupc4k3s-'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/')
def show_cupcake_list():
    "Render a page with a list of all cupcakes and a form to add another cupcake."
    return render_template('index.html')

@app.route('/api/cupcakes')
def get_all_cupcakes():
    "Return JSON of a list of dictionaries representing all cupcakes in the database"
    cupcakes = Cupcake.query.all()
    json_list = [ cupcake.serialize() for cupcake in cupcakes ]
    return jsonify(cupcakes=json_list)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_single_cupcake(cupcake_id):
    "Return JSON describing a single cupcake's properties. 404 if cupcake ID doesn't exist in the database."
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def add_cupcake():
    """
    Add a cupcake to the database based on the JSON data passed to the route.
    """
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']

    new_cupcake = Cupcake.add(flavor=flavor, size=size, rating=rating, image=image)
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def edit_cupcake(cupcake_id):
    """
    Edit properties of the cupcake at the URL ID with the JSON properties passed in.
    404 if the cupcake does not exist.
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """
    Delete the cupcake at the URL ID from the database.
    404 if the cupcake does not exist.
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")