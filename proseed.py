import json
enc = 'utf8'
fp = open('KnuStudents_short.json','r', encoding = enc)
knu = json.load(fp)
fp.close()
names = {}
for student in knu:
	name = student["Name"]
	last_name = name.split(maxsplit=1)[0]
	if last_name in names:
		names[last_name] += 1
	else:
		names[last_name] = 1
values = list(names.values())
values = sorted(values, reverse = True)
print(len(values))
famous = [(key, names[key]) for key in names.keys() if names[key] > 30]
sorted(famous, reverse = False, key=lambda student: student[1])
print(famous)
