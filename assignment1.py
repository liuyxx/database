#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


import sqlite3

# Display SQLite version number
print (sqlite3.sqlite_version)

import pandas as pd
import numpy as np


# In[2]:


import plotly.express as px


# In[9]:


# Connect to the Database - the DATABASE must already exisit

conn=sqlite3.connect('D:\\onedrive_exeter\\OneDrive - University of Exeter\\database\\assignment\\assignment1.db')

# conn is an object of the Connection class - the next command is only for display
print(type(conn))

# The connection object (conn) has access to various methods of the Connection class. 
# We are using the method cursor() and which returns a cursor object.
# The cursor object is essential to perform any operation on the database (CRUD operations).
cur=conn.cursor()

# The next command is only for display
print(type(cur))


# In[10]:


# Create a new table called ECC_DEPARTMENT
# Note: If the table is created succesfully, executing the code again will lead to exception

# Once we have the cursor object, we can perform all SQL operations with the help of .execute() method

qry='''
CREATE TABLE customer (
    cus_ID INTEGER   PRIMARY KEY
                     NOT NULL,
    name   TEXT (40) NOT NULL,
    tel    TEXT (20),
    email  TEXT (40) NOT NULL,
    age    INTEGER,
    sex    TEXT
)

'''
try:
        cur.execute(qry)
        print ('Table created successfully')
except:
# If table already exists then use the SQLite console to connect to the database (BEMM459.db) and then use the drop table command.
# .. Altenatively, use the SQLiteStudio GUI to delete table ECC_DEPARTMENT and execute this code block again.
        print ('Error in creating table')
        
     


# In[11]:


qry='''
CREATE TABLE [order] (
    order_ID     INTEGER    PRIMARY KEY
                            NOT NULL,
    cost         NUMERIC    NOT NULL,
    customer_ID  INTEGER    REFERENCES customer (cus_ID) ON DELETE NO ACTION
                                                         ON UPDATE CASCADE,
    shipping_add TEXT (100) NOT NULL,
    product_ID   NOT NULL   REFERENCES product (pro_ID) ON DELETE NO ACTION
                                                        ON UPDATE CASCADE
)
WITHOUT ROWID;


'''
try:
        cur.executescript(qry)
        print ('Tables created successfully')
except:
        print ('Error in creating tables')
        
       


# In[12]:


qry='''

CREATE TABLE comment (
    comment_ID  INTEGER        PRIMARY KEY
                               NOT NULL,
    rating      INTEGER (0, 5) NOT NULL,
    reviewer_ID INTEGER        REFERENCES customer (cus_ID) ON DELETE NO ACTION
                                                            ON UPDATE CASCADE,
    product_ID  INTEGER        REFERENCES product (pro_ID) ON DELETE NO ACTION
                                                           ON UPDATE CASCADE
)
WITHOUT ROWID;
'''
try:
        cur.executescript(qry)
        print ('Tables created successfully')
except:
        print ('Error in creating tables')


# In[13]:


qry='''
CREATE TABLE product (
    pro_ID      INTEGER   PRIMARY KEY
                          NOT NULL,
    pro_name    TEXT (20) NOT NULL,
    price       NUMERIC   NOT NULL,
    customer_ID           REFERENCES customer (cus_ID) ON DELETE RESTRICT
                                                       ON UPDATE CASCADE
)
WITHOUT ROWID;


'''
try:
        cur.executescript(qry)
        print ('Tables created successfully')
except:
        print ('Error in creating tables')
        


# In[14]:


# Listing all tables in your database (suggest using SQLIte prompt and command .tables)
# Once we have the cursor object, we can perform all SQL operations with the help of execute() method.

# define a function
def tables_in_sqlite_db(conn):
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [
        v[0] for v in cursor.fetchall()
        if v[0] != "sqlite_sequence"
    ]
    cursor.close()
    return tables


# In[15]:


# call the function and pass connection object 
tables = tables_in_sqlite_db(conn)

#print tables in the current database
print(tables)


# In[16]:


# Insert multiple records in table customer

