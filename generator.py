import re

class Generator:

    def parse(self, s):
        if s.find("#") > 0:
            s = s.split("#")[0]

        tokens = [i for i in re.split("[\n\s\t]", s) if i.strip() != ""]
        if len(tokens) < 2:
            return TestMethod()

        c = TestMethod()
        c.mehtod = tokens[0]
        c.string = tokens[1]
    
        for part in c.string.split("/"):
            if part.startswith("<"):
                c.parameters.append(part.strip("<").strip(">"))
            else:
                c.names.append(part)

            c.bits.append(part)

        c.names = [n for n in c.names if n is not ""]

        c.name = c.bits[0]
        
        c.class_name = "_".join(c.names)

        return c

    def class_name(self, names):
        cn = "_".join(names)
        return cn

