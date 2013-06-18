class TestClass:

    def __init__(self, class_name):
        self.class_name = class_name
        self.methods = []
        self.tab = "\t"

    def generate_methods(self):
        code = ""
        #pdb.set_trace()
        for m in self.methods:
            code += m.generate_method()

        return code

    def generate_class(self):
        #pdb.set_trace()
        code = """import requeststest

class %(classname)sTest(requesttest.RequestTest):

%(tab)s#self.server = "example.com"
%(tab)s
""" % {"classname":"<TESTCLASSGOESHERE>"+self.class_name, "tab":self.tab}

        print "CLASS NAME: " + self.class_name
        print dir(self)

        code += self.generate_methods()

        return code

    def __str__(self):
        return "<TestClass class: %s methods:%d>" % (self.class_name, len(self.methods))

    def __unicode__(self):
        return self.__str__() 
