from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class Cupcake(db.Model):
    """
    Class to define a model for Cupcakes in our database.
    """

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    flavor = db.Column(
        db.Text,
        nullable = False
    )

    size = db.Column(
        db.Text,
        nullable = False
    )

    rating = db.Column(
        db.Float,
        nullable = False
    )

    image = db.Column(
        db.Text,
        nullable = False,
        default = 'https://tinyurl.com/demo-cupcake'
    )

    def serialize(self):
        """
        Return a dictionary with all relevant properties for a cupcake instance.
        """
        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image': self.image
        }

    @classmethod
    def add(cls, flavor, size, rating, image):
        """
        Create and commit a new instance of a cupcake. 
        Return the cupcake after it's committed.
        """
        new_cupcake = cls(flavor=flavor, size=size, rating=rating)
        if image:
            new_cupcake.image = image
        db.session.add(new_cupcake)
        db.session.commit()

        return new_cupcake