qry="insert into customer (cus_ID, name, tel,email,age,sex) values (?,?,?,?,?,?);"
customerlist=[(1,'Jack','07529981234','Jack@163.com',22,'Male'),
             (2,'Janet','07529985678','Janet@163.com',23,'Female'),
             (3,'Tom','07529989012','Tom@163.com',21,'Male'),
             (4,'Mary','07529983456','Mary@163.com',18,'Female'),
             (5,'Henry','07529987890','Henry@163.com',52,'Male'),
             (6,'Anna','07529982345','Anna@163.com',26,'Female'),
             (7,'Alex','07529986789','Alex@163.com',42,'Female'),
             (8,'Iris','07529980123','Iris@163.com',33,'Male'),
             (9,'Irem','07529984567','Irem@163.com',16,'Male'),
             (10,'Mike','07529988901','Mike@163.com',20,'Male'),
             (11,'Andy','7526854675','Andy@163.com',20,'Female'),
             (12,'Judy','7521476583','Judy@163.com',24,'Female'),
             (13,'Mark','7525214836','Mark@163.com',22,'Male'),
             (14,'Mario','7529456328','Mario@163.com',22,'Male'),
             (15,'Jack','7529984564','Jack@163.com',19,'Male'),
             (16,'John','7529989856','John@163.com',35,'Male'),
             (17,'Bob','7529988888','Bob@163.com',29,'Male'),
             (18,'Anderson','7529987541','Anderson@163.com',27,'Male'),
             (19,'Anya','7528547441','Anya@163.com',16,'Female'),
             (20,'Jenny','7529981254','Jenny@163.com',20,'Female')]
           
            

try:
        cur.executemany(qry, customerlist)
        conn.commit()
        print ('Records inserted successfully..committed')
except:
        print ('Error in insert operation..rollback')
        conn.rollback()


# In[17]:


# Insert multiple records in table order

qry="insert into [order] (order_ID, cost, customer_ID,shipping_add,product_ID) values (?,?,?,?,?);"
orderlist=[(1,30,5,'11 King Edwart Street, Exeter, EX6 7ED','2'),
             (2,40,3,'13 King Edwart Street, Exeter, EX6 7ED','1'),
             (3,70,7,'51 Rosebloom Avenue, Exeter, EX1 5RT','1,2'),
             (4,10,8,'116 Exeter High Street, Exeter, EX4 5TY','3'),
             (5,60,2,'19 Orchid Road, Exeter EX3 1GT','4'),
             (6,80,2,'19 Orchid Road, Exeter EX3 1GT','5'),
             (7,20,8,'116 Exeter High Street, Exeter, EX4 5TY','6'),
             (8,50,5,'11 King Edwart Street, Exeter, EX6 7ED','1,3'),
             (9,40,3,'13 King Edwart Street, Exeter, EX6 7ED','1'),
             (10,20,7,'51 Rosebloom Avenue, Exeter, EX1 5RT','6'),
             (11,60,11,'11 King Edwart Street, Exeter, EX6 7ED','4'),
              (12,300,12,'11 King Edwart Street, Exeter, EX6 7ED','11'),
              (13,350,13,'11 King Edwart Street, Exeter, EX6 7ED','12'),
              (14,300,14,'11 King Edwart Street, Exeter, EX6 7ED','11'),
              (15,60,13,'11 King Edwart Street, Exeter, EX6 7ED','4'),
              (16,95,15,'11 King Edwart Street, Exeter, EX6 7ED','5,13'),
              (17,300,16,'11 King Edwart Street, Exeter, EX6 7ED','11'),
              (18,55,17,'11 King Edwart Street, Exeter, EX6 7ED','1,13')]
           
            

try:
        cur.executemany(qry, orderlist)
        conn.commit()
        print ('Records inserted successfully..committed')
except:
        print ('Error in insert operation..rollback')
        conn.rollback()


# In[18]:


# Insert multiple records in table product

qry="insert into product (pro_ID, pro_name, price,customer_id) values (?,?,?,?);"
productlist=[(1,'keyboard',40,'3,5,7,17'),
             (2,'microphone',30,'5,7'),
             (3,'postcard',10,'5,8'),
             (4,'calculator',60,'2,11,13'),
             (5,'displayer',80,'2,15'),
             (6,'tableware',20,'7,8'),
             (7,'charger',10,''),
             (8,'sperker',15,''),
             (9,'heater',25,''),
             (10,'earphone',30,''),
             (11,'switch',300,'12,14,16'),
             (12,'smartphone',350,'13'),
             (13,'mouse',15,'15,17')]
           
            

