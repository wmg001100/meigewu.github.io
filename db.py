import connect, psycopg2   # import connect.py file & SQL driver to the database and let the python talk to the database
print("import done - establishing connection") # comfirm that imported & established the connection 
conn = psycopg2.connect(dbname=connect.dbname, user=connect.dbuser, \
     password=connect.dbpass, host=connect.dbhost, port=connect.dbport) #connect with database server and pass the variables from connect.py
print(f"connection done - {conn}") 
with conn:              # query is happen within the sursor and does not allow directly execute the query
    cur = conn.cursor() # so we need get the cursor  
    cur.execute("select * from member;")# execute the query
    select_result = cur.fetchall() 
    print(select_result) # get result from the query and get all results


