import os
import unittest
from urlparse import urlparse

from werkzeug.security import generate_password_hash

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "synonyms.config.TestingConfig"

from synonyms import app
from synonyms import models
from synonyms.database import Base, engine, session

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        Create an example user
        self.user = models.User(name="Alice", email="alice@example.com",
                                password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()
        
        
    def simulate_login(self):
        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(self.user.id)
            http_session["_fresh"] = True

    def testAddPost(self):
        self.simulate_login()

        response = self.client.post("/post/add", data={
            "title": "Test Post",
            "content": "Test content"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        words = session.query(models.Word).all()
        self.assertEqual(len(words), 1)

        word = words[0]
        self.assertEqual(words.content, "<p>Test word content</p>\n")
        self.assertEqual(words.author, self.user)    

    def testDeletePost(self):  #this is not described in detail in tutorial, only testAddPost is in tutorial
        self.simulate_login()

        response1 = self.client.post("/post/add", data={
            "title": "Test Post1",
            "content": "Test content1"
        })
        

        self.assertEqual(response1.status_code, 302)
        self.assertEqual(urlparse(response1.location).path, "/")
        words = session.query(models.Word).all()
        self.assertEqual(len(words), 1)


        
        #we are testing that word1 is in fact being deleted.  This is the real test.
        word1 = words[0]
        word1_id = word1.id
        delete_url1 = "/post/" + str(word1.id) + "/delete"
        response = self.client.post(delete_url1)
        self.assertEqual(response1.status_code, 302)     
        word_list = session.query(models.Word).all()
        self.assertEqual(len(word_list), 0)

        
        
    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

if __name__ == "__main__":
    unittest.main()