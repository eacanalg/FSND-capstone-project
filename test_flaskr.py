import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor, db, database_name, database_path

# Define the Tokens used for  the tests. This tokens must be renewed
# each 24 hours according to Auth0 api config.
producerToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56azJRak0yTkRjeE56Z3pOVGMxTlVWQ09VWXhOamt5TkVVeVFVWkVNVGsyTnpRMU1qQTVRdyJ9.eyJpc3MiOiJodHRwczovL2VhY2cuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNjFiN2VmMjllMWUwMGQzZTc3OTI2YiIsImF1ZCI6ImNhcHN0b25lIHByb3llY3QiLCJpYXQiOjE1ODQ1OTMyMzcsImV4cCI6MTU4NDY3OTYzNywiYXpwIjoiQ1JzSzVydTUyRnVxT2Z6VTU5YmQ1Z3VRWWQyUm1wN1UiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.o52RGZMfTIPy4oqxyZpwTVXu_0I4704U_-8PPh9MWXHr_voOtdZTg1lr4zOJLz1-q5k1S8B0NqDhcmcqmOscBVuvXxnjCpQZ1K1k5Dwa4MqoMYCBEP87y9XBziVP5Kq-RSwO2SprFnrsbV0G183kdBHQ3Zli5xka-OnbqrOv5SpYw_C6m-O5Hqh8Uq4ptuBCqDOn9Dqup79ak_MgcnKTx8Rdjh5Asii6U04dTWEHu7C9gk-aNbT5BZukilR0XmAOc4eGSWEdAXeThcbtqDx0PwnwTfBpXLLgcCm6htiXi3CAl9y2jVmr7gmo1YQ3igkj0bGQkW8J0_Vxud8kRFJL0Q'
directorToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56azJRak0yTkRjeE56Z3pOVGMxTlVWQ09VWXhOamt5TkVVeVFVWkVNVGsyTnpRMU1qQTVRdyJ9.eyJpc3MiOiJodHRwczovL2VhY2cuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNjFiODNmMjViMmU2MGQzYjc3ZDRmOSIsImF1ZCI6ImNhcHN0b25lIHByb3llY3QiLCJpYXQiOjE1ODQ1OTMzNTMsImV4cCI6MTU4NDY3OTc1MywiYXpwIjoiQ1JzSzVydTUyRnVxT2Z6VTU5YmQ1Z3VRWWQyUm1wN1UiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBvc3Q6YWN0b3JzIl19.I8oJ9OmMhvtUOKvPGcFUrgco3WX7LPErDbZwI5NiOiHB0_uwerpmdbf0_RYGrjMWkgSrt0C0HACukWEXK_w09xda3Or2KyKNICsOdxX79OIkkuBZyFnb7TJ7bsBxTG2VzbQe8yT6iaYro9VvN74YpyhhtvwoSTL2_uJN79N1NKH0nwhzjriK2WEjG7Hcz33lj4HA35rK298azIA57iuCKg6802kpu_yETbDSUFxfOVtK3ckvLKD60RUdXcGruohIRALkDDqCwtEkRoJ0ss1zmoHn593uBAugVvw7chB40-IzndgK2tzKekPr0rzye1Gf6Z6TEQop7rkqrSYjkpNlnw'
assistantToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56azJRak0yTkRjeE56Z3pOVGMxTlVWQ09VWXhOamt5TkVVeVFVWkVNVGsyTnpRMU1qQTVRdyJ9.eyJpc3MiOiJodHRwczovL2VhY2cuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNzA0MjIyMTI2ZDZhMGMzMTM2OGI4NyIsImF1ZCI6ImNhcHN0b25lIHByb3llY3QiLCJpYXQiOjE1ODQ1OTM0MzUsImV4cCI6MTU4NDY3OTgzNSwiYXpwIjoiQ1JzSzVydTUyRnVxT2Z6VTU5YmQ1Z3VRWWQyUm1wN1UiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.FrYa4nN5pNImV3gYFr5Gca2rNmh83GM0a00aOa6KkcWxarVMU_tEfhTb9cNfB93fKXbiwRiKtmdlwMvpfh9tMZSYp6NscqjbaGUu0h3sciCR3CHDdMLDPbuDJ-ay660iMmKKlJWmg2PtVpIFXZ2st34Tqpu6bLCvImglbGoDihuyAuaG-mFw0zlczNnwpTUAnRSdktJmim0jr05KpVjet3ZaVfA_YUWg12kAJHiJJ1ldcRTr2Iv714cdU2neBNiXLELxisv_RZzBOUsVHMNjNs7gQXcAdIuJsDwufDr7jkBPWNSIN_Ge_-OppfujWGvZqNw73MUqVN4_qWSEuQLR5w'


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

        # Creates a movie object to be inserted in POST endpoints
        # Id is not necessary and suggested to not specify.
        # In this case ID is used for keeping track for future
        # PATCH and DELETE over the same object
        self.new_movie = {
            "title": "Star Wars",
            "release": "2020/03/05",
            "actors": [],
            "id": 1
        }
        # Creates an actor object to be inserted in POST endpoints
        # Id is not necessary and suggested to not specify.
        # In this case ID is used for keeping track for future
        # PATCH and DELETE over the same object
        self.new_actor = {
            "name": "Brad Pitt",
            "gender": "male",
            "age": 42,
            "movies": [],
            "id": 1
        }

        # Creates the headers used for each one of the roles request's
        self.producerHeader = {
            'Content-Type': 'application/json',
            'authorization': f'Bearer {producerToken}'}
        self.directorHeader = {
            'Content-Type': 'application/json',
            'authorization': f'Bearer {directorToken}'}
        self.assistantHeader = {
            'Content-Type': 'application/json',
            'authorization': f'Bearer {assistantToken}'}

    def tearDown(self):
        """Executed after reach test"""
        pass
    # Producer tests
    # All the following tests use the prodocer autorization token.

    # test endpoint to get all the existing actors
    def test_producer_getactors(self):
        res = self.client().get('/actors', headers=self.producerHeader)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    # test endpoint to get all existing movies.
    def test_producer_getmovies(self):
        res = self.client().get('/movies', headers=self.producerHeader)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    # Test the post, patch and delete endpoints for actors
    # This are joined because they Patch and Delete work on the object
    # created by the post request. This test is dessigned to run
    # regardless of the db state as long as no item with id 1 is created
    # manually. As psql doesn't reuse deleted ids, id one is expected
    # only to be used by tests.
    def test_producer_ppdactor(self):
        # Post
        res = self.client().post('/actors', headers=self.producerHeader,
                                 json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        # Patch
        res = self.client().patch('/actors/1', headers=self.producerHeader,
                                  json={"name": "new name"})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        # Delete
        res = self.client().delete('/actors/1', headers=self.producerHeader)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    # Test post, patch and delete endpoints for movies in the same way as
    # test_producer_ppdactor.
    def test_producer_ppdmovie(self):
        # Post
        res = self.client().post('/movies', headers=self.producerHeader,
                                 json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        # Patch
        res = self.client().patch('/movies/1', headers=self.producerHeader,
                                  json={"title": "new title"})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        # Delte
        res = self.client().delete('/movies/1', headers=self.producerHeader)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    # Director Tests
    # Same tests as in Producer but with the director Token.

    def test_director_getactors(self):
        res = self.client().get('/actors', headers=self.directorHeader)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_director_getmovies(self):
        res = self.client().get('/movies', headers=self.directorHeader)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    # As  post, patch and delete request for movies are expected to be denied
    # by RBAC the tests can be runned individually.
    def test_director_postmovie(self):
        res = self.client().post('/movies', headers=self.directorHeader,
                                 json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)

    def test_director_patchmovie(self):
        res = self.client().patch('/movies/1', headers=self.directorHeader,
                                  json={"title": 'new title'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)

    def test_director_deletemovie(self):
        res = self.client().delete('/movies/1', headers=self.directorHeader)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)

    def test_director_ppdactor(self):
        # Post
        res = self.client().post('/actors', headers=self.directorHeader,
                                 json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        # Patch
        res = self.client().patch('/actors/1', headers=self.directorHeader,
                                  json={"name": "new name"})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        # Delete
        res = self.client().delete('/actors/1', headers=self.directorHeader)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    # Assistant tests
    # tests all point with the assistant permissions.
    # Here all tests  can be runned individually.

    def test_assistant_getactors(self):
        res = self.client().get('/actors', headers=self.assistantHeader)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_assistant_getmovies(self):
        res = self.client().get('/movies', headers=self.assistantHeader)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_assistant_postactor(self):
        res = self.client().post('/actors', headers=self.assistantHeader,
                                 json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)

    def test_assistant_postmovie(self):
        res = self.client().post('/movies', headers=self.assistantHeader,
                                 json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)

    def test_assistant_patchmovie(self):
        res = self.client().patch('/movies/1', headers=self.assistantHeader,
                                  json={"title": 'new title'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)

    def test_assistant_patchactor(self):
        res = self.client().patch('/actors/1', headers=self.assistantHeader,
                                  json={"name": 'new name'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)

    def test_assistant_deletemovie(self):
        res = self.client().delete('/movies/1', headers=self.assistantHeader)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)

    def test_assistant_deleteactor(self):
        res = self.client().delete('/actors/1', headers=self.assistantHeader)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 403)

    # General Tests
    # Test for an unidentified person (no role or Token).
    # All the requests are expected to be rejected.
    def test_general_getactors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)

    def test_general_getmovies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)

    def test_general_postactor(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)

    def test_general_postmovie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)

    def test_general_patchmovie(self):
        res = self.client().patch('/movies/1', json={"title": 'new title'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)

    def test_general_patchactor(self):
        res = self.client().patch('/actors/1', json={"name": 'new name'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)

    def test_general_deletemovie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)

    def test_general_deleteactor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
