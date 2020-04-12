import config 
import pyodbc

server = config.sql_server #'<server>.database.windows.net'
database = config.sql_db #'<database>'
username = config.sql_username #'<username>'
password = config.sql_password #'<password>'
driver= '{ODBC Driver 17 for SQL Server}'

cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

# need to commit when modify table
# cursor.execute("insert into dbo.sample(id, temp) values (2, 34);")
# cnxn.commit()

cursor.execute("SELECT TOP 20 * FROM dbo.sample")
row = cursor.fetchone()

while row:
    print (str(row[0]) + " " + str(row[1]))
    row = cursor.fetchone()