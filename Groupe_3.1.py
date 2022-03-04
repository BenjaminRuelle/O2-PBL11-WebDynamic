from flask import Flask
from flask import request
import mysql.connector
 
app = Flask(__name__ )
 
#creates instance db of class mysql.connector
#connects to the database with the credentials given in the document
db = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="1234",
	database="pbl_mia_11"
)
 
#this function is called to generate the home page of your website
@app.route('/')
def index():
	#htmlCode is some text	
	htmlCode = "Menu"
	htmlCode += "<br>"
	htmlCode += "<h1><a href='/'>Homepage</a></h1>"
	htmlCode += "<br>"
	htmlCode += "<a href='/list'>List of students</a>"
	htmlCode += "<br>"
	htmlCode += "<a href='/campus'>Campus</a>"
	htmlCode += "<br>"
	htmlCode += "<a href='/add'>Add</a>"
	htmlCode += "<br>"
	#this text is returned
	return htmlCode
 
@app.route('/list')
def list():
	
	#you must create a Cursor object
	#it will let you execute the needed query
	cur = db.cursor()
 
	#you must complete the below SQL select query
	cur.execute("SELECT campusName, studentMail, Campus_idCampus, idCampus FROM Campus, MobilityWish WHERE Campus_idCampus = idCampus")
 
	htmlCode = "<link rel='stylesheet' href='...\CSS\Home.css'>"
	htmlCode += "<body>"
	htmlCode += "<br>"
	htmlCode += "<h1><a href='/'>Homepage</a></h1>"
	htmlCode += "<br>"
	htmlCode += "<a href='/list'>List</a>"
	htmlCode += "<br>"
	htmlCode += "<a href='/campus'>Campus</a>"
	htmlCode += "<br>"
	htmlCode += "<a href='/add'>Add</a>"
	htmlCode += "<br>"
	htmlCode += "</body>"
 
	htmlCode += "<ol>"
	
	#print the first cell (or column) of all rows (or records)
	for row in cur.fetchall():
           	
		htmlCode += "<li>"
		htmlCode += str(row[1])
		htmlCode += "</li>"
		htmlCode += str(row[0])
	
	htmlCode += "</ol>"
 	
	return htmlCode

@app.route('/campus')
def campus():
	
	htmlCode = "<h1><a href='/'>Homepage</a></h1>"
	htmlCode += "<br>"
	htmlCode += "List of campus :"
	htmlCode += "<br>"
	htmlCode += "<a href='/campus_Douala'>Douala</a>"
	htmlCode += "<br>"
	htmlCode += "<a href='/campus_Kinshasa'>Kinshasa</a>"
	htmlCode += "<br>"
	htmlCode += "<a href='/campus_Nantes'>Nantes</a>"
	htmlCode += "<br>"
	htmlCode += "<a href='/campus_Lille'>Lille</a>"
	htmlCode += "<br>"
	htmlCode += "<a href='/campus_Paris'>Paris-Sénart</a>"
	htmlCode += "<br>"
	htmlCode += "<a href='/campus_Toulouse'>Toulouse</a>"
	htmlCode += "<br>"
	
	return htmlCode

