import sys

from resttest import Generator

def main(argv):
    spec_filename = argv[0]
    overwrite = argv[:1][0] == "--overwrite"
    if overwrite:
        target_dirname = argv[1] if len(argv) == 3 else "."
    else:
        target_dirname = argv[1] if len(argv) == 2 else "."

    generator = Generator()
    spec_file = open(spec_filename)
    generator.generate_from_file(spec_file)
    generator.save(target_dirname, overwrite)

def usage():
    print "python generate.py specfile [targetfolder] [--overwrite]"

if __name__ == '__main__':
    if len(sys.argv)-1 in [1, 2, 3]:
        main(sys.argv[1:])
    else:
        print len(sys.argv)
        usage()