try:
        cur.executemany(qry, productlist)
        conn.commit()
        print ('Records inserted successfully..committed')
except:
        print ('Error in insert operation..rollback')
        conn.rollback()


# In[19]:


# Insert multiple records in table comment

qry="insert into comment (comment_ID, rating, reviewer_ID,product_id) values (?,?,?,?);"
commentlist=[(1,5,2,4),
             (2,4,2,5),
             (3,3,3,1),
             (4,5,5,1),
             (5,2,5,2),
             (6,4,5,3),
             (7,3,7,1),
             (8,5,7,2),
             (9,4,7,6),
             (10,5,8,3),
             (11,4,8,6),
             (12,5,11,4),
             (13,5,12,11),
             (14,1,13,12),
             (15,5,14,11),
             (16,2,13,4),
             (17,2,15,5),
             (18,4,15,13),
             (19,5,16,11),
             (20,3,17,1),
             (21,4,17,13)]
           
            

try:
        cur.executemany(qry, commentlist)
        conn.commit()
        print ('Records inserted successfully..committed')
except:
        print ('Error in insert operation..rollback')
        conn.rollback()


# In[20]:


# Query and display records from the table customer (all rows)

# Prepare the query String
qry="select * from customer;"

# Execute query on SQLite
cur.execute(qry)

# Fetch and display all rows
rows=cur.fetchall()

for row in rows:
    print (row)


# In[21]:


# Query and display records from the table order (all rows)

# Prepare the query String
qry="select * from [order];"

# Execute query on SQLite
cur.execute(qry)

# Fetch and display all rows
rows=cur.fetchall()

for row in rows:
    print (row)


# In[22]:


# Query and display records from the table product (all rows)

# Prepare the query String
qry="select * from product;"

# Execute query on SQLite
cur.execute(qry)

# Fetch and display all rows
rows=cur.fetchall()

for row in rows:
    print (row)


# In[23]:


# Query and display records from the table comment (all rows)

# Prepare the query String
qry="select * from comment;"

# Execute query on SQLite
cur.execute(qry)

# Fetch and display all rows
rows=cur.fetchall()

for row in rows:
    print (row)


# In[ ]:





# In[24]:


# Creating databse dump ... we are connected to assignment.db
# If conn object is closed then uncomment the next line and execute code



file=open('D:\\onedrive_exeter\\OneDrive - University of Exeter\\database\\assignment\\assignment1_backup.sql','w')

for line in conn.iterdump():
        file.write('{}\n'.format(line))
        
file.close()

# Closing database connection
# conn.close()


# In[28]:


# Creating new database, reading content of the dump file and executing SQL statements in it using cursor object's executescript() method

connRestore=sqlite3.connect('D:\\onedrive_exeter\\OneDrive - University of Exeter\\database\\assignment\\assignment1_backup.db')

file=open('D:\\onedrive_exeter\\OneDrive - University of Exeter\\database\\assignment\\assignment1_backup.sql','r')
qry=file.read()
file.close()

curRestore=connRestore.cursor()
curRestore.executescript(qry)

# call function (defined earlier) and pass connection object 
tables = tables_in_sqlite_db(connRestore)

#print tables in the newly restored database
print(tables)

connRestore.close()


# In[29]:


# Close database connection to assignment.db
#conn.close()


# In[31]:


pip install pymongo


# In[43]:


from pymongo import MongoClient  #导入模块
mongoclient=MongoClient('localhost',27017) #获取连接


# In[44]:


#Check what databases exist - the output is a list of database names
print(mongoclient.list_database_names())

#You can also check databases that presently exisit using a loop
dblist = mongoclient.list_database_names()
for x in dblist:
    print(x) 


# In[45]:


#Defining a user function to check if database exists - In MongoDB, a database is not created until it gets content. 
def check_DatabaseExists(argDBName):
    local_dblist = mongoclient.list_database_names()
    if argDBName in local_dblist:
        print("The database ", argDBName, " exists.")
    else:
        print("The database ", argDBName, " does not exist.")