@app.route('/add')
def add():
	htmlCode = "<link rel='stylesheet' href='...\CSS\Home.css'>"
	htmlCode += "<body>"
	htmlCode += "<br>"
	htmlCode += "<h1><a href='/'>Homepage</a></h1>"
	htmlCode += "<br>"
	htmlCode += "<a href='/list'>List</a>"
	htmlCode += "<br>"
	htmlCode += "<a href='/campus'>Campus: Lille</a>"
	htmlCode += "<br>"
	htmlCode += "<a href='/add'>Add</a>"
	htmlCode += "<br>"
	htmlCode += "</body>"
 
	#you must create a Cursor object
	#it will let you execute the needed query
	cur = db.cursor()
 	
	#we look for all campuses
	cur.execute("SELECT * FROM Campus")
         	
	htmlCode += "<br>"
	htmlCode += "Make a wish"
	htmlCode += "<br>"
	htmlCode += "<form action='addsave' method='GET''>"
	#start a form to let user enter data
	#action is the route/page called when the form is submitted
	#method indicates how the information is submitted to the other page (GET means through the URL)
	#observe the URL in your browser after submit, it will look like
	#http://127.0.0.1:5000/addsave?student=name%40icam.fr&choice=1
	#the first parameter starts with ?
	#then we have parameter1=value1
	#the second (or any subsequent parameter) starts with &
	#then we have parameter2=value2
	htmlCode += "<label>Email Address:</label>"
	htmlCode += "<br>"
	#we a have an input field of type email for the student identifier (required)
	htmlCode += "<input type='email' name='student' required>"
	htmlCode += "<br>"
    	
	htmlCode += "<label>Campus choice:</label>"
	htmlCode += "<br>"
	#we use a drop down list to select a campus
	htmlCode += "<select name='choice'>"
	
	#print the first cell (or column) of all rows (or records)
	for row in cur.fetchall():
    		#for each campus, we create an <option value=id>name</option>   	
		htmlCode += "<option value=" + str(row[0]) +">"
		htmlCode += str(row[1])
		htmlCode += "</option>"
	
	#we close the select tag
	htmlCode += "</select>"
    	
	#at the end of the form, we display a button to save the record
	htmlCode += "<br>"
	htmlCode += "<input type='submit' value='Save'>"
	#close form
	htmlCode += "</form>"
	  
	return htmlCode

#we use this route to save the form result
#we indicate that we use method GET to indicate we retrieve information from previous page
@app.route('/addsave',  methods=['GET'])
def addsave():
	htmlCode = "Menu"
	htmlCode += "<br>"
	htmlCode += "<a href='/'>Homepage</a>"
	htmlCode += "<br>"
	htmlCode += "<a href='/list'>List</a>"
	htmlCode += "<br>"
	htmlCode += "<a href='/add'>Add</a>"
	htmlCode += "<br>"
 
	#you must create a Cursor object
	#it will let you execute the needed query
	cur = db.cursor()
	
	#MobilityWish is the table
	#Campus_idCampus and studentMail are the fields in the table
	#SQL syntax is INSERT INTO table(field1, field2) VALUES('value1', 'value2')  
	sql = "INSERT INTO MobilityWish(studentMail, Campus_idCampus) VALUES (%s, %s)"
	#request.values['choice'] and request.values['student'] are input from the form by user
	val = (request.values['student'], request.values['choice'])
	#we execute an insert query
	cur.execute(sql, val)
 
	#commit = save changes in database
	db.commit()
 
	 #display the number of records added
	htmlCode += str(cur.rowcount) + " record inserted."
 	
	return htmlCode

@app.route('/campus_Douala')
def campus_Douala():

	htmlCode = "Menu"
	htmlCode += "<br>"
	htmlCode += "<a href='/'>Homepage</a>"
	htmlCode += "<br>"	
	htmlCode += "<a href='/campus'>Campus</a>"
	
	
	#you must create a Cursor object
	#it will let you execute the needed query
	cur = db.cursor()

	#we look for all campuses
       	   	
	cur.execute("SELECT campusName, studentMail from campus INNER JOIN mobilitywish ON idCampus = Campus_idCampus WHERE Campus_idCampus = 3 ORDER BY idMobilityWish")
	for row in cur.fetchall():
           	
		htmlCode += "<li>"
		htmlCode += str(row[1])
		htmlCode += "</li>"
		htmlCode += str(row[0])
	
	htmlCode += "</ol>"
 	
	return htmlCode

