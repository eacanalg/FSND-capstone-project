import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor, db, database_name, database_path

# Define the Tokens used for  the tests. This tokens must be renewed each 24 hours according to Auth0 api config.
producerToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56azJRak0yTkRjeE56Z3pOVGMxTlVWQ09VWXhOamt5TkVVeVFVWkVNVGsyTnpRMU1qQTVRdyJ9.eyJpc3MiOiJodHRwczovL2VhY2cuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNjFiN2VmMjllMWUwMGQzZTc3OTI2YiIsImF1ZCI6ImNhcHN0b25lIHByb3llY3QiLCJpYXQiOjE1ODQ1MDA1MTMsImV4cCI6MTU4NDU4NjkxMywiYXpwIjoiQ1JzSzVydTUyRnVxT2Z6VTU5YmQ1Z3VRWWQyUm1wN1UiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.cV0uHwHK2ZA41dZHb2gLjyCT7kEuMv7G1LpBI9DGPudFbj6rx_uSSfeaMPzQd-99lPvXjpPdhAnkxyyE3LygSdNmnuO4S5oBrOPoilI6285RSo7fCOBvaGaXTqdnlshuAFu4gPXMtA7xFyb__onrJS51t1t66vTpN7laZxFOTXIVHFbgvL8SQaxESU0BEHDBTadHhuPQry-HE8QaJXZcF8WRwsRhnjVKZis9659AFcgxavR5r_XqHtAIMShHckEsyDuwg6dR7HszAU5XiHhieP9vQxOJWANpU-EGMZNBxRKZHsROnbVGTYyKKWnm1TwlFk7O2SumdwePDYD0dbYtYg'
directorToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56azJRak0yTkRjeE56Z3pOVGMxTlVWQ09VWXhOamt5TkVVeVFVWkVNVGsyTnpRMU1qQTVRdyJ9.eyJpc3MiOiJodHRwczovL2VhY2cuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNjFiODNmMjViMmU2MGQzYjc3ZDRmOSIsImF1ZCI6ImNhcHN0b25lIHByb3llY3QiLCJpYXQiOjE1ODQ1MDA1NjUsImV4cCI6MTU4NDU4Njk2NSwiYXpwIjoiQ1JzSzVydTUyRnVxT2Z6VTU5YmQ1Z3VRWWQyUm1wN1UiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBvc3Q6YWN0b3JzIl19.xmSc5W_QSAM9x5mN7pefyCu9g-VhqMz273sUCq0jbDTpD05ByDHdi4gHj9AHckxL5tqshTxeDf4PcTy4hq_XEVUKlgtejMyymBuoEHWzTfl7IzvsMIQEqNLrJ6mk-4X4aSReZU4flMm9y31rXZULhloc_6YC7U61n002v_x81QOzoGrYZnyaZT86ohXlld9C-mSszOM7WLDXmGUTbCH-K_bDLoG1fCPF80MZ5Fr5zDBpZPUGGYnyBt-jGR8qUK9yIw3OFgoijv8Ajz839PShsmkKTdFGAdqhw2SJBGjksBwSSapec2cLgC2OMkIL1QJsYR3hBZYDtIYDk2tNHw_q1g'
assistantToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56azJRak0yTkRjeE56Z3pOVGMxTlVWQ09VWXhOamt5TkVVeVFVWkVNVGsyTnpRMU1qQTVRdyJ9.eyJpc3MiOiJodHRwczovL2VhY2cuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNzA0MjIyMTI2ZDZhMGMzMTM2OGI4NyIsImF1ZCI6ImNhcHN0b25lIHByb3llY3QiLCJpYXQiOjE1ODQ1MDA2MjQsImV4cCI6MTU4NDU4NzAyNCwiYXpwIjoiQ1JzSzVydTUyRnVxT2Z6VTU5YmQ1Z3VRWWQyUm1wN1UiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.m5Ru9I1YAGE-zkrZkcvtv_2zBlHKWrVuL7Tm8d5Qo4XCFM7T3xxpoB66nP3kJpgcU_ftvZBRvuIONUAQ-S4XBEqOXWjc_K2VYAcLD1eo8FkMSzjoFqP8eKW5eUXQzeehmTcPEn6LLDp10iZUwB8gArUYTCmoUW-pev3S7brUav92DrUVvnGtNRot-IzQD7WZQ9oBRDyDe_Ke1vGTs7W8Hxc86B3kcqMMEsa9o96TH1ZLH5iz94IJjd8xIwczDIm68Deqxstb-ZBkA45jMk83CdMZxFQWAYIAS8efHqgPqzWIGfpZxHyEntlMFVdJDM9gQ4nQTgwdKR7wNl99uwZUEg'

