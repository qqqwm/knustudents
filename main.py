import requests

mainUrl = 'https://student.triton.univ.kiev.ua/Registration'
groupsByFacultyAndCourse = '/GroupsByFacultyAndCourse?id1=1&id2=2'
studentsByGroup = '/StudentsByGroup?id='

requestsSession = requests.session()
