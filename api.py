from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, db
import json
import pyrebase

with open('serviceAccountKey.json', 'r') as file:
	config = json.load(file)
	cred = credentials.Certificate("serviceAccountKey.json")
	firebase_admin.initialize_app(cred, {"databaseURL": config['databaseURL']})
	firebase = pyrebase.initialize_app(config)
	auth = firebase.auth()

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=['*'],
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*']
)

def isTokenExpired():
	return False

"""
STUDENT

sid: int
name: str
years: dict[ year_id ]
"""
@app.get('/user')
@isTokenExpired
async def get_user():
	user = auth.sign_in_with_email_and_password('test2@email.com', 'Password123!')
	return user

@app.post('/user')
async def create_user():
	user = auth.create_user_with_email_and_password('test2@email.com', 'Password123!')
	auth.update_profile(user['idToken'],display_name='test')
	return user

@app.get('/{id}')
async def get_student(id:int):
	ref = db.reference(f'/{id}')
	result = ref.get()
	return result

@app.post('/{id}')
async def post_student(id:int, 
					   name:str):
	ref = db.reference(f'/{id}')
	ref.set({
		"name": name
	})
	return f"success - OK"

@app.delete('/{id}')
async def delete_student(id:int):
	ref = db.reference(f'/{id}')
	ref.delete()
	return f"success - OK"


"""
YEAR

year: int
semesters: dict[ semester_id ]
"""
@app.get('/{id}/{year}')
async def get_year(id:int, 
				   year:int):
	ref = db.reference(f'/{id}/years/{year}')
	result = ref.get()
	return result

@app.delete('/{id}/{year}')
async def delete_year(id:int, 
					  year:int):
	ref = db.reference(f'/{id}/years/{year}')
	ref.delete()
	return f"success - OK"



"""
SEMESTER

semester_id: str
courses: dict[ course_id ]
"""
@app.get('/{id}/{year}/{semester}')
async def get_semester(id:int, 
					   year:int, 
					   semester:str):
	ref = db.reference(f'/{id}/years/{year}/semesters/{semester}')
	result = ref.get()
	return result

@app.delete('/{id}/{year}/{semester}')
async def delete_semester(id:int, 
						  year:int, 
						  semester:str):
	ref = db.reference(f'/{id}/years/{year}/semesters/{semester}')
	ref.delete()
	return f"success - OK"



"""
COURSE

course: str		ex: CSCI-3333
hours: int
name: str
grade: float
isUpdated: bool
weights: dict[ weight_id ]
assignment: dict[ assignment_id ]
"""
@app.get('/{id}/{year}/{semester}/{course}')
async def get_course(id:int, 
					 year:int, 
					 semester:str, 
					 course:str):
	ref = db.reference(f'/{id}/years/{year}/semesters/{semester}/courses/{course}')
	result = ref.get()
	return result

@app.post('/{id}/{year}/{semester}/{course}')
async def post_course(id:int, 
					  year:int, 
					  semester:str, 
					  course:str, 
					  name:str, 
					  hours:int=3, 
					  grade:float=None, 
					  isUpdated:bool=False):
	ref = db.reference(f'/{id}/years/{year}/semesters/{semester}/courses/{course}')
	ref.set({
		'name': name,
		'hours': hours,
		'grade': grade,
		'isUpdated': isUpdated,
	})
	return "success - OK"

@app.delete('/{id}/{year}/{semester}/{course}')
async def delete_course(id:int, 
						year:int, 
						semester:str, 
						course:str):
	ref = db.reference(f'/{id}/years/{year}/semesters/{semester}/courses/{course}')
	ref.delete()
	return f"success - OK"



"""
ASSIGNMENT

name: str
category: str
grade: float
points: float
date: str

/student/year/semester/course/assignment
"""
@app.get('/{id}/{year}/{semester}/{course}/{assignment}')
async def get_assignment(id:int, 
						 year:int, 
						 semester:str, 
						 course:str, 
						 assignment:str):
	ref = db.reference(f'/{id}/years/{year}/semesters/{semester}/courses/{course}/assignments/{assignment}')
	result = ref.get()
	return result
	
@app.post('/{id}/{year}/{semester}/{course}/{assignment}')
async def post_assignment(id:int, 
						  year:int, 
						  semester:str, 
						  course:str, 
						  assignment:str,
						  name:str,
						  category:str,
						  grade:float=None,
						  points:float=None,
						  date:str=None):
	ref = db.reference(f'/{id}/years/{year}/semesters/{semester}/courses/{course}/assignments/{assignment}')
	ref.set({
		"name": name,
		"category": category,
		"grade": grade,
		"points": points,
		"date": date,
	})
	return "success - OK"

@app.delete('/{id}/{year}/{semester}/{course}/{assignment}')
async def delete_assignment(id:int, 
							year:int, 
							semester:str, 
							course:str, 
							assignment:str):
	ref = db.reference(f'/{id}/years/{year}/semesters/{semester}/courses/{course}/assignments/{assignment}')
	ref.delete()
	return f"success - OK"



"""
WEIGHT

category: str
weight: float
"""
@app.get('/{id}/{year}/{semester}/{course}/{category}')
async def get_weight(id:int, 
					 year:int, 
					 semester:str, 
					 course:str, 
					 category:str):
	ref = db.reference(f'/{id}/years/{year}/semesters/{semester}/courses/{course}/weights/{category}')
	result = ref.get()
	return result
	
@app.post('/{id}/{year}/{semester}/{course}/{category}')
async def post_weight(id:int, 
					  year:int, 
					  semester:str, 
					  course:str, 
					  category:str,
					  weight:float):
	ref = db.reference(f'/{id}/years/{year}/semesters/{semester}/courses/{course}/weights/{category}')
	ref.set({
		"weight": weight,
	})
	return "success - OK"

@app.delete('/{id}/{year}/{semester}/{course}/{category}')
async def delete_weight(id:int, 
						year:int, 
						semester:str, 
						course:str, 
						category:str):
	ref = db.reference(f'/{id}/years/{year}/semesters/{semester}/courses/{course}/weights/{category}')
	ref.delete()
	return f"success - OK"
