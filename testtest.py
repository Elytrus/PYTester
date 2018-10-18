import subprocess as sb

mini = sb.Popen(['py', 'echo.py'], stdin=sb.PIPE, stdout=sb.PIPE)
data = str(mini.communicate(b'Hello, World!')[0], 'utf-8')
print(data)
