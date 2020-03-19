# Full Stack Developer Nanodegree Capstone Project

This project consist of a platform used by Casting Agencies to connect a movie project with a group of actors. In this way it is possible to pick one or more actors
in a list of available actors and relate them with one or more movies from a list of upcomming movies. This project motivation is to show the developed skills during
the Full Stack Developer Nanodegree. The api is not full accesible by the users, access to the information is role-based. The implemented roles and permissions are:

  - Casting assistant (refered also as Assistant): Can view the available actors and movies.

  - Casting Director (refered also as director): Assistant permissions + Can create, edit and delete actors.

  - Executive Producer (refered also as producer): Director permissions + Can create, edit and delete movies.

More information about role access is available in the auth.py section

## Main Files

### models.py

File containing the database configuration sattings (Database created using PSQL) and the desired models for Actor and movies.

### auth.py 

Decorator used for RBAC. All the requests must contain a token that identifies the user with one of the roles and the corresponding permissions. The token are generated and validated
by a 3rd party, in this case AUTH0 (see [auth0.com](https://auth0.com)). This decorator is used for checking if a Token is valid and if the user has permission to access the requested endpoint. The roles are assigned manually by the administrator in Auth0. For login or creating a new user there is the [login/register url](https://eacg.auth0.com/authorize?audience=capstone%20proyect&response_type=token&client_id=CRsK5ru52FuqOfzU59bd5guQYd2Rmp7U&redirect_uri=https://127.0.0.1:5000/login-results). Currently there is no url to handle postlogin interactions, so the user is redirected to a localhost adress. Token must be taken from the redirected url and added to the requests, currently token lifespan is 1 day for debug issues. After registering a new user, it is necessary to request the administrator for assigning a new role. Some test Tokens are included but can be expired.

### app.py

Main file where all the endpoints and error handlers of the api are found. Is the file that must be runned in order to start the server.

### test_app.py

A file containing a set of 26 unittest tests to guarantee the correct operation of all the end points and correct interactions witth the roles and permissions. The test must run without mistakes. The same series of test are included in a postman collection which can also be used by the user. Test_app.py is directly linked with the aplication, so it can be executed from any container or localhost. In the case of postman the url must be specified in each request. Default url in postman corresponds to the deployed hosting url (see section Hosting).

## Running locally

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Postgres SQL

Follow the instructions in [PSQL webpage](https://www.postgresql.org/) to install postgres SQL. 

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

### Modifying the app

- A PSQL database must be manually created before runnning the app.
- Inside LocalHost at the beginning of the "models.py" file variables "database_path" and "database_name" must be correctly updated to the corresponding local database.
- Auth0 host can be changed by modifying the variables "AUTH0_DOMAIN", "ALGORITHMS" and "API_AUDIENCE", to the corresponding of your auth0 applicaiton. Roles and permissions in auth0 must be created. Permissions declaration can be found inside the "app.py" at the @requires_auth decorator calls. 
- In "app.py" file change the host where the app run at the end of the file.


### Running the server

From within the project directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python app.py
```

## Hosting

Api is hosted online using heroku. 
api link: https://eacg-capstone.herokuapp.com/
git link:  https://git.heroku.com/eacg-capstone.git

## End points


GET '/movies'
GET '/actors'
POST '/movies'
POST '/actors'
PATCH '/movies/<id>'
PATCH '/actors/<id>'
DELETE '/movies/<id>'
DELETE '/actors/<id>'


*NOTE when refering to 'all existing elements' in case of the existing more than 10 actors or movies, it will be a pagination grouping that will just return a max of 10 elements per page. Get requests can accept a page parameter for this pagination. 

GET '/movies'
- Fetches a dictionary of movies in which each movie id, release date, title and actors are included
- Request Arguments: None
- Returns: A success message and a vector containing all the movies information. 

sample output:

```bash
{
  "movies": [
    {
      "actors": [],
      "id": 1,
      "release": "2020/03/05",
      "title": "Star Wars"
    }
  ],
  "success": true
}
```

GET '/actors'
- Fetches a dictionary of actors in which each actor's id, name, gender, age and movies are included
- Request Arguments: None
- Returns: A success message and a vector containing all the actors information. 

sample output:
```bash
{
  "actors": [
    {
      "age": 42,
      "gender": "male",
      "id": 1,
      "movies": [],
      "name": "Brad Pitt"
    }
  ],
  "success": true
}
```

POST '/movies'
- Request for adding a new movie to the database
- Request arguments: A dictionary containing the information about the movie. The actors must be included as a vector including the actors ids.
- Returns: A success message and the information of the recently created movie.

Sample input:
```bash
{
	"title":"Star Wars",
	"release":"2020/03/05",
	"actors":[],
	"id":1
}
```
Sample output:
```bash
  {
  "movie": {
    "actors": [],
    "id": 1,
    "release": "2020/03/05",
    "title": "Star Wars"
  },
  "success": true
}
```

POST '/actors'
- Request for adding a new actor to the database
- Request arguments: A dictionary containing the information about the actor. The movies must be included as a vector including the movies ids.
- Returns: A success message and the information of the recently created actor.

Sample input:
```bash
{
	"name":"Brad Pitt",
	"gender":"male",
	"age":42,
	"movies":[],
	"id":1
}
```
Sample output:
```bash
{
  "actor": {
    "age": 42,
    "gender": "male",
    "id": 1,
    "movies": [],
    "name": "Brad Pitt"
  },
  "success": true
}
```

PATCH '/actors/<id>'
- Request for editing an existing actor in the database
- Request arguments: Id of the actor to modify. A dictionary containing the information about the actor to change. The movies must be included as a vector including the movies ids.
- Returns: A success message and the information of the recently modified actor.

Sample input:
```bash
{
	"name":"Johnny Depp"
}
```
Sample output:
```bash
{
  "actor": {
    "age": 42,
    "gender": "male",
    "id": 1,
    "movies": [],
    "name": "Johnny Depp"
  },
  "success": true
}
```

PATCH '/movies/<id>'
- Request for editing an existing movie in the database
- Request arguments: Id of the movie to modify. A dictionary containing the information about the movie to change. The actors must be included as a vector including the actors ids.
- Returns: A success message and the information of the recently modified movie.

Sample input:
```bash
{
	"title":"Lord of the Rings"
}
```
Sample output:
```bash
{
  "movie": {
    "actors": [],
    "id": 1,
    "release": "2020/03/05",
    "title": "Lord of the Rings"
  },
  "success": true
}
```

DELETE '/actors/<id>'
- Deletes an actor fromm the database
- Request Arguments: Id of the actor to delete
- Returns: A success message and the id of the deleted actor

sample output:
```bash
{
  "deleted": "1",
  "success": true
}
```

DELETE '/movies/<id>'
- Deletes a movie fromm the database
- Request Arguments: Id of the movie to delete
- Returns: A success message and the id of the deleted movie

sample output:
```bash
{
  "deleted": "1",
  "success": true
}
```

## Contact
api developed by Edwin Canal (edwinacg96@gmail.com). Project accepting contributions.  