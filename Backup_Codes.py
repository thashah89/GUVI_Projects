from sqlalchemy import create_engine
import pymysql
import pandas as pd

# Creating a connection to mysql to import data into database
try:
    mydb = pymysql.connect(
        host = '127.0.0.1',
        user = 'root',
        password = 'ShahulSqL2024'
    )
    print("Connection Established")
    cursor = mydb.cursor()
    cursor.execute("create database if not exists redbus")
    mydb.commit()
    print("Database created successfully")
    cursor.execute("use redbus")
    cursor.execute("drop table if exists bus_routes")

except pymysql.Error as e:
    print(f"An error occured {e}")

host = '127.0.0.1'
db = 'redbus'
user = 'root'
pw = 'ShahulSqL2024'

engine = create_engine(f"mysql+pymysql://{user}:{pw}@{host}/{db}")

file_list = ['C:\Users\Shahul_Desktop\OneDrive\Desktop\GUVI_Projects\CSV Backup\Andhra Pradesh.csv','C:\Users\Shahul_Desktop\OneDrive\Desktop\GUVI_Projects\CSV Backup\Assam.csv',
             'C:\Users\Shahul_Desktop\OneDrive\Desktop\GUVI_Projects\CSV Backup\Chandigarh.csv','C:\Users\Shahul_Desktop\OneDrive\Desktop\GUVI_Projects\CSV Backup\Haryana.csv',
             'C:\Users\Shahul_Desktop\OneDrive\Desktop\GUVI_Projects\CSV Backup\Karnataka.csv','C:\Users\Shahul_Desktop\OneDrive\Desktop\GUVI_Projects\CSV Backup\Kerala.csv',
             'C:\Users\Shahul_Desktop\OneDrive\Desktop\GUVI_Projects\CSV Backup\Punjab.csv','C:\Users\Shahul_Desktop\OneDrive\Desktop\GUVI_Projects\CSV Backup\Rajasthan.csv',
             'C:\Users\Shahul_Desktop\OneDrive\Desktop\GUVI_Projects\CSV Backup\South Bengal.csv','C:\Users\Shahul_Desktop\OneDrive\Desktop\GUVI_Projects\CSV Backup\Telangana.csv',
             'C:\Users\Shahul_Desktop\OneDrive\Desktop\GUVI_Projects\CSV Backup\Uttar Pradesh.csv','C:\Users\Shahul_Desktop\OneDrive\Desktop\GUVI_Projects\CSV Backup\West Bengal.csv'
]

for i in file_list:
    df = pd.DataFrame(pd.read_csv(i))
    df.to_sql('bus_routes',engine,if_exists='append',index=False)

cursor.execute('Alter table bus_routes add column id int auto_increment primary key')
cursor.execute('Alter table bus_routes modify column departing_time time')
cursor.execute('Alter table bus_routes modify column reaching_time time')
cursor.execute('Alter table bus_routes modify column star_rating float')
cursor.execute('Alter table bus_routes modify column price decimal')
cursor.execute('Alter table bus_routes modify column seat_availability int')