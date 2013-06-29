import unittest
from resttest import TestMethod
from resttest import Generator

class TestTestMethod(unittest.TestCase):

    def setUp(self):
        self.g = Generator()

    def test_create(self):
        m = TestMethod()
        self.assertEqual("\t", m.tab)


    def test_generate_parameter_list(self):
        data = "post /domain/<domain>"
        m = self.g.parse(data)
        plist =  m.generate_parameter_list()
        self.assertEqual('"domain/"+domain',plist)

    def test_generate_method(self):
        data = "post /domain/<domain>"
        m = self.g.parse(data)
        code = m.generate_method()
        self.assertTrue(code.find("def test_post_domain_by_domain(self):") > 0)
        self.assertTrue(code.find('response = post( "domain/"+domain )') > 0)

    def test_generate_variable_initialisations(self):
        data = "get /domain/<domain>/contacts/<id>"
        m = self.g.parse(data)
        code = m.generate_variable_initialisations()

        self.assertTrue(code.find("domain = None") > 0)
        self.assertTrue(code.find("id = None") > 0)






















