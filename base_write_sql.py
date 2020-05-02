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
# cursor.execute("insert into dbo.sample(id, temp) values (98, 33);")
# cursor.execute("insert into dbo.sample(id, temp) values (98, 333);")
a = '1970-01-01 11:11:22'
b = 'xxx'
c = 'NULL'
d = 22.9
cursor.execute(f"""insert into 
dbo.home_stat_temp(timestamp, device_name, temperature, humidity) 
values ('{a}', '{b}', {c}, {d});
""")
# cnxn.commit()

cursor.execute("SELECT TOP 20 * FROM dbo.home_stat_temp")
row = cursor.fetchone()

cursor.execute

while row:
    # print(str(row[0]) + "\t" + str(row[1]))
    row_str = '\t'.join([str(s) for s in row])
    print(row_str)
    row = cursor.fetchone()

# print('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)