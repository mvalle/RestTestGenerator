import unittest
from testmethod import TestMethod
from testclass import TestClass
from generator import Generator

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
        


class TestTestClass(unittest.TestCase):

    def setUp(self):
        self.g = Generator()


    def test_create(self):
        name = "Some_name"
        c = TestClass(name)
        self.assertEqual(name, c.class_name)

    def test_generate_methods(self):
        data = "post /domain/<domain>"
        m = self.g.parse(data)

        c = TestClass(m.class_name)
        c.add_method(m)

        code = c.generate_methods()

        self.assertTrue(code.find("def test_post_domain_by_domain(self):") > 0)
        self.assertTrue(code.find('response = post( "domain/"+domain )') > 0)

    def test_add_method(self):
        data = "post /domain/<domain>"
        m = self.g.parse(data)

        c = TestClass(m.class_name)
        c.add_method(m)

        self.assertEqual(c.methods[0], m)


    def test_add_method_twice(self):
        data1 = "post /domain/<domain>"
        data2 = "get /domain/<id>"

        m1 = self.g.parse(data2)
        m2 = self.g.parse(data1)
        c = TestClass(m1.class_name)
        c.add_method(m1)
        c.add_method(m2)

        self.assertEqual(c.methods[0], m1)
        self.assertEqual(c.methods[1], m2)

        

    def test_generate_methods_two_methods(self):
        data1 = "post /domain/<domain>"
        data2 = "get /domain/<id>"

        m1 = self.g.parse(data1)
        m2 = self.g.parse(data2)

        c = TestClass(m1.class_name)
        c.add_method(m1)
        c.add_method(m2)

        code = c.generate_methods()

        self.assertTrue(code.find("def test_post_domain_by_domain(self):") > 0)
        self.assertTrue(code.find('response = post( "domain/"+domain )') > 0)

        self.assertTrue(code.find("def test_get_domain_by_id(self):") > 0)
        self.assertTrue(code.find('response = get( "domain/"+id )') > 0)

    def test_generate_class_simple(self):
        name = "TestC"
        c = TestClass(name)

        code = c.generate_class()

        self.assertTrue(code.find("class TestCTest(requesttest.RequestTest):") > 0)

    def test_generate_class_simple_title(self):
        name = "testC"
        c = TestClass(name)

        code = c.generate_class()

        self.assertTrue(code.find("class TestCTest(requesttest.RequestTest):") > 0)


    def test_generate_class(self):
        data = "post /domain/<domain>"
        m = self.g.parse(data)

        c = TestClass(m.class_name)
        c.add_method(m)

        code = c.generate_class()

        self.assertTrue(code.find("class DomainTest(requesttest.RequestTest):") > 0)

        self.assertTrue(code.find("def test_post_domain_by_domain(self):") > 0)
        self.assertTrue(code.find('response = post( "domain/"+domain )') > 0)

    def test_generate_class_two_methods(self):
        data1 = "post /domain/<domain>"
        data2 = "get /domain/<id>"

        m1 = self.g.parse(data1)
        m2 = self.g.parse(data2)

        c = TestClass(m1.class_name)
        c.add_method(m1)
        c.add_method(m2)

        code = c.generate_class()

        self.assertTrue(code.find("class DomainTest(requesttest.RequestTest):") > 0)

        self.assertTrue(code.find("def test_post_domain_by_domain(self):") > 0)
        self.assertTrue(code.find('response = post( "domain/"+domain )') > 0)

        self.assertTrue(code.find("def test_get_domain_by_id(self):") > 0)
        self.assertTrue(code.find('response = get( "domain/"+id )') > 0)

    def test_generate_method_name(self):
        data = "get /domain/<domain>/contacts/<id>"
        m = self.g.parse(data)

        name = m.generate_name()

        self.assertEqual("domain_by_domain_contacts_by_id", name)

    def test_generate_method_parameter_list(self):
        data = "get /domain/<domain>/contacts/"
        m = self.g.parse(data)

        params = m.generate_parameter_list()

        self.assertEqual('"domain/"+domain+"/contacts/"', params)

    def test_generate_method_parameter_list_with_id(self):
        data = "get /domain/<domain>/contacts/<id>"
        m = self.g.parse(data)

        params = m.generate_parameter_list()

        self.assertEqual('"domain/"+domain+"/contacts/"+id', params)



    def test_generate_from_file(self):
        g = Generator()

        open_file = open("spec")

        g.generate_from_file(open_file)

        self.spec_assertions(g)

    def spec_assertions(self, g):
        domain = g.get_class("domain").generate_class()
        search = g.get_class("search").generate_class()
        domain_contacts = g.get_class("domain_contacts").generate_class()
        domain_nameservers = g.get_class("domain_nameservers").generate_class()
        domain_renew = g.get_class("domain_renew").generate_class()
        domain_transfer = g.get_class("domain_transfer").generate_class()
        domain_restore = g.get_class("domain_restore").generate_class()

        self.assertTrue(domain.find("class DomainTest(requesttest.RequestTest):") > 0)
        self.assertTrue(domain.find("def test_post_domain_by_domain(self):") > 0)
        self.assertTrue(domain.find("def test_get_domain_by_domain(self):") > 0)
        self.assertTrue(domain.find('response = get( "domain/"+domain )') > 0)
        self.assertTrue(domain.find('response = post( "domain/"+domain )') > 0)

        self.assertTrue(search.find("class SearchTest(requesttest.RequestTest):") > 0)
        self.assertTrue(search.find("def test_get_search_by_domain(self):") > 0)
        self.assertTrue(search.find('response = get( "search/"+domain )') > 0)


        dc = domain_contacts
        self.assertTrue(dc.find("class Domain_contactsTest(requesttest.RequestTest):") > 0)
        self.assertTrue(dc.find("def test_post_domain_by_domain_contacts(self):") > 0)
        self.assertTrue(dc.find("def test_get_domain_by_domain_contacts(self):") > 0)
        self.assertTrue(dc.find("def test_get_domain_by_domain_contacts_by_id(self):") > 0)
        self.assertTrue(dc.find("def test_put_domain_by_domain_contacts_by_id(self):") > 0)

        self.assertTrue(dc.find('response = put( "domain/"+domain+"/contacts/"+id )') > 0)
        self.assertTrue(dc.find('response = post( "domain/"+domain+"/contacts/" )') > 0)
        self.assertTrue(dc.find('response = get( "domain/"+domain+"/contacts/" )') > 0)
        self.assertTrue(dc.find('response = get( "domain/"+domain+"/contacts/"+id )') > 0)
        self.assertTrue(dc.find('response = put( "domain/"+domain+"/contacts/"+id )') > 0)

        
        dn = domain_nameservers
        self.assertTrue(dn.find("class Domain_nameserversTest(requesttest.RequestTest):") > 0)
        self.assertTrue(dn.find("def test_post_domain_by_domain_nameservers(self):") > 0)
        self.assertTrue(dn.find("def test_get_domain_by_domain_nameservers(self):") > 0)
        self.assertTrue(dn.find("def test_put_domain_by_domain_nameservers_by_id(self):") > 0)
        self.assertTrue(dn.find("def test_get_domain_by_domain_nameservers_by_id(self):") > 0)

        self.assertTrue(dn.find('response = put( "domain/"+domain+"/nameservers/"+id )') > 0)
        self.assertTrue(dn.find('response = post( "domain/"+domain+"/nameservers/" )') > 0)
        self.assertTrue(dn.find('response = get( "domain/"+domain+"/nameservers/" )') > 0)
        self.assertTrue(dn.find('response = get( "domain/"+domain+"/nameservers/"+id )') > 0)

        
        dr = domain_renew
        self.assertTrue(dr.find("class Domain_renewTest(requesttest.RequestTest):") > 0)
        self.assertTrue(dr.find("def test_put_domain_by_domain_renew(self):") > 0)
        self.assertTrue(dr.find('response = put( "domain/"+domain+"/renew/" )') > 0)


        dt = domain_transfer
        self.assertTrue(dt.find("class Domain_transferTest(requesttest.RequestTest):") > 0)
        self.assertTrue(dt.find("def test_put_domain_by_domain_transfer(self):") > 0)
        self.assertTrue(dt.find('response = put( "domain/"+domain+"/transfer/" )') > 0)

        drs = domain_restore
        self.assertTrue(drs.find("class Domain_restoreTest(requesttest.RequestTest):") > 0)
        self.assertTrue(drs.find("def test_put_domain_by_domain_restore(self):") > 0)
        self.assertTrue(drs.find('response = put( "domain/"+domain+"/restore/" )') > 0)

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

if __name__ == '__main__':
    unittest.main()
