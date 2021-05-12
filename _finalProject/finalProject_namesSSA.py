#!/usr/bin/env python
# coding: utf-8

# In[6]:


from csv import reader
import sqlite3
import os
import re
import pandas as pd
import matplotlib.pyplot as plt


# In[7]:


# ============================================================================================================
# db connection and close functions
# ============================================================================================================

def connect_to_db(dbName):
    try:
        # establish a connection OR create new db and connect
        # dbconn is an object that will facilitate our communication to db
        dbconn = sqlite3.connect(dbName)
        #ask the connection for an object called a cursor
        cursor = dbconn.cursor()
        print('Connected to DB!')
    except sqlite3.Error as err:
        print("Error connecting")
        print(err)
    return dbconn,cursor
# ============================================================================================================
def close_DB_Resources(dbconn, cursor):
    '''
    Came directly from Lisa's guide
    https://github.com/lan33-ccac/DAT-129/blob/e05c8244077a518778df7457879f39d50e564fb8/DB_Interaction/dbdemo2.py#L332
    '''
    try:
        cursor.close()
        dbconn.close()
        print('\nDB resources were closed successfully.')
    except sqlite3.Error as error:
        print('Error occurred closing DB resources.', error)


# In[8]:


# ============================================================================================================
# db create, load and drop tables functions
# ============================================================================================================

def create_tables():
    
# --------------------------------------------------------
#  genders 
# --------------------------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS
            genders (
                genderID INTEGER PRIMARY KEY,
                genderCode TEXT NOT NULL,
                genderName TEXT NOT NULL,
        UNIQUE (genderCode, genderName) ON CONFLICT IGNORE
            );        
    ''')
    print('genders table created.')
# --------------------------------------------------------
#  names   
# --------------------------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS
            names (
                nameID INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
        UNIQUE (name) ON CONFLICT IGNORE
            );
    ''')
    print('names table created.')
