import requests
import json

groupsByFacultyAndCourse = 'https://student.triton.univ.kiev.ua/Registration/GroupsByFacultyAndCourse'
studentsByGroup = 'https://student.triton.univ.kiev.ua/Registration/StudentsByGroup'

#read data about faculties and groups
fp = open('FacultyId.json','r')
facultyId = json.load(fp)
fp.close()
fp = open('CourseId.json','r')
courseId = json.load(fp)
fp.close()

facultyKeys = facultyId.keys()
courseKeys = courseId.keys()

requestsSession = requests.session()

id1 = '4' # Faculty ID
id2 = '2' # Course  ID
groupsJSON = requestsSession.get(groupsByFacultyAndCourse, params = {'id1' : id1, 'id2' : id2}).json()
#delete item with value "-1"
del groupsJSON[0] 

knuStudents = []
for group in groupsJSON:
	# let's get list of students for each group
	rawStudentsJSON = requestsSession.get(studentsByGroup, params = {'id' : group['Value']}).json()
	del rawStudentsJSON[0]
	# delete unnessesary fields in JSON
	studentsJSON = [{"Text": student["Text"], "Value" : student["Value"]} for student in rawStudentsJSON]
	knuStudents += studentsJSON

fp = open('knuStudents.json', 'w', encoding = 'utf8')
json.dump(knuStudents, fp, ensure_ascii = False, indent = 4)
fp.close()


"""
#dump json for debug
fp = open('out1.json', 'w', encoding = 'utf8')
json.dump(answerJSON, fp, ensure_ascii = False, indent = 4)
fp.close()
"""