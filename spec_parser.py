


if __name__ == '__main__':
    classes = {}
    for line in open("spec"):
        #print
        print "#" + line
        p = parse(line)
        #print p.generate_parameter_list()
        
        if classes.has_key(p.class_name):
            c = classes.get(p.class_name)
        else:
            c = TestClass(p.class_name)
            classes[p.class_name] = c

        c.methods.append(p)

        #pdb.set_trace()



    for i in classes.values():
        print c.class_name
        print len(c.methods)
        print c.generate_class()

