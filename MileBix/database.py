import pyodbc

# Informations de connexion
server = '192.168.0.168'
database = 'database_test'
username = 'PASSWORDTS-VIDEO\\oussema'
password = 'PASSWORD1234.'

# Chaîne de connexion
connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

# Connexion au serveur SQL Server
connection = pyodbc.connect(connection_string)

