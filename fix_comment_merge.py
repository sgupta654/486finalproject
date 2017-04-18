import sys
import os

comments = sys.argv[1]
fixed = False
for filename in os.listdir('./r/' + comments):
  f = open('./r/' + comments +'/'+ filename, 'r')
  #print('checking: ' + './r/' + comments +'/'+ filename)
  merge = False
  for line in f:
    #print('filename: ' + line)
    if '<<<<<<<' in line:
      #print('found head')
      merge = True
      continue
    if merge:
      fixed = True
      merge = False
      #print(line)
      o = open('./r/' + comments +'/'+ filename, 'w')
      o.write(line)
      f.close()
      o.close()
      break

#television
#sports
#space
#mildlyinteresting
#Showerthoughts
#LifeProTips
#DIY
