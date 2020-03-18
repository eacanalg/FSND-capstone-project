import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import setup_db, Movie, Actor, db
from auth import AuthError, requires_auth

#Paginate function used for only returning 10 elements
PAGINATE_SIZE = 10
def paginate(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * PAGINATE_SIZE
  end = start + PAGINATE_SIZE

  current = [element.format() for element in selection]
  current_paginated = current[start:end]

  return current_paginated

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app)
  migrate = Migrate(app,db)
  
  # GET Methods
  # returns a success message and a list of desired class.
  # Can take a page argument for pagination, 1  by default.
  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies(jwt):
    movies = Movie.query.order_by(Movie.id).all()
    current = paginate(request, movies)
    return jsonify({
      'success': True,
      'movies': current
    })

  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors(jwt):
    actors = Actor.query.order_by(Actor.id).all()
    current = paginate(request, actors)
    return jsonify({
      'success': True,
      'actors': current
    })
  
  # DELETE Methods
  # takes an id and returns a success message and the element id

  @app.route('/movies/<movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(jwt, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)
    try:
        movie.delete()
        return jsonify({
            'success': True,
            'deleted': movie_id
        })
    except:
        abort(422)
  
  @app.route('/actors/<actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(jwt, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)
    try:
        actor.delete()
        return jsonify({
            'success': True,
            'deleted': actor_id
        })
    except:
        abort(422)

  #POST Methods
  # return a succes message and the information about de new element
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_actor(jwt):
    body = request.get_json()
    name = body.get('name', None)
    gender = body.get('gender', None)
    age = body.get('age', None)
    id = body.get('id', None)
    movies = body.get('movies', [])
    models = [Movie.query.get(element) for element in movies]
    try:
        newActor = Actor(name=name, gender=gender, age=age, movies=models, id=id)
        newActor.insert()
        return jsonify({
            'success': True,
            'actor': newActor.format()
        })
    except:
        abort(422)

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def add_movie(jwt):
    body = request.get_json()
    title = body.get('title', None)
    release = body.get('release', None)
    actors = body.get('actors', [])
    id = body.get('id', None)
    models = [Actor.query.get(element) for element in actors]
    try:
        newMovie = Movie(title=title, release=release, actors=models, id=id)
        newMovie.insert()
        return jsonify({
            'success': True,
            'movie': newMovie.format()
        })
    except:
        abort(422)

  # PATCH Methods
  # Return a success message and updated element

  @app.route('/movies/<id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def patch_movie(jwt, id):
    body = request.get_json()
    title = body.get('title', None)
    release = body.get('release', None)
    actors = body.get('actors', None)
    movie = Movie.query.filter(Movie.id == id).one_or_none()
    if movie is None:
      abort(404)
    if not title is None:
      movie.title = title
    if not release is None:
      movie.release = release
    if not actors is None:
      models = [Actor.query.get(element) for element in actors]
      movie.actors = models
    try:
        movie.update()
        return jsonify({
            'success': True,
            'movie': movie.format()
        })
    except:
        abort(422)

  @app.route('/actors/<id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def patch_actor(jwt, id):
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)
    movies = body.get('movies', None)

    actor = Actor.query.filter(Actor.id == id).one_or_none()
    if actor is None:
      abort(404)
    if not name is None:
      actor.name = name
    if not age is None:
      actor.age = age
    if not gender is None:
      actor.gender = gender
    if not movies is None:
      models = [Movie.query.get(element) for element in movies]
      actor.movies = models
    try:
        actor.update()
        return jsonify({
            'success': True,
            'actor': actor.format()
        })
    except:
        abort(422)

  # Error handlers.s
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404
                    
  @app.errorhandler(AuthError)
  def unauthorized(error):
    return jsonify({
        "success": False, 
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400
  
  @app.errorhandler(500)
  def server_error():
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "server error"
    })

  return app

APP = create_app()



if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

    #For local host
    #APP.run(debug=True)