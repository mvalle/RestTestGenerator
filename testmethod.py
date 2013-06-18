class TestMethod:

    def __init__(self):
        self.method = ""
        self.string = ""
        self.bits = []
        self.parameters = []
        self.names = []
        self.name = ""
        self.class_name = ""
        self.tab = "\t"

    def generate_method(self):
       # print self.generate_parameter_list()
        code = """
%(tab)s%(tab)sdef test_%(method)s_%(name)s(self):
%(tab)s%(tab)s%(tab)sresponse = get( %(parameters)s )
%(tab)s%(tab)s%(tab)sself.assert(response_code, 200) 
""" % {"method":self.method, "name":"test"+self.name,
       "tab":self.tab, "parameters":self.generate_parameter_list()}


        return code

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
                    l += "+\"" + i + "/"
                last = "reg"
            
        if last == "reg":
            l + "\""

        return l