@app.route('/campus_Kinshasa')	
def campus_Kinshasa():

	htmlCode = "Menu"
	htmlCode += "<br>"
	htmlCode += "<a href='/'>Homepage</a>"
	htmlCode += "<br>"	
	htmlCode += "<a href='/campus'>Campus</a>"
	
	
	#you must create a Cursor object
	#it will let you execute the needed query
	cur = db.cursor()

	#we look for all campuses
       	   	
	cur.execute("SELECT campusName, studentMail from campus INNER JOIN mobilitywish ON idCampus = Campus_idCampus WHERE Campus_idCampus = 4 ORDER BY idMobilityWish")
	for row in cur.fetchall():
           	
		htmlCode += "<li>"
		htmlCode += str(row[1])
		htmlCode += "</li>"
		htmlCode += str(row[0])
	
	htmlCode += "</ol>"
 	
	return htmlCode

@app.route('/campus_Lille')	
def campus_Lille():

	htmlCode = "Menu"
	htmlCode += "<br>"
	htmlCode += "<a href='/'>Homepage</a>"
	htmlCode += "<br>"	
	htmlCode += "<a href='/campus'>Campus</a>"
	
	
	#you must create a Cursor object
	#it will let you execute the needed query
	cur = db.cursor()

	#we look for all campuses
       	   	
	cur.execute("SELECT campusName, studentMail from campus INNER JOIN mobilitywish ON idCampus = Campus_idCampus WHERE Campus_idCampus = 1 ORDER BY idMobilityWish")
	for row in cur.fetchall():
           	
		htmlCode += "<li>"
		htmlCode += str(row[1])
		htmlCode += "</li>"
		htmlCode += str(row[0])
	
	htmlCode += "</ol>"
 	
	return htmlCode

@app.route('/campus_Nantes')	
def campus_Nantes():

	htmlCode = "Menu"
	htmlCode += "<br>"
	htmlCode += "<a href='/'>Homepage</a>"
	htmlCode += "<br>"	
	htmlCode += "<a href='/campus'>Campus</a>"
	
	
	#you must create a Cursor object
	#it will let you execute the needed query
	cur = db.cursor()

	#we look for all campuses
       	   	
	cur.execute("SELECT campusName, studentMail from campus INNER JOIN mobilitywish ON idCampus = Campus_idCampus WHERE Campus_idCampus =  2 ORDER BY idMobilityWish")
	for row in cur.fetchall():
           	
		htmlCode += "<li>"
		htmlCode += str(row[1])
		htmlCode += "</li>"
		htmlCode += str(row[0])
	
	htmlCode += "</ol>"
 	
	return htmlCode

@app.route('/campus_Paris')	
def campus_Paris():

	htmlCode = "Menu"
	htmlCode += "<br>"
	htmlCode += "<a href='/'>Homepage</a>"
	htmlCode += "<br>"	
	htmlCode += "<a href='/campus'>Campus</a>"
	
	
	#you must create a Cursor object
	#it will let you execute the needed query
	cur = db.cursor()

	#we look for all campuses
       	   	
	cur.execute("SELECT campusName, studentMail from campus INNER JOIN mobilitywish ON idCampus = Campus_idCampus WHERE Campus_idCampus = 6 ORDER BY idMobilityWish")
	for row in cur.fetchall():
           	
		htmlCode += "<li>"
		htmlCode += str(row[1])
		htmlCode += "</li>"
		htmlCode += str(row[0])
	
	htmlCode += "</ol>"
 	
	return htmlCode

@app.route('/campus_Toulouse')	
def campus_Toulouse():

	htmlCode = "Menu"
	htmlCode += "<br>"
	htmlCode += "<a href='/'>Homepage</a>"
	htmlCode += "<br>"	
	htmlCode += "<a href='/campus'>Campus</a>"
	
	
	#you must create a Cursor object
	#it will let you execute the needed query
	cur = db.cursor()

	#we look for all campuses
       	   	
	cur.execute("SELECT campusName, studentMail from campus INNER JOIN mobilitywish ON idCampus = Campus_idCampus WHERE Campus_idCampus = 5 ORDER BY idMobilityWish")
	for row in cur.fetchall():
           	
		htmlCode += "<li>"
		htmlCode += str(row[1])
		htmlCode += "</li>"
		htmlCode += str(row[0])
	
	htmlCode += "</ol>"
 	
	return htmlCode
if __name__ == '__main__':
        app.run()