#Defining a user function to check if a collection exists - In MongoDB, a collection is not created until it gets content. 
def check_CollectionExists(argDBName, argCollName, local_mydb):
    local_mydb = mongoclient[argDBName]
    local_collist = local_mydb.list_collection_names()
    if argCollName in local_collist:
        print("The collection ",  argCollName, "exists in database ", argDBName)
    else:
        print("The collection ", argCollName, " does not exist in database ", argDBName)


# In[46]:


#Create a new database       
mydb = mongoclient["assignment1"]
print(type(mydb))

#Check if database exists by calling function check_DatabaseExists with name of database as the arguement
check_DatabaseExists("assignment1")

'''
#Without a function the code will be as follows
if "Database_BEMM459_Pymongo" in dblist:
    print("The database 'Database_BEMM459_Pymongo' exists.")
else:
    print("The database 'Database_BEMM459_Pymongo' does not exist.")
'''

print()


# In[47]:


#Return a list of all collections in your database:
print(mydb.list_collection_names())

#Create a new collection called "comment"
mycol = mydb["comment"]
print(type(mycol))

#Check if collection exists by calling function check_CollectionExists with the following arguements (parameters):
#Name of database as the first arguement 
#Name of collection as the second arguement
#mydb as the third arguement
#In MongoDB, a collection is not created until it gets content. 
check_CollectionExists("assignment1", "comment", mydb)

'''
#Without a function the code will be as follows
collist = mydb.list_collection_names()
if "customers" in collist:
    print("The collection 'customers' exists.")
'''


# In[48]:


#Example of schemaless - adding additional key-value pairs
#Insert Multiple Documents, with Specified IDs
mylist = [
  { "_id": 1, "customer_ID": 2, "product_ID": 4, "rating":5, "content": "I love it!"},
  { "_id": 2, "customer_ID": 2, "product_ID": 5, "rating":4, "content": "Worked great for me"},
  { "_id": 3, "customer_ID": 3, "product_ID": 1, "rating":3, "content": "Def not best, but not worst"},
  { "_id": 4, "customer_ID": 5, "product_ID": 1, "rating":5, "content": "Excellent product"},
  { "_id": 5, "customer_ID": 5, "product_ID": 2, "rating":2, "content": "Worth paying more for something else."},
  { "_id": 6, "customer_ID": 5, "product_ID": 3, "rating":4, "content": "Exellent Service"},
  { "_id": 7, "customer_ID": 7, "product_ID": 1, "rating":3, "content": "Pissed off-a little bit"},
  { "_id": 8, "customer_ID": 7, "product_ID": 2, "rating":5, "content": "Five Stars"},
  { "_id": 9, "customer_ID": 7, "product_ID": 6, "rating":4, "content": "Awesome with a But!!"},
  { "_id": 10, "customer_ID": 8, "product_ID": 3, "rating":5, "content": "simply great!"},
  { "_id": 11, "customer_ID": 8, "product_ID": 6, "rating":4, "content": "not bad"},
  { "_id": 12, "customer_ID": 11, "product_ID": 4, "rating":5, "content": "Pretty Good!"},
  { "_id": 13, "customer_ID": 12, "product_ID": 11, "rating":5, "content": "I love it!"},
  { "_id": 14, "customer_ID": 13, "product_ID": 12, "rating":1, "content": "It is broken!"},
  { "_id": 15, "customer_ID": 14, "product_ID": 11, "rating":5, "content": "This is my love"},
  { "_id": 16, "customer_ID": 13, "product_ID": 4, "rating":2, "content": "Just so"},
  { "_id": 17, "customer_ID": 15, "product_ID": 5, "rating":2, "content": "It have not sound"},
  { "_id": 18, "customer_ID": 15, "product_ID": 13, "rating":4, "content": "Good thing"},
  { "_id": 19, "customer_ID": 16, "product_ID": 11, "rating":5, "content": "I will recommend it to my friends!"},
  { "_id": 20, "customer_ID": 17, "product_ID": 1, "rating":3, "content": "Just for use"},
  { "_id": 21, "customer_ID": 17, "product_ID": 13, "rating":4, "content": "Pretty good game mouse"}
]

var = mycol.insert_many(mylist)

#print list of the _id values of the inserted documents:
print(var.inserted_ids)


# In[49]:


#Display all documents in collection
#The find() method returns all occurrences in the selection.
#The first parameter of the find() method is a query object. In this example we use an empty query object, which selects all documents in the collection.

