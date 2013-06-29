class TestMethod:


    def __init__(self):
        self._method = ""
        self.string = ""
        self.bits = []
        self.parameters = []
        self.names = []
        #self.name = ""
        self.class_name = ""
        self.tab = "\t"

    @property
    def name(self):
        return self.generate_name()

    @property
    def method(self):
        return self._method.lower()

    @method.setter
    def set_method(self, value):
        self._method = value

    @property
    def param(self):
        return self.generate_parameter_list()

    def generate_method(self):
       # print self.generate_parameter_list()
        code = """
%(tab)sdef test_%(method)s_%(name)s(self):
%(tab)s%(tab)s
%(variables)s
%(tab)s%(tab)sresponse = %(method)s( %(parameters)s )
%(tab)s%(tab)s
%(tab)s%(tab)sself.assert(response_code, 200) 
""" % {"method":self.method, "name":self.name,
       "tab":self.tab, "parameters":self.param,
       "variables":self.generate_variable_initialisations()}

        return code

    def generate_variable_initialisations(self):
        s = ""
        for var in self.parameters:
            s += "%(tab)s%(tab)s%(variable)s = None\n" % {"tab":self.tab, "variable":var}
        return s
            

    def generate_name(self):
        name = ""
        for i in self.bits:
            if i.startswith("<"):
                name += "_by_"+i.strip("<").strip(">")
            else:
                name += "_"+i

        return name.strip("_")

    def generate_parameter_list(self):
        l = "\""
        last = "reg"
        for i in self.bits:
            if i.startswith("<"):
                if last == "reg":
                    l += "\"+"+i.strip("<").strip(">")
                else:
                    l += "+\"/\"+"+i.strip("<").strip(">")
                last = "param"
            else:
                if last == "reg":
                    l += i + "/"
                    
                else:
                    l += "+\"/" + i + "/"
                last = "reg"
            
        if last == "reg":
            l += "\""

        return l


