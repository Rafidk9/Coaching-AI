# Prompt the person for their name, date of class, and topic of the class
 
import mysql.connector

# Establish a database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="72117577",
    database="dummydata"
)

# Create a cursor object
mycursor = mydb.cursor()

# Rest of your code (SQL queries, execution, and commits) here...




name = input("What is your name? ")
date = input("What is the date of the class? ")
topic = input("What is the topic of the class? ")

# Mark "recordings given" to the person's name in the database
sql = "UPDATE recordings SET recordings_given = True WHERE name = %s AND date = %s AND topic = %s"
val = (name, date, topic)
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "recordings given to", name)

import datetime

# Restrict access to recordings after exactly one week
one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
sql = "UPDATE recordings SET recordings_given = False WHERE recordings_given = True AND date < %s"
val = (one_week_ago,)
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "recordings access restricted")