myresult = mycol.find()

#print the result:
for x in myresult:
    print(x)


# In[50]:


#Return a list of all collections in your database:
print(mydb.list_collection_names())

#Create a new collection called "comment"
mycol = mydb["product_comment"]
print(type(mycol))

#Check if collection exists by calling function check_CollectionExists with the following arguements (parameters):
#Name of database as the first arguement 
#Name of collection as the second arguement
#mydb as the third arguement
#In MongoDB, a collection is not created until it gets content. 
check_CollectionExists("product_comment", "test2", mydb)

'''
#Without a function the code will be as follows
collist = mydb.list_collection_names()
if "customers" in collist:
    print("The collection 'customers' exists.")
'''


# In[51]:


#Example of schemaless - adding additional key-value pairs
#Insert Multiple Documents, with Specified IDs
mylist = [
  { "product":[{"product_ID": 1, "product_name": "keyboard", "product_price": 40 }], 
    "comment":[{"rating": 3, "content":"Def not best, but not worst", "reviewer":
                [{"customer_ID": 3, "customer_name":"Jack"}]},
               {"rating": 5, "content":"Excellent product", "reviewer":
                [{"customer_ID": 5, "customer_name":"Henry"}]},
               {"rating": 3, "content":"Pissed off-a little bit", "reviewer":
                [{"customer_ID": 7, "customer_name":"Alex"}]}
              ] 
  },
  { "product":[{"product_ID": 2, "product_name": "microphone", "product_price": 30 }], 
    "comment":[{"rating": 2, "content":"Worth paying more for something else.", "reviewer":
                [{"customer_ID": 5, "customer_name":"Henry"}]},
               {"rating": 5, "content":"Five stars", "reviewer":
                [{"customer_ID": 7, "customer_name":"Alex"}]}
              ] 
  },
  { "product":[{"product_ID": 3, "product_name": "postcard", "product_price": 10 }], 
    "comment":[{"rating": 5, "content":"simply great!", "reviewer":
                [{"customer_ID": 8, "customer_name":"Iris"}]},
               {"rating": 4, "content":"Exellent Service", "reviewer":
                [{"customer_ID": 5, "customer_name":"Henry"}]}
              ] 
  },
  { "product":[{"product_ID": 4, "product_name": "calculator", "product_price": 60 }], 
    "comment":[{"rating": 5, "content":"I love it!", "reviewer":
                [{"customer_ID": 2, "customer_name":"Janet"}]},
               {"rating": 5, "content":"Pretty good!", "reviewer":
                [{"customer_ID": 11, "customer_name":"Andy"}]},
               {"rating": 2, "content":"just so", "reviewer":
                [{"customer_ID": 13, "customer_name":"Mark"}]}
              ] 
  },
  { "product":[{"product_ID": 5, "product_name": "displayer", "product_price": 80 }], 
    "comment":[{"rating": 4, "content":"Worked great for me", "reviewer":
                [{"customer_ID": 2, "customer_name":"Janet"}]},
               {"rating": 2, "content":"It have not sound", "reviewer":
                [{"customer_ID": 15, "customer_name":"Jack"}]}
              ] 
  },
  { "product":[{"product_ID": 6, "product_name": "tableware", "product_price": 20 }], 
    "comment":[{"rating": 4, "content":"not bad", "reviewer":
                [{"customer_ID": 8, "customer_name":"Iris"}]},
               {"rating": 4, "content":"Awesome", "reviewer":
                [{"customer_ID": 7, "customer_name":"Alex"}]}
              ] 
  },
  { "product":[{"product_ID": 11, "product_name": "switch", "product_price": 300 }], 
    "comment":[{"rating": 5, "content":"I love it!", "reviewer":
                [{"customer_ID": 12, "customer_name":"Judy"}]},
               {"rating": 5, "content":"This is my love", "reviewer":
                [{"customer_ID": 14, "customer_name":"Mario"}]},
               {"rating": 5, "content":"I will recommend it to my friends!", "reviewer":
                [{"customer_ID": 16, "customer_name":"John"}]}
              ] 
  },
  { "product":[{"product_ID": 12, "product_name": "smartphone", "product_price": 350 }], 
    "comment":[{"rating": 1, "content":"It is broken!", "reviewer":
                [{"customer_ID": 13, "customer_name":"Mark"}]}] 
  },
  { "product":[{"product_ID": 13, "product_name": "mouse", "product_price": 15 }], 
    "comment":[{"rating": 4, "content":"Good thing", "reviewer":
                [{"customer_ID": 15, "customer_name":"Jack"}]},
               {"rating": 4, "content":"Pretty good game mouse", "reviewer":
                [{"customer_ID": 17, "customer_name":"Bob"}]}
              ] 
  }
]

