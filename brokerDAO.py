# brokerDAO
# DAO contains the functions that will be used by the Application to interact with the Database

import mysql.connector
import config as cfg
class BrokerDAO:
    connection=""
    cursor =''
    host=       ''
    user=       ''
    password=   ''
    database=   ''
    
    def __init__(self):
        self.host=       cfg.mysql['host']
        self.user=       cfg.mysql['user']
        self.password=   cfg.mysql['password']
        self.database=   cfg.mysql['database']

    def getcursor(self): 
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password,
            database=   self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        self.connection.close()
        self.cursor.close()
         
    def getAll(self):
        cursor = self.getcursor()
        sql="SELECT * FROM broker_info"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        #print(results)
        for result in results:
            returnArray.append(self.convertToDictionary(result))
        return returnArray
            

        self.closeAll()
        return returnArray

    def findByID(self, ID):
        cursor = self.getcursor()
        sql="select * from broker_info where ID = %s"
        values = (ID,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def create(self, broker):
        cursor = self.getcursor()
        sql="insert into broker_info (Name, Address, County, Phone, Web) values (%s,%s,%s,%s,%s)"
        values = (broker.get("Name"), broker.get("Address"), broker.get("County"), broker.get("Phone"), broker.get("Web"))
        cursor.execute(sql, values)

        self.connection.commit()
        newID = cursor.lastrowid
        broker["ID"] = newID
        self.closeAll()
        return broker


    def update(self, ID, broker):
        cursor = self.getcursor()
        sql="update broker_info set Name= %s, Address=%s, County=%s, Phone=%s, Web=%s where ID = %s"
        print(f"update broker_info {broker}")
        values = (broker.get("Name"), broker.get("Address"), broker.get("County"), broker.get("Phone"), broker.get("Web"), ID) #passing in the values to the above sql query
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        
    def delete(self, ID):
        cursor = self.getcursor()
        sql="delete from broker_info where ID = %s"
        values = (ID,)

        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll()
        
        print("delete done")

    
    
    def findByCounty(self, county):
        cursor = self.getcursor()
        sql="SELECT * FROM broker_info Where County = %s"
        values = (county,)

        cursor.execute(sql, values)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            returnArray.append(self.convertToDictionary(result))
        return returnArray
    
    def convertToDictionary(self, resultLine):
        attkeys=['ID', 'Name', 'Address','County', 'Phone', 'Web']
        broker = {}
        currentkey = 0
        for attrib in resultLine:
            broker[attkeys[currentkey]] = attrib
            currentkey = currentkey + 1 
        return broker

        
brokerDAO = BrokerDAO()