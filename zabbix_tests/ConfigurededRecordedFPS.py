import mysql.connector
import sys 
cnx = mysql.connector.connect(
    host='127.0.0.1',  # Replace with the actual hostname
    user='root',  # Replace with your MySQL username
    password='password',  # Replace with your MySQL password
    database='Milebix'  # Replace with the name of your MySQL database
)
sql2="select ConfiguredRecordedFPS from zabbix_iteam where Id='"+ sys.argv[1]+"'"
cursor= cnx.cursor()
cursor.execute(sql2)
rows=cursor.fetchall()
for row in rows :
    print(int(row[0]))
cursor.close()
cnx.close()
