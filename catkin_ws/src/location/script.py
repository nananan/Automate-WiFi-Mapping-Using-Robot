
import fileinput
import re
num = 345
for line in fileinput.input():
    line = re.sub(r'\([0-9]*,','(', line.rstrip())
    num = num+1
    print(line)
 