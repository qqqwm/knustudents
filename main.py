import requests
import json

groupsByFacultyAndCourse = 'https://student.triton.univ.kiev.ua/Registration/GroupsByFacultyAndCourse'
studentsByGroup = 'https://student.triton.univ.kiev.ua/Registration/StudentsByGroup'

#read data about faculties and groups
fp = open('FacultyId.json','r', encoding = 'utf8')
facultyId = json.load(fp)
fp.close()
fp = open('CourseId.json','r', encoding = 'utf8')
courseId = json.load(fp)
fp.close()

facultyKeys = facultyId.keys()
courseKeys = courseId.keys()
#get requests with possible keep-alive
requestsSession = requests.session()
#all knu students
knuStudents = []
#some requests are not permitted.(Bug in Triton system)
#add to this list 'bad' group id's
exceptionList = ['2631', '2667', '2266', '2666', '2708', '2063', '2321', '2314', '2313', '2815', '2878', '2880', '2881', '2896', '1960', '2851', '2811', '1759', '1769', '2863', '1743', '1716', '1686', '1639', '1514', '1539', '1824', '1345', '2825', '2885', '2903', '2917', '2912', '2913', '2914', '2883']

totalNumberGroups = 0

for id1 in facultyKeys:
	for id2 in courseKeys:
		groupsJSON = requestsSession.get(groupsByFacultyAndCourse, params = {"id1" : id1, "id2" : id2}).json()
		#delete item with value "-1"
		if groupsJSON[0]["Value"] == "-1":
			del groupsJSON[0]
		for group in groupsJSON:
			groupId = group["Value"]
			if groupId in exceptionList:
				continue
			# let's get list of students for each group
			page = requestsSession.get(studentsByGroup, params = {"id" : groupId})
			try:
				rawStudentsJSON = page.json()
			except ValueError:
				exceptionList.append(groupId)
				print('Add exception list')
				continue
			#delete item with value "-1"
			del rawStudentsJSON[0]
			# delete unnessesary fields in JSON
			studentsJSON = [{"Name": student["Text"], "Value" : student["Value"], "Group" : group["Text"], "GroupId" : groupId, "Course" : id2, "Faculty" : id1} for student in rawStudentsJSON]
			# add students to knu students list
			knuStudents += studentsJSON
			totalNumberGroups += 1

print(totalNumberGroups)
fp = open('knuStudents.json', 'w', encoding = 'utf8')
json.dump(knuStudents, fp, ensure_ascii = False, indent = 4)
fp.close()

fp = open('exceptionList.txt', 'w', encoding = 'utf8')
fp.write(str(exceptionList))
fp.close()
