#!/usr/bin/env python

# Brian Lim, Elaine Apaza, Sandeep Gupta, Scot Freysinger
# blimmer, etapaza, sandgupt, sfrey

import sys
import re
import os
import math
import sets

def calc_pagerank(url_score, in_edges, out_edges, threshold):
  iterate = True
  web_const = float(1.0 - 0.85) / float(len(url_score))
  iteration = 0

  # iterate until convergence below threshold
  # value for all pages in the graph
  while iterate:
    # Calculate new score for each page
    for url in url_score:
      weight = 0.0
      if url in in_edges:
        # sum up the value for the score of an in edge
        # divided by the number of out edges that page
        # has
        for edge in in_edges[url]:
          weight += float(url_score[edge][iteration]) / float(len(out_edges[edge]))

      # calculate the new pagerank score, and append it
      # to the list of scores
      new_score = float(web_const) + 0.85 * float(weight)
      url_score[url].append(new_score)

    iterate = False
    # check to make sure all pagerank scores change fall
    # within the change threshold.
    for url in url_score:
      score_dif = float(url_score[url][iteration]) - float(url_score[url][iteration + 1])
      if score_dif > threshold:
        iterate = True
        break

    iteration += 1

  return iteration, url_score


#~~~ Run PageRank ~~~
node_link = sys.argv[1]

urls = open(node_link)


threshold = 0.001
url_score = {}
in_edges = {}
out_edges = {}

# Initialize data


for line in urls:
  nodes = line.split()
  if nodes[0] not in url_score:
    url_score[nodes[0]]  = [0.25]

  if nodes[1] not in url_score:
    url_score[nodes[1]]  = [0.25]



  if nodes[1] in in_edges:
    in_edges[nodes[1]].append(nodes[0].strip())
  else:
    in_edges[nodes[1]] = [nodes[0].strip()]

  if nodes[0] in in_edges:
    in_edges[nodes[0]].append(nodes[1].strip())
  else:
    in_edges[nodes[0]] = [nodes[1].strip()]

  if nodes[0] in out_edges:
    out_edges[nodes[0]].append(nodes[1].strip())
  else:
    out_edges[nodes[0]] = [nodes[1].strip()]

  if nodes[1] in out_edges:
    out_edges[nodes[1]].append(nodes[0].strip())
  else:
    out_edges[nodes[1]] = [nodes[0].strip()]


for number in in_edges:
  print(number, len(in_edges[number]))

# Calculate the pagerank scores for each node
pagerank_data = calc_pagerank(url_score, in_edges, out_edges, threshold)

print('number of iterations: ' + str(pagerank_data[0] + 1))

outfile = open('redditPagerankings', 'w')
for url in pagerank_data[1]:
  line = url + ' ' + str(pagerank_data[1][url][pagerank_data[0]]) + '\n'
  outfile.write(line)
