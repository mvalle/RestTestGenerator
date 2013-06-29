import sys

from resttest import Generator

def main(argv):
    spec_filename = argv[0]
    target_dirname = argv[1] if len(argv) == 2 else "."

    generator = Generator()
    spec_file = open(spec_filename)
    generator.generate_from_file(spec_file)
    generator.save(target_dirname)

def usage():
    print "python generate.py specfile [targetfolder]"

if __name__ == '__main__':
    if len(sys.argv)-1 in [1, 2]:
        main(sys.argv[1:])
    else:
        print len(sys.argv)
        usage()
