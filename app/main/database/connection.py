import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="myusername",
    password="mypassword",
    database="crmintegrations",
)

cursor = mydb.cursor()

cursor.execute("CREATE DATABASE crmintegrations")
