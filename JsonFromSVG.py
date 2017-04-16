import xml.etree.ElementTree as ET
import json
import sys
import commentCompile
import pickle

"""This script converts a SVG file into a JSON file for data assignment using d3. 
This script should be replaced with a more holistic one that integrates original data that is lost during the svg conversion, such as post content or upvotes."""

filename = sys.argv[1]
limit = sys.argv[2]
if filename[-4:] == ".svg":
    filename = filename[:-4]
try:
    algorithm = sys.argv[3]
except:
    algorithm = "openord"

container = list()
jsonrep = dict()
edges = list()
nodes = list()
arrows = list()
labels = list()

additionalInfo = dict()

tree = ET.parse("out/" + filename + limit + algorithm + ".svg")
root = tree.getroot()

svgattribs = root.attrib
width  = svgattribs["width"]
height = svgattribs["height"]
viewbox = svgattribs["viewBox"]

for child in root:
    for element in child:
        elementID = child.attrib["id"]
        attribs = element.attrib
        attribs["name"] = attribs["class"]
        if elementID == "nodes":
            nodes.append(attribs)
        elif elementID == "edges":
            edges.append(attribs)
        elif elementID == "arrows":
            arrows.append(attribs)
        elif elementID == "node-labels":
            attribs["text"] = element.text
            labels.append(attribs)
            
            
jsonrep["nodes"] = nodes
jsonrep["edges"] = edges
jsonrep["arrows"] = arrows
jsonrep["labels"] = labels

jsonrep["width"] = width
jsonrep["height"] = height
jsonrep["viewBox"] = viewbox

# Next, read in the context.
context = open("DBs/" + filename + "_db.pickle", "r")
DB = pickle.load(context)
context.close()


for key in DB:
    buffer = dict()
    buffer["name"] = DB[key].ID;
    buffer["in"] = DB[key].commentsRecieved;
    buffer["out"] = DB[key].commentsMade;
    buffer["contexts"] = DB[key].parents;    
    additionalInfo[key] = buffer;


container.append(jsonrep)
container.append(additionalInfo)

file = open("out/" + filename + limit + algorithm + ".json", "w")
file.write(json.dumps(container, sort_keys=True, indent=4, separators=(',', ': ')))