var = mycol.insert_many(mylist)

#print list of the _id values of the inserted documents:
print(var.inserted_ids)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[52]:


#Return a list of all collections in your database:
print(mydb.list_collection_names())

#Create a new collection called "comment"
mycol = mydb["order_product"]
print(type(mycol))

#Check if collection exists by calling function check_CollectionExists with the following arguements (parameters):
#Name of database as the first arguement 
#Name of collection as the second arguement
#mydb as the third arguement
#In MongoDB, a collection is not created until it gets content. 
check_CollectionExists("assignment1", "order_product", mydb)

'''
#Without a function the code will be as follows
collist = mydb.list_collection_names()
if "customers" in collist:
    print("The collection 'customers' exists.")
'''


# In[53]:


#Example of schemaless - adding additional key-value pairs
#Insert Multiple Documents, with Specified IDs
mylist = [
  { "order_id": 1, "product_ID": 2},
  { "order_id": 2, "product_ID": 1},
  { "order_id": 3, "product_ID": 1},
  { "order_id": 3, "product_ID": 2},
  { "order_id": 4, "product_ID": 3},
  { "order_id": 5, "product_ID": 4},
  { "order_id": 6, "product_ID": 5},
  { "order_id": 7, "product_ID": 6},
  { "order_id": 8, "product_ID": 3},
  { "order_id": 9, "product_ID": 1},
  { "order_id": 10, "product_ID": 6},
  { "order_id": 11, "product_ID": 4},
  { "order_id": 12, "product_ID": 11},
  { "order_id": 13, "product_ID": 12},
  { "order_id": 14, "product_ID": 11},
  { "order_id": 15, "product_ID": 4},
  { "order_id": 16, "product_ID": 5},
  { "order_id": 16, "product_ID": 13},
  { "order_id": 17, "product_ID": 11},
  { "order_id": 18, "product_ID": 1},
  { "order_id": 18, "product_ID": 13}
 
]

var = mycol.insert_many(mylist)

#print list of the _id values of the inserted documents:
print(var.inserted_ids)


# In[47]:


#Display all documents in collection
#The find() method returns all occurrences in the selection.
#The first parameter of the find() method is a query object. In this example we use an empty query object, which selects all documents in the collection.

myresult = mycol.find()

#print the result:
for x in myresult:
    print(x)


# In[ ]:





# In[ ]:





# In[54]:


#Return a list of all collections in your database:
print(mydb.list_collection_names())

#Create a new collection called "comment"
mycol = mydb["customer_product"]
print(type(mycol))

#Check if collection exists by calling function check_CollectionExists with the following arguements (parameters):
#Name of database as the first arguement 
#Name of collection as the second arguement
#mydb as the third arguement
#In MongoDB, a collection is not created until it gets content. 
check_CollectionExists("assignment1", "customer_product", mydb)

'''
#Without a function the code will be as follows
collist = mydb.list_collection_names()
if "customers" in collist:
    print("The collection 'customers' exists.")
'''


# In[58]:


#Example of schemaless - adding additional key-value pairs
#Insert Multiple Documents, with Specified IDs
mylist = [
  { "customer_id": 2, "product_ID": 4},
  { "customer_id": 2, "product_ID": 5},
  { "customer_id": 3, "product_ID": 1},
  { "customer_id": 3, "product_ID": 1},
  { "customer_id": 5, "product_ID": 2},
  { "customer_id": 5, "product_ID": 3},
  { "customer_id": 7, "product_ID": 1},
  { "customer_id": 7, "product_ID": 2},
  { "customer_id": 7, "product_ID": 6},
  { "customer_id": 8, "product_ID": 3},
  { "customer_id": 8, "product_ID": 6},
  { "customer_id": 11, "product_ID": 4},
  { "customer_id": 12, "product_ID": 11},
  { "customer_id": 13, "product_ID": 12},
  { "customer_id": 13, "product_ID": 4},
  { "customer_id": 14, "product_ID": 11},
  { "customer_id": 15, "product_ID": 5},
  { "customer_id": 15, "product_ID": 13},
  { "customer_id": 16, "product_ID": 11},
  { "customer_id": 17, "product_ID": 1},
  { "customer_id": 17, "product_ID": 13}  
]


