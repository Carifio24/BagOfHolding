import sys
import json

def chars_to_school(ch):
	if ch == "A":
		return "Abjuration"
	if ch == "C":
		return "Conjuration"
	if ch == "D":
		return "Divination"
	if ch == "EV":
		return "Evocation"
	if ch == "I":
		return "Illusion"
	if ch == "N":
		return "Necromancy"
	if ch == "T":
		return "Transmutation"

def parse_components(components_string):
	components = components_string.replace(")", "").split("(")
	if len(components) == 1:
		material = ""
	else:
		material = components[1]
		material = material[0].upper() + material[1:] + "."

	components = components[0].strip().split(",")
	return components, material



# Get the XGE spell data JSON
fname = "XGESpells.json"
f = open(fname)
xgedata = f.read()
f.close()

# Class names to remove
classes_to_remove = ["Fighter (Eldritch Knight)", "Rogue (Arcane Trickster)"]

# The container for the converted data
converted_data = []

# Read through the documents and convert each one to the new list
xgedata = json.loads(xgedata)
spells = xgedata["spell"]
for s in spells:
	snew = {}
	snew["level"] = s["level"]
	snew["school"] = {"name" : chars_to_school(s["school"])}
	snew["casting_time"] = s["time"]
	snew["range"] = s["range"]
	duration_text = s["duration"]
	if duration_text.startswith("Concentration"):
		snew["duration"] = True
		duration_text = duration_text[len("Concentration, "):]
		duration_text = duration_text[0].upper() + duration_text[1:]
	else:
		snew["duration"] = False
	snew["duration"] = duration_text
	classes = s["classes"]
	classes = classes.strip()
	classes = classes.replace("Rogue (Arcane Tricksster),", "")
	classes = classes.replace("Fighter (Eldritch Knight),", "")
	classes = classes.split(",")
	snew["classes"] = [ {"name" : cname} for cname in classes ]
	components_text = s["components"]
	components, material = parse_components(components_text)
	snew["components"] = components
	if material != "":
		snew["material"] = material
	description_text = s["text"][:-2] # Cut out the ending null and "This spell can be found..."
	description_text = [w for w in description_text if w is not None]
	description = []
	higher_level = ""
	for t in description_text:
		if t.startswith("At Higher Levels: "):
			higher_level = t[len("At Higher Levels: "):]
		else:
			description.append(t)
	snew["desc"] = description
	if higher_level != "":
		snew["higher_level"] = [higher_level]
	if "ritual" in s.keys() and s["ritual"] == "YES":
		snew["ritual"] = "yes"
	classes_list = s["classes"].split(", ")
	snew["classes"] = [x for x in classes_list if x not in classes_to_remove]

	# Write to the file
	converted_data.append(snew)


# Write to  file
outfile = "XGESpells_converted.json"
with open(outfile, 'w') as f:
	f.write("[\n")
	for x in converted_data:
		s = str(x).replace("\'", "\"")
		f.write("\t%s\n" % s)
	f.write("]\n")
