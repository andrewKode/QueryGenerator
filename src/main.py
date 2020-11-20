import sys

from generator import QueryGenerator

if __name__ == '__main__':
    queryGenerator = QueryGenerator(sys.argv[1])
    queryGenerator.run()