import sys

f = open('listOfSubreddits.txt')
o = open('formated_output.txt', 'w')

for line in f:
  s = line.split()[1]
  sub = s[3:]
  sub += '\n'
  o.write(sub)
