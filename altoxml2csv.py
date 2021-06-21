#!/usr/bin/env python3
import sys,csv,argparse,codecs,re
import xml.etree.ElementTree as ET 

tags = []

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

