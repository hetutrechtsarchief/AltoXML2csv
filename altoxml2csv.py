#!/usr/bin/env python3
import sys,csv,argparse,codecs,re
import xml.etree.ElementTree as ET 

tags = []

def main(): 
  writer = csv.DictWriter(sys.stdout, fieldnames=["image","imageWidth","imageHeight","id","text","x","y","width","height","confidence"], quoting=csv.QUOTE_NONNUMERIC)
  writer.writeheader()
    
  for filename in sys.argv[1:]:
    with open(filename) as file:

      xmlstring = file.read()
      xmlstring = re.sub(r'\sxmlns="[^"]+"', '', xmlstring, count=1)
      xml = ET.fromstring(xmlstring) 
      items = []

      image = filename.replace("_alto.xml",".jpg").rpartition("/")[-1]

      imageWidth = xml.find(".//Page").attrib["WIDTH"]
      imageHeight = xml.find(".//Page").attrib["HEIGHT"]

      for textline in xml.findall('.//TextLine/String'): # recursive findall with XPath to also allow TextLines within tables

        item = {}

        item["id"] = ""

        item["image"] = image
        item["imageWidth"] = int(imageWidth)
        item["imageHeight"] = int(imageHeight)

        text = textline.attrib["CONTENT"]
       
        item["text"] = text   #text.text if text!=None else ""

        item["x"] = int(textline.attrib["HPOS"])
        item["y"] = int(textline.attrib["VPOS"])
        item["width"] = int(textline.attrib["WIDTH"])
        item["height"] = int(textline.attrib["HEIGHT"])
        item["confidence"] = round(float(textline.attrib["WC"]),2)

        writer.writerow(item)

class BoundingBox(object):
    """
    A 2D bounding box
    """
    def __init__(self, points):
        if len(points) == 0:
            raise ValueError("Can't compute bounding box of empty list")
        self.minx, self.miny = float("inf"), float("inf")
        self.maxx, self.maxy = float("-inf"), float("-inf")
        for x, y in points:
            self.minx = min(x,self.minx)
            self.maxx = max(x,self.maxx)
            self.miny = min(y,self.miny)
            self.maxy = max(y,self.maxy)

    @property
    def width(self):
        return self.maxx - self.minx
    @property
    def height(self):
        return self.maxy - self.miny
    def __repr__(self):
        return "BoundingBox(minX={}, minY={}, maxX={}, maxY={})".format(
            self.minx, self.miny, self.maxx, self.maxy)


if __name__ == "__main__": 
  main() 
