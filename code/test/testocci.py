#!/usr/bin/python
import getopt
import random
import sys
import unittest

class TestSequenceFunctions(unittest.TestCase):
    
    def setUp(self):
        self.seq = range(10)
    
    def testshuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))
    
    def testchoice(self):
        element = random.choice(self.seq)
        self.assert_(element in self.seq)
    
    def testsample(self):
        self.assertRaises(ValueError, random.sample, self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assert_(element in self.seq)

def usage():
	print "Real men read source code."

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:p:t:", ["help", "hostname=", "username=", "password="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    username = "test"
    password = "test"
    target = "localhost"
    
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-u", "--username"):
            username = a
        elif o in ("-p", "--password"):
            password = a
        elif o in ("-t", "--target"):
            target = a
        else:
            assert False, "unhandled option"
    
    unittest.main()
