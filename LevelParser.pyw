#-----------------------------------------------------------------
#GenerateDefaultLevel generates a default map for the thing to use
#-----------------------------------------------------------------
#FindElement works by finding elements in the xml file and returning
#the x and y coordinates, the type and the boolean of Solid.
#-----------------------------------------------------------------

import xml.etree.ElementTree as ET
import xml.dom.minidom as MD

tile_properties = '''<root><x>{0}</x><y>{1}</y><type>{2}</type><solid>{3!s}</solid></root>'''
sprite_properties = '''<root><x>{0}</x><y>{1}</y><type>{2}</type></root>'''

class GameLevel:
    def __init__(self,directory):
        self.directory = directory
        try:
            with open(self.directory):
                print("File exists")
        except IOError:
            print("Error opening " + str(self.directory))
            self.GenerateDefaultLevel()
        try:
            self.levelTree = ET.parse(self.directory)
            print("File successfully parsed")
        except ET.ParseError:
            print("An error has occurred")

    def GetData(self,El_first):
        root = self.levelTree.getroot()
        group = []
        x = -1
        y = -1
        t = -1
        s = -1
        for element in root.iter(El_first):
            try:
                width = element.find("width").text
                height = element.find("height").text
                group.append((width,height))
            except AttributeError:
                try:
                    x = element.find('x').text
                except AttributeError:
                    x = -1
                try:
                    y = element.find('y').text
                except AttributeError:
                    y = -1
                try:
                    t = element.find('type').text
                except AttributeError:
                    t = -1
                try:
                    s = element.find('solid').text
                except AttributeError:
                    s = -1
                group.append((x,y,t,s))
        return group
    
    def GenerateDefaultLevel(self):
        level = ET.Element('Main_Level')
        level_map = ET.SubElement(level,'Map')
        level_sprites = ET.SubElement(level,'Sprites')

        tiles_child = ET.SubElement(level_map,'Tile')
        tiles_child.set('id','0')
        tiles_child.extend(ET.XML(tile_properties.format(100,100,1,"True")))

        sprites_child = ET.SubElement(level_sprites,'Sprite')
        sprites_child.set('id','0')
        sprites_child.extend(ET.XML(sprite_properties.format(100,50,0)))

        file = open(self.directory,'w')
        file.write(self.GenerateIndentationForXML(level))

    def GenerateIndentationForXML(self,element):
        rough_string = ET.tostring(element,'utf-8')
        reparsed = MD.parseString(rough_string)
        return reparsed.toprettyxml(indent="    ")