class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = database_name
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        #Creates a movie object to be inserted in POST endpoints
        #Id is not necessary and suggested to not specify.
        #In this case ID is used for keeping track for future PATCH and DELETE over the same object
        self.new_movie ={
            "title":"Star Wars",
            "release":"2020/03/05",
            "actors":[],
            "id":1
        }
        #Creates an actor object to be inserted in POST endpoints
        #Id is not necessary and suggested to not specify.
        #In this case ID is used for keeping track for future PATCH and DELETE over the same object
        self.new_actor = {
            "name":"Brad Pitt",
            "gender":"male",
            "age":42,
            "movies":[],
            "id":1
        }

        #Creates the headers used for each one of the roles request's
        self.producerHeader={'Content-Type': 'application/json', 'authorization': f'Bearer {producerToken}'}
        self.directorHeader={'Content-Type': 'application/json', 'authorization': f'Bearer {directorToken}'}
        self.assistantHeader={'Content-Type': 'application/json', 'authorization': f'Bearer {assistantToken}'}

    def tearDown(self):
        """Executed after reach test"""
        pass
    #Producer tests
    #All the following tests use the prodocer autorization token.

    #test endpoint to get all the existing actors
    def test_producer_getactors(self):
        res = self.client().get('/actors', headers=self.producerHeader)
        data=json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    #test endpoint to get all existing movies.
    def test_producer_getmovies(self):
        res = self.client().get('/movies', headers=self.producerHeader)
        data=json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
    
    # Test the post, patch and delete endpoints for actors
    # This are joined because they Patch and Delete work on the object created by the post request.
    # This test is dessigned to run regardless of the db state as long as no item with id 1 is created manually.
    # As psql doesn't reuse deleted ids, id one is expected only to be used by tests.
    def test_producer_ppdactor(self):
        #Post
        res = self.client().post('/actors', headers=self.producerHeader, json=self.new_actor)
        data=json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        #Patch
        res = self.client().patch('/actors/1', headers=self.producerHeader, json={"name":"new name"})
        data=json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        #Delete
        res = self.client().delete('/actors/1', headers=self.producerHeader)
        data=json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    # Test post, patch and delete endpoints for movies in the same way as test_producer_ppdactor.
    def test_producer_ppdmovie(self):
        #Post
        res = self.client().post('/movies', headers=self.producerHeader, json=self.new_movie)
        data=json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        #Patch
        res = self.client().patch('/movies/1', headers=self.producerHeader, json={"title":"new title"})
        data=json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        #Delte
        res = self.client().delete('/movies/1', headers=self.producerHeader)
        data=json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)


    # Director Tests
    # Same tests as in Producer but with the director Token.
    def test_director_getactors(self):
        res = self.client().get('/actors', headers=self.directorHeader)
        data=json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_director_getmovies(self):
        res = self.client().get('/movies', headers=self.directorHeader)
        data=json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
    
    # As  post, patch and delete request for movies are expected to be denied by RBAC the tests can be runned individually.
    def test_director_postmovie(self):
        res = self.client().post('/movies', headers=self.directorHeader, json=self.new_movie)
        data=json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)
    
    def test_director_patchmovie(self):
        res = self.client().patch('/movies/1', headers=self.directorHeader, json={"title":'new title'})
        data=json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)

    def test_director_deletemovie(self):
        res = self.client().delete('/movies/1', headers=self.directorHeader)
        data=json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)

    def test_director_ppdactor(self):
        #Post
        res = self.client().post('/actors', headers=self.directorHeader, json=self.new_actor)
        data=json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        #Patch
        res = self.client().patch('/actors/1', headers=self.directorHeader, json={"name":"new name"})
        data=json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        #Delete
        res = self.client().delete('/actors/1', headers=self.directorHeader)
        data=json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
    


    #Assistant tests
    #tests all point with the assistant permissions. Here all tests  can be runned individually.
    def test_assistant_getactors(self):
        res = self.client().get('/actors', headers=self.assistantHeader)
        data=json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_assistant_getmovies(self):
        res = self.client().get('/movies', headers=self.assistantHeader)
        data=json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
    
    def test_assistant_postactor(self):
        res = self.client().post('/actors', headers=self.assistantHeader, json=self.new_actor)
        data=json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)
    
    def test_assistant_postmovie(self):
        res = self.client().post('/movies', headers=self.assistantHeader, json=self.new_movie)
        data=json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)
    
    def test_assistant_patchmovie(self):
        res = self.client().patch('/movies/1', headers=self.assistantHeader, json={"title":'new title'})
        data=json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)
    
    def test_assistant_patchactor(self):
        res = self.client().patch('/actors/1', headers=self.assistantHeader, json={"name":'new name'})
        data=json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)

    def test_assistant_deletemovie(self):
        res = self.client().delete('/movies/1', headers=self.assistantHeader)
        data=json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)

    def test_assistant_deleteactor(self):
        res = self.client().delete('/actors/1', headers=self.assistantHeader)
        data=json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)

    #General Tests
    # Test for an unidentified person (no role or Token). All the requests are expected to be rejected.
    def test_general_getactors(self):
        res = self.client().get('/actors')
        data=json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)

    def test_general_getmovies(self):
        res = self.client().get('/movies')
        data=json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)
    
    def test_general_postactor(self):
        res = self.client().post('/actors', json=self.new_actor)
        data=json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)
    
    def test_general_postmovie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data=json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)
    
    def test_general_patchmovie(self):
        res = self.client().patch('/movies/1', json={"title":'new title'})
        data=json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)
    
    def test_general_patchactor(self):
        res = self.client().patch('/actors/1', json={"name":'new name'})
        data=json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)

    def test_general_deletemovie(self):
        res = self.client().delete('/movies/1')
        data=json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)

    def test_general_deleteactor(self):
        res = self.client().delete('/actors/1')
        data=json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()