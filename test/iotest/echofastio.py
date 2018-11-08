import os
import sys

# sys.stdin.readline()
print(str(os.read(0, 100000000), 'utf-8'))
