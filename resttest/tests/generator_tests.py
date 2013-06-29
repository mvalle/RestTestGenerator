import unittest
from resttest import Generator

class TestGenerator(unittest.TestCase):
    
    def test_create(self):
        g = Generator()
        self.assertIsNotNone(g.__getattribute__("parse"))
        self.assertIsNotNone(g.__getattribute__("class_name"))

    def test_parse(self):        
        data = "post /domain/<domain>"
        g = Generator()
        m = g.parse(data)
        self.assertIsNotNone(m)
        self.assertEqual("domain", m.class_name)
        self.assertEqual("post", m.method)
        self.assertEqual("/domain/<domain>", m.string)
        self.assertEqual(["domain", "<domain>"], m.bits)
        self.assertEqual(["domain"], m.parameters)
        self.assertEqual(["domain"], m.names)
        self.assertEqual("domain_by_domain", m.name)
    
    def test_parse_with_tabs(self):
        data = "post\t/domain/<domain>"
        g = Generator()
        m = g.parse(data)
        self.assertIsNotNone(m)
        self.assertEqual("domain", m.class_name)
        self.assertEqual("post", m.method)
        self.assertEqual("/domain/<domain>", m.string)
        self.assertEqual(["domain", "<domain>"], m.bits)
        self.assertEqual(["domain"], m.parameters)
        self.assertEqual(["domain"], m.names)
        self.assertEqual("domain_by_domain", m.name)
        


if __name__ == '__main__':
    unittest.main()
