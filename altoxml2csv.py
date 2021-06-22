#!/usr/bin/env python3
import sys,csv,argparse,codecs,re
import xml.etree.ElementTree as ET 

columns = ["image","imageWidth","imageHeight","id","text","x","y","width","height","confidence"]
writer = csv.DictWriter(sys.stdout, fieldnames=columns, quoting=csv.QUOTE_NONNUMERIC)
writer.writeheader()

for filename in sys.argv[1:]:
  with open(filename) as file:

    xmlstring = file.read()
    xmlstring = re.sub(r'\sxmlns="[^"]+"', '', xmlstring, count=1)
    xml = ET.fromstring(xmlstring) 
    
    image = filename.replace("_alto.xml",".jpg").rpartition("/")[-1] # extract image filename without path
    imageWidth = int(xml.find(".//Page").attrib["WIDTH"])
    imageHeight = int(xml.find(".//Page").attrib["HEIGHT"])

    for textline in xml.findall('.//TextLine/String'): # recursive findall with XPath to also allow TextLines within tables

      item = {}
      item["id"] = ""
      item["image"] = image
      item["imageWidth"] = imageWidth
      item["imageHeight"] = imageHeight
      item["text"] = textline.attrib["CONTENT"]
      item["x"] = int(textline.attrib["HPOS"])
      item["y"] = int(textline.attrib["VPOS"])
      item["width"] = int(textline.attrib["WIDTH"])
      item["height"] = int(textline.attrib["HEIGHT"])
      item["confidence"] = round(float(textline.attrib["WC"]),2)

      writer.writerow(item)

