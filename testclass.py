from os import path

class TestClass:

    @property
    def code(self):
        return self.generate_class()

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
""" % {"classname":self.classify(self.class_name), "tab":self.tab}

        code += self.generate_methods()

        return code


    def add_method(self, m):
        self.methods.append(m)

    def __str__(self):
        return "<TestClass class: %s methods:%d>" % (self.class_name, len(self.methods))

    def __unicode__(self):
        return self.__str__() 

    def classify(self, in_s):
        if len(in_s) == 0: return ""
        head = in_s[0]
        tail = in_s[1:]
        return head.upper() + tail

    def filename(self, directory):
        return path.join(directory, self.class_name.lower()+".py")
