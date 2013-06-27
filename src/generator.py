import re


from testmethod import TestMethod
from testclass import TestClass

class Generator(object):

    def __init__(self):
        self.classes = {}

    def parse(self, s):
        if s.find("#") > 0:
            s = s.split("#")[0]

        tokens = [i for i in re.split("[\n\s\t]", s) if i.strip() != ""]
        if len(tokens) < 2:
            return TestMethod()

        c = TestMethod()

        c.method = tokens[0]
        c.string = tokens[1]

        for part in c.string.split("/"):
            if part is "": continue
            if part.startswith("<"):
                c.parameters.append(part.strip("<").strip(">"))
            else:
                c.names.append(part)

            c.bits.append(part)

        c.names = [n for n in c.names if n is not ""]
        
        c.class_name = "_".join(c.names)

        return c

    def class_name(self, names):
        cn = "_".join(names)
        return cn

    def generate_from_file(self, open_file):
        for line in open_file:
            t_method = self.parse(line)
        
            self.add_method(t_method)
    
    def add_method(self, method):
        cls = self.get_class(method.class_name)
        if cls is None:
            cls = self.add_class(method.class_name)

        cls.add_method(method)

        return cls

    def get_class(self, class_name):
        return self.classes.get(class_name, None)

    def add_class(self, class_name):
        cls = TestClass(class_name)
        self.classes[class_name] = cls

        return cls

    def save(self, directory):
        for cls in self.classes.values():
            filename = cls.filename(directory)
            with open(filename, "w") as py:
                py.write(cls.code)





