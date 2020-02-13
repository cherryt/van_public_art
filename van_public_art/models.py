from van_public_art import db


class Artist(db.Model):
    __tablename__ = "artist"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    biography = db.Column(db.String())

    def __init__(self, id, first_name, last_name, biography):
        self.first_name = first_name
        self.last_name = last_name
        self.biography = biography


class Artwork(db.Model):
    __tablename__ = "artwork"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    address = db.Column(db.String())
    neighbourhood = db.Column(db.String())
    description = db.Column(db.String())

    def __init__(self, id, title, address, neighbourhood, description):
        self.id = id
        self.title = title
        self.address = address
        self.neighbourhood = neighbourhood
        self.description = description

    def get_neighbourhoods():
        return (
            db.session.query(Artwork.neighbourhood)
            .group_by(Artwork.neighbourhood)
            .having(Artwork.neighbourhood is not None)
            .order_by(Artwork.neighbourhood.asc())
        )
