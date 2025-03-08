import xml.etree.cElementTree as ET
import re

with open("SAP_20190122201654_utility.xml") as f:
    xml = f.read()
tree = ET.fromstring(re.sub(r"(<\?xml[^>]+\?>)", r"\1<root>", xml) + "</root>")