import csv
import subprocess
import mysql.connector
import datetime 
import fun_api as fa
import time 

cnx = mysql.connector.connect(
     host='localhost',  # Replace with the actual hostname
     user='root',  # Replace with your MySQL username
     password='Qnb1234.',  # Replace with your MySQL password
     database='milebix'  # Replace with the name of your MySQL database
)
x=datetime.datetime.now()
print (str(x)+" :connexion a la base reussite")
#addr=fa.get_address()
#url=fa.get_url()
with open('data.csv', 'r') as csvfile:
     reader1 = csv.DictReader(csvfile)
     for row in reader1 :
         url='http://'+row["url"]+'/zabbix/api_jsonrpc.php'
         addr=row["address"]
key=fa.zabbix_connect(url)
name=fa.get_name(key,url)
Id=fa.Id_detecter(key,url)
command = '$User="qnbts-video\\oussema";$PWord = ConvertTo-SecureString -String "your_password" -AsPlainText -Force;$Credential = New-Object -TypeName "System.Management.Automation.PSCredential" -ArgumentList $User, $PWord;Connect-ManagementServer -server  127.0.0.1 -Credential $Credential; Get-VmsCameraReport | Export-Csv -Path "test.csv" -NoTypeInformation'
while(True): 
 subprocess.run(['powershell.exe', '-Command', command])
 data = dict()
 x=datetime.datetime.now()
 datetime_string=x.strftime("%Y%m%d%H%M%S")
 sql1="select Id from zabbix_iteam"
 cursor=cnx.cursor()
 cursor.execute(sql1)
 rows =cursor.fetchall()
 L=list()
 for row in rows :
     L.append(row[0])
 cursor.close()
 with open('test.csv', 'r') as csvfile:
     reader = csv.DictReader(csvfile)
     x=datetime.datetime.now()
     for row in reader:
         data={"Id":row['Id'],"Name":row['Name'],"Enabled":row['Enabled'],"State":row['State'],"ErrorNoConnection":row['ErrorNoConnection'],"HardwareName":row['HardwareName'],"HardwareId":row['HardwareId'],"Model":row['Model'],"Address":row['Address'],"MAC":row['MAC'],"RecorderName":row['RecorderName'],"RecorderUri":row['RecorderUri'],"RecorderId":row['RecorderId'],"ConfiguredRecordedFPS":row['ConfiguredRecordedFPS'],"PercentRecordedOneWeek":row['PercentRecordedOneWeek'],"UsedSpaceInGB":row['UsedSpaceInGB'],"Date":x}
         if(data["Id"] in L):
             sql2="update zabbix_iteam SET Name ='"+ data['Name']+"',Enabled ='"+ data["Enabled"]+"',State ='"+ data["State"] + "',ErrorNoConnection ='"+ data["ErrorNoConnection"]+"',HardwareName='"+data["HardwareName"]+"',HardwareId='"+data["HardwareId"]+"',Model='"+data["Model"]+"',Address='"+data["Address"]+"',MAC='"+data["MAC"]+"',RecorderName='"+data["RecorderName"]+"',RecorderUri='"+data["RecorderUri"]+"',RecorderId='"+data["RecorderId"]+"',ConfiguredRecordedFPS='"+data["ConfiguredRecordedFPS"]+"',PercentRecordedOneWeek='"+data["PercentRecordedOneWeek"]+"',UsedSpaceInGB='"+data["UsedSpaceInGB"]+"',Date='"+str(data["Date"])+"'" + "where Id ='"+data["Id"]+"'"
             cursor=cnx.cursor()
             cursor.execute(sql2)
             cnx.commit()
             cursor.close()
             x=datetime.datetime.now()
             print(str(x)+":mise a jour a la base ")
         else :
             sql2="insert into zabbix_iteam (Id,Name,Enabled,State,ErrorNoConnection,HardwareName,HardwareId,Model,Address,MAC,RecorderName,RecorderUri,RecorderId,ConfiguredRecordedFPS,PercentRecordedOneWeek,UsedSpaceInGB,Date) Values('"+ data['Id']+"','"+ data["Name"]+"','"+data["Enabled"]+"','"+ data["State"] + "','"+ data["ErrorNoConnection"]+"','"+data["HardwareName"]+"','"+data["HardwareId"]+"','"+data["Model"]+"','"+data["Address"]+"','"+data["MAC"]+"','"+data["RecorderName"]+"','"+data["RecorderUri"]+"','"+data["RecorderId"]+"','"+data["ConfiguredRecordedFPS"]+"','"+data["PercentRecordedOneWeek"]+"','"+data["UsedSpaceInGB"]+"','"+str(data["Date"])+"')"
             cursor=cnx.cursor()
             cursor.execute(sql2)
             fa.add_items(key,Id,data,url,name)
             cnx.commit()
             cursor.close()
             x=datetime.datetime.now()
             print(str(x)+":creation de l'id")
 print("attendre 1 min" )
 time.sleep(60)