# --------------------------------------------------------    
# ssaNamesData
# --------------------------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS
            ssaNameData (
                year INT NOT NULL,
                nameID INT NOT NULL,
                genderID INT NOT NULL,
                number INT NOT NULL
            );
    ''')
    print('ssaNameData table created.')
# --------------------------------------------------------
    dbconn.commit()
    
# UNIQUE prevents duplicate data in the column, 
# it does not look at the combination of columns
# therefore I was not able to use it in the ssaNameData table
# ============================================================================================================

def drop_table(tblName):
    
    dropTable = 'DROP TABLE IF EXISTS '+ tblName
    cursor.execute(dropTable)
    print('Table',tblName,'was deleted.')
    dbconn.commit()
# ============================================================================================================

def load_genders_table():
    
    genders_list = [('F', 'Female'),('M', 'Male')]

    # insert gender data into the table
    gender_insert = '''
        INSERT INTO genders (genderCode, genderName)
        VALUES (?, ?);
    '''

    # for each gender in the gender list
    # create a code, name tuple
    for g in genders_list:
        insert_tuple = (g[0],g[1])
        cursor.execute(gender_insert, insert_tuple)
        print(insert_tuple, 'loaded to genders table')
    dbconn.commit()
# ============================================================================================================

def load_names_table(root):
    
    # insert names data into the table
    name_insert = '''
        INSERT INTO names (name)
        VALUES (?);
    '''
    for location, directories, files in os.walk(root):
        # for each file in the folder
        for file in files:
            filename = location + str(os.sep) + file
            print('reading names from: ', filename)
            count = 0
            # open and read the file
            with open (filename) as ssafile:
                csv_reader = reader(ssafile)
                # for each row in the file
                for row in csv_reader:
                    # find name in the record and insert 
                    cursor.execute(name_insert,(row[0],))
                    count +=1    # keep a count of records found
            print('names found: ', count)

    dbconn.commit()
# ============================================================================================================

def getID(SELECT, match):
    # function to run the select query passed through SELECT and return the ID for match
    cursor.execute(SELECT,(match,))
    foundID = cursor.fetchone()
    return foundID[0]
# ============================================================================================================
def load_ssaNameData_table(root):
    # build the sql INSERT statement
    ssaNameData_insert = '''
        INSERT INTO ssaNameData (year, nameID, genderID, number)
        VALUES (?, ?, ?, ?);
    '''
    # These are select queries to pass in to getID() and return the matching name/gender id
    getnameID = 'SELECT nameID, name FROM names WHERE name=?' 
    getgenderID = 'SELECT genderID, genderCode FROM genders WHERE genderCode=?' 

    # for each file in the directory open and retrieve ssaNameData per row
    for location, directories, files in os.walk(root):
        for file in files:
            filename = location + str(os.sep) + file 
            print('loading data from: ', filename)
            count = 0    # start record count
            year = int(re.findall(r'\d+', file)[0])    # get year from file name to load as year

            with open (filename) as ssafile:
                csv_reader = reader(ssafile)
                # for each row, get data for insert_tuple
                for row in csv_reader:
                    nameID = getID(getnameID, row[0])    # finds nameID from names table
                    genderID = getID(getgenderID, row[1])    # finds genderID from gender table
                    number = int(row[2])    # finds the data value for name occurences
                    insert_tuple = (year, nameID, genderID, number)    #creates tuple of row data        
                    cursor.execute(ssaNameData_insert,insert_tuple)    # inserts data from tuple into data table
                    count +=1    # counts the number of rows found
            print('\trecords found: ', count)

    dbconn.commit()
    
# === Room for improvement ===
# This function loads all files in the folder
# if a new file is recevied all data should be
# deleted and reloaded to avoid duplication.


# In[9]:


# ============================================================================================================
# data queries
# ============================================================================================================

def qry1(namesList):

    # This query sums the occurences for each name per year (regardless of gender)
    
    inList = str(namesList)[1:-1]

    selectFrom='''
         SELECT names.name, ssaNameData.year, sum (ssaNameData.number) AS 'occurences'
            FROM ssaNameData INNER JOIN names on ssaNameData.nameID = names.nameID
            '''
    where= 'WHERE names.name IN'
    groupOrder='''
            GROUP BY names.name, ssaNameData.year
            ORDER BY ssaNameData.year DESC, names.name;
    '''
    if inList.lower() == str(['all'])[1:-1]:
        qrySQL = (selectFrom + groupOrder)
    else:
        qrySQL = (selectFrom + where + ' ('+ inList + ') '+ groupOrder)
        
    return qrySQL
# ============================================================================================================
def qry2(namesList):
    
    # This query shows per name, first/last year appeared and year of peak occurences
    
    inList = str(namesList)[1:-1]

    selectFrom='''
        SELECT t1.name, t1.first, t2.peakYear, t1.last
        FROM
            (SELECT names.name, min(ssaNameData.year) as 'first', max(ssaNameData.year) AS 'last'
            FROM ssaNameData INNER JOIN names on ssaNameData.nameID = names.nameID
            GROUP BY names.name
            ORDER BY name) t1
        LEFT JOIN
            (SELECT names.name, ssaNameData.year AS 'peakYear', max(ssaNameData.number) AS 'peakOccur' 
            FROM ssaNameData INNER JOIN names on ssaNameData.nameID = names.nameID
            GROUP BY names.name) t2
            ON (t1.name = t2.name)
            '''
    where='WHERE t1.name IN'

    if inList.lower() == str(['all'])[1:-1]:
        qrySQL = (selectFrom + ';')
    else:
        qrySQL = (selectFrom + where + ' (' + inList + ');')

    return qrySQL
# ============================================================================================================
def qry3(namesList):
    
    # This query shows per name, total occurences descending 
    
    inList = str(namesList)[1:-1]

    selectFrom='''
        SELECT names.name, sum (ssaNameData.number) AS 'occurences'
            FROM ssaNameData INNER JOIN names on ssaNameData.nameID = names.nameID
            '''
    where= 'WHERE names.name IN'
    groupOrder='''
            GROUP BY names.name
            ORDER BY occurences DESC;
            '''
    if inList.lower() == str(['all'])[1:-1]:
        qrySQL = (selectFrom + groupOrder)
    else:
        qrySQL = (selectFrom + where + ' ('+ inList + ') '+ groupOrder)

    return qrySQL 
# ============================================================================================================
def qry4(namesList):
    
    # This query shows per name the count of years ranked #1 in most occurences
    
    qrySQL='''
        SELECT t1.name, t1.genderName as 'gender', count(t1.year) as 'yearsTopRank'
        FROM
            (SELECT ssaNameData.year, names.name,genders.genderName, max(ssaNameData.number) as 'occurences'
                FROM ssaNameData INNER JOIN names on ssaNameData.nameID = names.nameID
                INNER JOIN genders on ssaNameData.genderID = genders.genderID
                GROUP BY ssaNameData.year, genders.genderName) as t1
        GROUP BY t1.name
        ORDER BY [yearsTopRank] DESC
        '''
    return qrySQL
# ============================================================================================================
def qry5(namesList):

    # This query shows per gender the count of unique names and total occurences
    
    qrySQL='''
        SELECT genders.genderName as 'gender', COUNT(DISTINCT names.name) AS 'uniqueNames',
            SUM(ssaNameData.number) AS 'Occurences'
        FROM ssaNameData INNER JOIN names on ssaNameData.nameID = names.nameID
        INNER JOIN genders on ssaNameData.genderID = genders.genderID
        GROUP BY gender
        '''
    return qrySQL
# ============================================================================================================
def qry6(namesList):
    
    # This query shows the count of unique names and total occurences
    
    qrySQL='''
        SELECT COUNT(DISTINCT names.name) AS 'uniqueNames', SUM(ssaNameData.number) AS 'occurences'
        FROM ssaNameData INNER JOIN names on ssaNameData.nameID = names.nameID
        '''
    return qrySQL
# ============================================================================================================
def qry7(namesList):

    # This query show the Top name per gender per year
    
    qrySQL='''
        SELECT ssaNameData.year, names.name,genders.genderName as 'gender', max(ssaNameData.number) as 'num'
        FROM ssaNameData INNER JOIN names on ssaNameData.nameID = names.nameID
        INNER JOIN genders on ssaNameData.genderID = genders.genderID
        GROUP BY ssaNameData.year, gender
        ORDER BY ssaNameData.year DESC, gender
        '''
    return qrySQL


# In[10]:


# ===================
# pandas data frames
# ===================

def qry_table(query, namesList,topN=25):
# display query as data table
    df = pd.read_sql_query(query(namesList), dbconn).head(topN)
    display(df)
    
def qry1_pivotTable(query, namesList):
    # display query 1 as data table (Head counts per year)
    df = pd.read_sql_query(query(namesList), dbconn).pivot('year', 'name', 'occurences').sort_index(ascending=False).fillna(0).style.format('{:20,.0f}').set_caption('Occurences by year and name - Details')
    display(df)
    # === TO DO ===
    # sort year desc
        
def qry1_graph(query, namesList):
    # display query 1 as graph (Head counts per year)
    df = pd.read_sql_query(query(namesList), dbconn).pivot('year', 'name', 'occurences')
    plt.figure(figsize=(15,10)); df.plot(colormap='jet'); plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5));
    plt.title('Occurences by year and name - Graph')


# In[11]:


# ===========================================
# program actions for future menu navigation
# ===========================================

def action(action=0):
    
    if action == 1:    # initionalize db and create tables for gender, name, and data
        create_tables()

    elif action == 2:    # load unique genders into the gender table
        load_genders_table()
 
    elif action == 3:    # load from data files, unique names into the names table
        load_names_table(filesLoc)

    elif action == 4:    # load from data files, unique names into the names table
        load_ssaNameData_table(filesLoc)

    elif action == 5:    # drop 'ssaNameData' to reload data
        drop_table('ssaNameData')

    elif action == 6:    # drop 'names' to reload data
        drop_table('names') 
        
    elif action == 7:    # drop 'genders' to reload data
        drop_table('genders')


# In[12]:


# ===========================================
# various name lists for queries
# ===========================================

def qryNames(listNumber):

    if listNumber == 0:
        listNames = ['All']

    elif listNumber == 1:    # Top Ranked Names each year
        listNames = ['Mary', 'Michael', 'John','Robert', 'Jennifer', 'Jacob', 'James',
                     'Emily', 'Jessica', 'Lisa', 'Linda', 'Emma', 'Noah', 'Sophia',
                     'Liam', 'Isabella', 'Ashley', 'Olivia', 'David']

    elif listNumber == 2:    # Top 5 overall
        listNames = ['James', 'John','Robert', 'Michael',  'William']

    elif listNumber == 3:    # Bottom 5 overall among Top Ranked Names
        listNames = ['Noah', 'Sophia', 'Liam', 'Isabella', 'Olivia',]


    elif listNumber == 4:    # Class Names - SP21 Python 2 6pm W
        listNames = ['Eric', 'Loretta', 'Virginia', 'Shane', 'Kamala', 'Evan', 'Jon',
                       'Leon', 'Rachael', 'Katie', 'Alissa', 'Matthew', 'Timothy',
                       'Carl', 'Alev', 'Ian', 'Monica', 'Paige']
        
    elif listNumber == 5:    # Class Names - Presentation Group - to be updated in class after group assignment
        listNames = ['Eric','Loretta', 'Alissa','Virginia', 'Shane', 'Kamala', 'Evan', 'Jon',
                       'Leon', 'Rachael', 'Katie', 'Alissa', 'Matthew', 'Timothy',
                       'Carl', 'Alev', 'Ian', 'Monica', 'Paige']

    elif listNumber == 6:    # Top 5 Class Names
        
        listNames = ['Matthew', 'Timothy', 'Carl','Eric', 'Virginia']

    elif listNumber == 7:    # Spelling Variations
        
        listNames = ['Alyssa', 'Alissa']

    elif listNumber == 8:    # select names
        listNames = ['Adolf']

    return listNames


# In[13]:


# ===============================================
# === FINAL PROJECT - SP21 DAT129 - Python II ===
# ===============================================
# source data downloaded in a zip file from 
# https://www.ssa.gov/oact/babynames/limits.html
# ===============================================


# In[14]:


# ==================================
# define location and database name
# ==================================

# define location of data files:
filesLoc = '.\ssaNames_national\data'

# define name of database:
dbName = 'fp_SSAnames.db'

# ==================================
# run database table actions
# ==================================

dbconn,cursor = connect_to_db(dbName)

action(0)

close_DB_Resources(dbconn, cursor)

# ACTION definitions
# ===========================================================
# 0: no action runs

# 1: create tables for genders, names, and data
# 2: load unique GENDERS into the 'genders' table
# 3: load unique NAMES from files into the 'names' table
# 4: load DATA from files into the 'ssaNames_National' table

# 5: drop 'ssaNameData' to reload data
# 6: drop 'genders' table to reload table
# 7: drop 'names' table to reload table
# ===========================================================

# ========== Room for Improvement ==========
# add error handling if files don't exist


# In[15]:


# ==========================================================
# run data queries for overall data
# ==========================================================
# queries have a top 25 rows limit, and an optional argument
# to increase or decrease the number of rows displayed.


# In[16]:


dbconn,cursor = connect_to_db(dbName)
print('\nOverall')
qry_table(qry6,['All'])
close_DB_Resources(dbconn, cursor)


# In[17]:


dbconn,cursor = connect_to_db(dbName)
print('\nOverall by gender')
qry_table(qry5,['All'])
close_DB_Resources(dbconn, cursor)


# In[18]:


dbconn,cursor = connect_to_db(dbName)
print('\nNumber of years ranked #1 in occurences')
print('by name and gender')
qry_table(qry4,['All'])
close_DB_Resources(dbconn, cursor)


# In[19]:


dbconn,cursor = connect_to_db(dbName)
print('\nTotal occurences by name')
qry_table(qry3,['All'],10)
close_DB_Resources(dbconn, cursor)


# In[20]:


dbconn,cursor = connect_to_db(dbName)
print('\nTotal occurences by name and gender')
qry_table(qry7,['All'],10)
close_DB_Resources(dbconn, cursor)


# In[21]:


# ============================================
# run data queries for selected name/s
# ============================================
# Query Names Lists 
# ============================================
# 0: All
# 1: Top Names each year
# 2: Top 5 Names overall
# 3: Bottom 5 overall among Top Ranked Names
# 4: Class Names - SP21 Python 2 6pm W
# 5: Top 5 Class Names
# 6: Class Names - presentation group
# 7: Spelling Variations
# 8: Other select name(s)
# ============================================

selectNames = qryNames(2)


# In[23]:


dbconn,cursor = connect_to_db(dbName)
print('\nTotal occurences by name')
qry_table(qry3, selectNames)
close_DB_Resources(dbconn, cursor)


# In[24]:


dbconn,cursor = connect_to_db(dbName)
print('\nFirst and last year in data')
print('and year of peak occurence')
qry_table(qry2, selectNames)
close_DB_Resources(dbconn, cursor)


# In[25]:


dbconn,cursor = connect_to_db(dbName)
qry1_graph(qry1, selectNames)
close_DB_Resources(dbconn, cursor)


# In[26]:


dbconn,cursor = connect_to_db(dbName)
qry1_pivotTable(qry1, selectNames)
close_DB_Resources(dbconn, cursor)

