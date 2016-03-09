import xml.etree.ElementTree as xml

def parse_file(filepath):
	tree = xml.parse(filepath)
	root = tree.getroot()
	if root.tag == "level":
		return [root]
	return root.findall("level")

def parse_level(level):
	grounds = []
	for groundlist in level.findall("grounds"):
		grounds = grounds + list(groundlist)
	return level.attrib["name"], grounds

def parse_coords(coords):
	litteral = coords.split(" ")
	vertices = []
	for i in litteral:
		vertices.append(float(i))
	return tuple(vertices)

def parse_ground(ground):
	properties = ground.tag
	shape = ground.attrib["type"]
	vert = parse_coords(ground.text)
	return vert, shape, properties, None, True # Animation will come, and ground disabling too.
