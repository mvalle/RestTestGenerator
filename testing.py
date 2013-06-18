import unittest
import requests

server = "http://localhost/api/v1/"

class TestAdApi(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        r = requests.get("http://localhost/tests/values")
        if r.status_code != 200:
            print "SetUp"
            print r.content
            print "-----"
        self.user = r.json().get("user")
        self.user["password"] = "abc" # from util.php

        r = requests.post(server+"auth/login", data=self.user)
        if r.status_code != 200:
            print "Login"
            print r.content
            print "-----"

        self.cookies = r.cookies


    @classmethod
    def tearDownClass(self):
        r = requests.get("http://localhost/tests/clean")
        if r.status_code != 200:
            print "TearDown"
            print r.content
            print "--------"

    def test_create_ad_when_logged_in(self):
        data = {"title": "Title",
                "subtitle": "Sub Title",
                "description": "Description of the Ad",
                "price": 12,
                "email": False,
                "twitter": False,
                "facebook": False,
                "phone": False,
                "ono": False,
                "status": "Status"}
        r = requests.post(server+"ad", data=data, cookies=self.cookies)
        self.assertEquals(r.status_code, 200)

        ad = r.json()

        self.assertIsNotNone(ad["id"])
        self.assertEqual(ad["title"], "Title")
        self.assertEqual(ad["user_id"], self.user["id"])

    def test_create_ad_when_not_logged_in(self):
        data = {"title": "Title",
                "subtitle": "Sub Title",
                "description": "Description of the Ad",
                "price": 12,
                "email": False,
                "twitter": False,
                "facebook": False,
                "phone": False,
                "ono": False,
                "status": "Status"}
        r = requests.post(server+"ad", data=data)
        if r.status_code == 500: print r.content

        self.assertEquals(r.status_code, 403)

    def test_login_with_wrong_password(self):
        data = {"email": self.user["email"],
                "password": "the.wrong"+self.user["password"]}
        #r = requests.post(server+"auth/login")
        #self.assertEquals(r.status_code, 400)

    def test_login_with_wrong_email_and_password(self):
        data = {"email": "the.wrong"+self.user["email"],
                "password": "the.wrong"+self.user["password"]}
        #r = requests.post(server+"auth/login")
        #self.assertEquals(r.status_code, 400)

    def test_login_via_get(self):
        pass
        #r = requests.get(server+"auth/login")
        #self.assertEquals(r.status_code, 405)

    def test_logout_when_logged_in(self):
        data = {"email": self.user["email"],
                "password": self.user["password"]}
        #r = requests.post(server+"auth/login", data=data)
        #self.assertEquals(r.status_code, 200)

        #self.assertIsNotNone(r.cookies.get("laravel_session"))
        #self.assertIsNotNone(r.cookies.get("session_payload"))

        #r = requests.get("http://localhost/tests/loggedin", cookies=r.cookies)
        #self.assertTrue(r.json())

        #r = requests.post(server+"auth/logout", cookies=r.cookies)


        #r = requests.get("http://localhost/tests/loggedin", cookies=r.cookies)
        #self.assertFalse(r.json())

    def test_logout_when_logged_out(self):
        pass
        #r = requests.post(server+"auth/logout")
        #self.assertEquals(r.status_code, 200)

        #r = requests.get("http://localhost/tests/loggedin", cookies=r.cookies)

        #self.assertFalse(r.json())

    def test_create_general_ad(self):
        data = {"title": "Ad Title",
                "subtitle": "Sub tititle",
                "price": 4,
                "desription": "Descripoton of ad",
                "expires": "2012-02-20",
                "category_type": "general",
                "condition": "New"
                }
        r = requests.post(server+"ad", data=data, cookies=self.cookies)

        if r.status_code == 500: print r.content

        self.assertEqual(r.status_code, 200)

        j = r.json()
        self.assertEqual(j["title"], "Ad Title")
        self.assertEqual(j["expires"], "2012-02-20")
        self.assertIsNotNone(j["id"])
        self.assertIsNotNone(j["category_id"])
        print j["id"]
        print j["category_id"]

    def test_update_ad(self):
        data = {"title": "Ad Title",
                                "subtitle": "Sub tititle",
                                "price": 4,
                                "desription": "Descripoton of ad",
                                "expires": "2012-02-20",
                                "category_type": "general",
                                "condition": "New"
                                }
        r = requests.post(server+"ad", data=data, cookies=self.cookies)
        if r.status_code == 500: print r.content

        self.assertEquals(r.status_code, 200)
        j = r.json()
        id = j["id"]

        data = {"price": 10}
        r = requests.put(server+"ad/"+str(id), data=data, cookies=self.cookies)
        if r.status_code == 500: print r.content

        self.assertEqual(r.status_code, 200)
        j = r.json()

        self.assertEqual(j["title"], "Ad Title")
        self.assertEqual(j["expires"], "2012-02-20 00:00:00")
        self.assertIsNotNone(j["id"])
        self.assertIsNotNone(j["category_id"])

        self.assertEqual(j["price"], 10)

    def test_delete_ad(self):
        data = {"title": "Ad Title",
                                "subtitle": "Sub tititle",
                                "price": 4,
                                "desription": "Descripoton of ad",
                                "expires": "2012-02-20",
                                "category_type": "general",
                                "condition": "New"
                                }
        r = requests.post(server+"ad", data=data, cookies=self.cookies)
        if r.status_code == 500: print r.content

        self.assertEquals(r.status_code, 200)
        j = r.json()
        id = j["id"]

        r = requests.delete(server+"ad/"+str(id), cookies=self.cookies)
        j = r.json()

        self.assertEquals(r.status_code, 200)
        if r.status_code == 500: print r.content

        self.assertEquals(j["id"], id)

    def test_delete_non_existant_ad(self):
        r = requests.delete(server+"ad/99999999999", cookies=self.cookies)
        if r.status_code == 500: print r.content

        self.assertEquals(r.status_code, 404)


    def test_delete_ad_with_no_id(self):
        r = requests.delete(server+"ad", cookies=self.cookies)
        if r.status_code == 500: print r.content

        self.assertEquals(r.status_code, 404)


    def test_view_ad(self):
        data = {"title": "Ad Title",
                                "subtitle": "Sub tititle",
                                "price": 4,
                                "desription": "Descripoton of ad",
                                "expires": "2012-02-20",
                                "category_type": "general",
                                "condition": "New"
                                }
        r = requests.post(server+"ad", data=data, cookies=self.cookies)
        if r.status_code == 500: print r.content

        self.assertEquals(r.status_code, 200)
        j = r.json()
        id = j["id"]

        r = requests.get(server+"ad/"+str(id))
        if r.status_code == 500: print r.content

        self.assertEqual(r.status_code, 200)

        self.assertEqual(j["title"], "Ad Title")
        self.assertEqual(j["expires"], "2012-02-20")
        self.assertIsNotNone(j["id"])
        self.assertIsNotNone(j["category_id"])

        
    def test_view_non_existant_ad(self):
        r = requests.get(server+"ad/9999999999999999")
        if r.status_code == 500: print r.content

        self.assertEqual(r.status_code, 404)

    def test_list_ad(self):
        # make sure there is atleast on ad, before checking the list
        data = {"title": "Ad Title",
                                "subtitle": "Sub tititle",
                                "price": 4,
                                "desription": "Descripoton of ad",
                                "expires": "2012-02-20",
                                "category_type": "general",
                                "condition": "New"
                                }
        r = requests.post(server+"ad", data=data, cookies=self.cookies)
        if r.status_code == 500: print r.content

        self.assertEquals(r.status_code, 200)

        j = r.json()
        id = j["id"]

        r = requests.get(server+"ad")

        ad = [ad for ad in r.json() if ad[u"id"] == id]
        self.assertNotEqual(ad, [])


if __name__ == '__main__':
    unittest.main()
