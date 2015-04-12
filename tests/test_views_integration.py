import os
import unittest
from urlparse import urlparse

from werkzeug.security import generate_password_hash

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user
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
        posts = session.query(models.Post).all()
        self.assertEqual(len(posts), 1)

        post = posts[0]
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "<p>Test content</p>\n")
        self.assertEqual(post.author, self.user)    

    def testDeletePost(self):  #this is not described in detail in tutorial, it from example of testAddPost
        self.simulate_login()

        response1 = self.client.post("/post/add", data={
            "title": "Test Post1",
            "content": "Test content1"
        })
        
        response2 = self.client.post("/post/add", data={
            "title": "Test Post2",
            "content": "Test content2"
        })

        self.assertEqual(response1.status_code, 302)
        self.assertEqual(urlparse(response1.location).path, "/")
        posts = session.query(models.Post).all()
        self.assertEqual(len(posts), 2)

        #we are testing that post 2 is NOT being deleted.  In contrast to post 1 which IS deleted
        post2 = posts[1]
        post2_id = post2.id
        delete_url2 = "/post/" + str(post2.id) + "/delete"
        post2_list = session.query(models.Post).filter(models.Post.id == post2_id).all()
        self.assertEqual(len(post2_list), 1)
        
        #we are testing that post1 is in fact being deleted.  This is the real test.
        post1 = posts[0]
        post1_id = post1.id
        delete_url1 = "/post/" + str(post1.id) + "/delete"
        session.delete(post1)
        session.commit()
        post1_list = session.query(models.Post).filter(models.Post.id == post1_id).all()
        self.assertEqual(len(post1_list), 0)

        
        
    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

if __name__ == "__main__":
    unittest.main()