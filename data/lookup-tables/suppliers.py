import sys
sys.path.insert(0,"/usr/lib/python3/dist-packages/")
import pymysql


db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
cursor = db.cursor()
sql = "SELECT DISTINCT VendorName FROM `supplier_cm_mapping`"
cursor.execute(sql)
results = cursor.fetchall()
OutputFile = open("/home/ebromic/data/lookup-tables/suppliers.txt", "w")


for row in results:
    OutputFile.write(row[0] + "\n")
    

OutputFile.close()
cursor.close()
db.close()
sys.exit()