var = mycol.insert_many(mylist)

#print list of the _id values of the inserted documents:
print(var.inserted_ids)


# In[55]:


#Display all documents in collection
#The find() method returns all occurrences in the selection.
#The first parameter of the find() method is a query object. In this example we use an empty query object, which selects all documents in the collection.

myresult = mycol.find()

#print the result:
for x in myresult:
    print(x)


# In[ ]:





# In[56]:


db = mongoclient.assignment1
collection = db.order_product
order_product = pd.DataFrame(list(collection.find()))
order_product.drop(['_id'], axis=1,inplace=True)
order_product


# In[59]:



collection = db.customer_product
customer_product = pd.DataFrame(list(collection.find()))
customer_product.drop(['_id'], axis=1,inplace=True)
customer_product


# In[ ]:





# In[60]:




collection = db.comment
comment = pd.DataFrame(list(collection.find()))
comment.rename(columns={'_id':'comment_ID'}, inplace = True)
comment


# In[61]:


customer = pd.read_sql("SELECT * FROM customer",con=conn)
order = pd.read_sql("SELECT * FROM [order]",con=conn)
product = pd.read_sql("SELECT * FROM product",con=conn)
comment_sql = pd.read_sql("SELECT * FROM comment",con=conn)


# In[62]:


customer


# In[63]:


order


# In[64]:


product


# In[70]:


comment_sql


# In[65]:


d = pd.merge(product, customer_product, left_on=['pro_ID'],right_on = ['product_ID'])
d


# In[85]:


table = pd.merge(order_product, order, left_on='order_id', right_on = 'order_ID')
table = pd.merge(table, customer, left_on = 'customer_ID',right_on = 'cus_ID')


# In[86]:


table = pd.merge(table,comment,left_on = ['customer_ID','product_ID_x'],right_on = ['customer_ID','product_ID'])


# In[87]:


table = pd.merge(table, d, left_on=['customer_ID','product_ID_x'],right_on = ['customer_id','product_ID'])


# In[89]:


table.head()


# In[90]:


table = table.drop(['product_ID_y','order_id','cus_ID','product_ID_x','product_ID_y','customer_id','pro_ID','customer_ID_y'],axis=1)


# In[91]:


table=table.drop('comment_ID',axis=1)


# In[93]:


table.head()


# In[94]:


table.columns = ['Order ID','Order Total Cost','Customer ID','Shipping Address','Name','Telephone Number','E-Mail','Age','Sex','Rating','Comments','Product','Price']


# In[95]:


table


# In[96]:


table = table[columns]
table = table.sort_values(['Order ID'])


# In[97]:


table


# In[ ]:





# In[98]:


product_rating = table.groupby(by=['Product'])['Rating'].mean()
customer_rating = table.groupby(by=['Name'])['Rating'].mean()
product_customer = table.groupby(by=['Product'])['Customer ID'].count()

px.bar(product_rating.reset_index().sort_values(by='Rating',ascending=False),
       x='Product', y='Rating', title='Rating Mean of Products')


# In[99]:


px.bar(customer_rating.reset_index().sort_values(by='Rating',ascending=False),
       x='Name', y='Rating', title='Rating of People')


# In[100]:


px.bar(product_customer.reset_index().sort_values(by='Customer ID',ascending=False),
       x='Product', y='Customer ID', title='Product Sales')


# In[101]:


# Item prices count
px.histogram(table, x='Price', title='item Prices')


# In[102]:


# Item prices count
px.histogram(table, x='Price', title='item Prices')


# In[103]:


# Do higher prices get better ratings?
px.scatter(table, x='Price', y='Rating', title='Ratings vs Prices') 


# In[104]:


px.line(table.groupby(by=['Rating'])['Product'].count().reset_index(), 
           x='Rating', y = 'Product' ,title='Ratings vs Sales') 


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




