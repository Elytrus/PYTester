import sys
import io
import atexit

_INPUT_LINES = sys.stdin.read().splitlines()
nexts = iter(_INPUT_LINES).__next__
_OUTPUT_BUFFER = io.BytesIO()
sys.stdout = _OUTPUT_BUFFER


@atexit.register
def write():
    sys.__stdout__.write(_OUTPUT_BUFFER.getvalue())


n = int(nexts())
for _ in range(n):
    print(nexts())

write()