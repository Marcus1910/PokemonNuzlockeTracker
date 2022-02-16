import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="Pokemon",
  password="/hucVS3vYwuolPNu"
)
name = "Renegade_platinum"
message = 'CREATE DATABASE ' + str(name)
mycursor = mydb.cursor()

mycursor.execute(message)