import requests
import unittest

class RequestTest(unittest.TestCase):

    self.protocol = "http"
    self.server = "localhost"
    self.cookies = None
    self.cookie_jar = False

    def _url(self, method):
        return self.protocol+"//"+self.server+"/"+method

    def get(self, method, data=None, cookies=None):
        if self.cookie_jar:
            if cookies == None:
                cookies = self.cookie

        r = requests.get(self._url(method), data=data, cookies=cookies)
        if self.cookie_jar:
            self.cookies = r.cookies
        return r

    def put(self, method, data=None, cookies=None):
        if self.cookie_jar:
            if cookies == None:
                cookies = self.cookie

        r = requests.put(self._url(method), data=data, cookies=cookies)
        if self.cookie_jar:
            self.cookies = r.cookies
        return r

    def post(self, method):
        if self.cookie_jar:
            if cookies == None:
                cookies = self.cookie

        r =  requests.post(self._url(method), data=data, cookies=cookies)
        if self.cookie_jar:
            self.cookies = r.cookies
        return r


