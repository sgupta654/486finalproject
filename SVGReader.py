import xml.etree.ElementTree as ET
import re


class Transform:
    @staticmethod
    def RealfromViewboxCoords(header, coords):
        zeroed = Transform.ZeroedFromViewboxCoords(coords)
        relCoords = zeroed[0] / header.viewbox.relwidth, zeroed[1] / header.viewbox.relheight
        realCoords = relCoords[0] * header.w, relCoords[1] * header.h
        return realCoords

    @staticmethod
    def ZeroedFromViewboxCoords(header, coords):
        return coords[0] - header.viewbox.startX, coords[1] - header.viewbox.startY
    
    @staticmethod
    def RelativeFromViewboxCoords(header, coords, scale = 1):
        zeroed = Transform.ZeroedFromViewboxCoords(header, coords)
        return zeroed[0] / header.viewbox.relwidth * scale, zeroed[1] / header.viewbox.relheight * scale

    @staticmethod  
    def RGBFromHex(hexcode):
        if hexcode[0] == """#""":
            hexcode = hexcode[1:] # remove the sharp
        if len(hexcode) != 6:
            raise ValueError("invalid hexcode for Transform.RGBFromHex(): %s" % hexcode)
        # Now that we have a hexcode that satisfies our conditions,
        r = hexcode[0:2]
        g = hexcode[2:4]
        b = hexcode[4:6]

        r = int(r, 16)
        g = int(g, 16)
        b = int(b, 16)

        r /= 255.0
        g /= 255.0
        b /= 255.0

        return r, g, b

class SVGElement:
    def __init__(self, elementType, attrib):
        self.type = elementType
        self.attrib = dict(attrib)
        if   self.type == "path": self.PathFromXML(attrib)
        elif self.type == "polyline": self.PolylineFromXML(attrib)
        elif self.type == "circle": self.CircleFromXML(attrib)
        elif self.type == "text": self.TextFromXML(attrib)

    def PathFromXML(self, attribs):
        self.stroke_width = float(attribs["stroke-width"])
        self.stroke = attribs["stroke"]
        strs = attribs["class"].split(" ")
        self.fromWho = strs[0]
        if (len(strs) == 1):
            self.toWhom = strs[0] # A self-reply
        else:
            self.toWhom = strs[1]

        d_strs = attribs["d"].split(" ")

        state = "start"
        counter = 0
        for s in d_strs:
            coords = s.split(",")
            #print "\"" + s + "\"", state
            if state=="start":
                if s=="M": 
                    state="M"
                elif s=="L":
                    state="L"
                elif s=="C":
                    state="C"
                    counter=3
                else:
                    s=None
            else:
                for c in range(0, len(coords)):
                    coords[c] = float(coords[c])
                if state=="M":
                    self.move_to = coords
                    state = "start"
                elif state=="L":
                    self.line_to = coords
                    state = "start"
                elif state=="C": # Bezier curves are a special case
                    if counter == 3:
                        self.Bezier = list()
                    self.Bezier.append(coords)
                    counter -= 1;
                    if counter == 0: 
                        state=="start"
        try:
            self.Bezier
        except AttributeError:
            self.isBezier = False
        else:
            self.isBezier = True
                

    def PolylineFromXML(self, attribs):
        self.fill = attribs["fill"]
        strs = attribs["class"].split(" ")
        self.fromWho = strs[0]
        self.toWhom = strs[1]
        
        points = attribs["points"].split(" ")
        self.points = list()
        for p in points:
            coords = p.split(",")
            for c in range(0, 2):
                coords[c] = float(coords[c])
            self.points.append(coords)

    def CircleFromXML(self, attribs):
        self.fill = attribs["fill"]
        self.r = float(attribs["r"])
        self.x = float(attribs["cx"])
        self.y = float(attribs["cy"])
        self.xy = self.x, self.y
        self.stroke = attribs["stroke"]
        self.stroke_width = float(attribs["stroke-width"])
        self.myName = attribs["class"]

    def TextFromXML(self, attribs):
        self.fontsize = int(attribs["font-size"])
        self.x = float(attribs["x"])
        self.y = float(attribs["y"])
        self.xy = self.x, self.y
        self.fill = attribs["fill"]
        self.text = attribs["text"]
        self.myName = attribs["text"] # myName and text should be the same in most cases
        self.fontFamily = attribs["font-family"]

class Viewbox:
    def __init__(self, viewboxStr):
        strs = viewboxStr.split(" ")
        self.attributes = list()
        for s in strs:
            self.attributes.append(int(s))
        self.startX = self.attributes[0]
        self.startY = self.attributes[1]
        self.relwidth = self.attributes[2]
        self.relheight = self.attributes[3]

class SVGHeader:
    def __init__(self, width, height, viewbox):
        self.w = int(width)
        self.h = int(height)
        self.viewbox = Viewbox(viewbox)

def getNamespace(rootTag):
    m = re.match(r'{(.*)}', rootTag)
    return m.group(1)

def readSVG(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    SVGElements = list()

    namespaceSize = len(getNamespace(root.tag)) + 2
    output = ""

    svgattribs = root.attrib
    Header = SVGHeader(svgattribs["width"][:-2], svgattribs["height"][:-2], svgattribs["viewBox"])

    for child in root:
        for element in child:
            elementID = child.attrib["id"]
            if elementID == "node-labels":
                attributes = dict(element.attrib)
                text = element.text
                attributes["text"] = text.strip()
                SVGElements.append(SVGElement("text", attributes))
            elif elementID == "edges":
                SVGElements.append(SVGElement("path", element.attrib))
            elif elementID == "arrows":
                SVGElements.append(SVGElement("polyline", element.attrib))
            elif elementID == "nodes":
                SVGElements.append(SVGElement("circle", element.attrib))
            else:
                print "Unknown ID: %s" % (elementID)

    return Header, SVGElements
