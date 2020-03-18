import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json

#database config
database_path = os.environ['DATABASE_URL']

#For localhost
#database_path = 'postgresql://postgres:postgres@localhost:5432/capstone'
#database_name = 'capstone'

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

#Table representing many to many relationship
movie_actors = db.Table('movie_actors',
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('actor_id', Integer, ForeignKey('actors.id'))
    )

# Defines the movies class and all their methods
class Movie (db.Model):
    __tablename__='movies'
    #movie attributes
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release = Column(String)
    actors = db.relationship('Actor', secondary=movie_actors, backref=db.backref('movies', lazy=True))

    # Methohd to create a movie element. id is not required and not suggested, used for tests.
    def __init__(self, title, release, actors, id):
        self.title=title
        self.release=release
        self.actors = actors
        self.id = id

    #method to insert a movie to the database
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    #Method to patch a movie
    def update(self):
        db.session.commit()

    #Method to delete a movie
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    #Long format, returns the all the information of the movie including the lists of actors involved in the movie
    def format(self):
        actors = self.actors
        formatted = [element.formatshort() for element in actors]
        return {
            'id': self.id,
            'title': self.title,
            'release': self.release,
            'actors': formatted
        }

    #Short format, returns all the information of the movie except the actors involved.
    # Used by the format method in Actor class to avoid an infinite callback looping
    def formatshort(self):
        return {
            'id': self.id,
            'title': self.title,
            'release': self.release,
        }

# Define Actor Class in the db.
# Has the same methods as the Movie class but different attributes.
class Actor (db.Model):
    __tablename__='actors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)

    def __init__(self, name, gender, movies, age, id):
        self.name=name
        self.gender=gender
        self.age=age
        self.movies=movies
        self.id=id
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        movies = self.movies
        formatted = [element.formatshort() for element in movies]
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'movies': formatted
        }
    
    def formatshort(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
        }