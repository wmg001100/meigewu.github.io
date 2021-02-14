# choose all libraries that i want to import
from flask import Flask  # import from flask class
from flask import render_template
# import from request class & deal with the data that come from the route
from flask import request
import connect
import psycopg2
from flask import redirect
from flask import url_for
import uuid  # import the uuid class and it will generate unique id number

app = Flask(__name__)
# create an instance of the class for use
dbconn = None


def genID():  # generate from version4 that will make a random unique id
    return uuid.uuid4().fields[1]


def getCursor():  # create a function that connect with database
    global dbconn  # use conn and get query by use cursor
    if dbconn == None:
        conn = psycopg2.connect(dbname=connect.dbname, user=connect.dbuser,
                                password=connect.dbpass, host=connect.dbhost, port=connect.dbport)
        conn.autocommit = True
        dbconn = conn.cursor()
        return dbconn
    else:
        return dbconn


# all route is a decorator for flask to know which function to call
# denote default route and the route that will go to when get to first home url that being visiting
@app.route("/")
def home():  # function named home that flask should return to the home template
    return render_template("home.html")


# denote route and the route that will go to when get to 'kid' url that being visiting
@app.route("/kid/")
def kid():
    cur = getCursor()
    getCursor().execute("select groupid, familyname, firstname, activitynightid, attendancestatus from attendancekids1;")
    select_result = cur.fetchall()
    print(select_result)
    # get out all description from each of the column that was selected by the each query
    column_names = [desc[0] for desc in cur.description]
    print(f"{column_names}")
    # return to template and define variables for jinja template
    return render_template("kidname.html", kid=select_result, kidcols=column_names)


@app.route('/kidname', methods=['GET'])  # allow the method to get
def getName():
    print(request.args)
    # select the familyname and get their information
    familyname = request.args.get("familyname")
    print(familyname)
    cur = getCursor()
    cur.execute("select * from attendancekids1 where familyname=%s",
                (familyname,))  # execute the query and search the familyname then enter in
    select_result = cur.fetchall()  # get back all the results from query
    # display all the columns from description
    column_names = [desc[0] for desc in cur.description]
    print(f"{column_names}")
    return render_template("kid.html", kid=select_result, kidcols=column_names)


# denote route and the route that will go to when get to 'adult' url that being visiting
@app.route("/adult/")
def adult():
    cur = getCursor()
    getCursor().execute("select familyname, firstname, groupid, activitynightid, attendancestatus, notes from attendanceadults1;")
    select_result = cur.fetchall()  # get back all the results from query
    column_names = [desc[0] for desc in cur.description]
    print(f"{column_names}")
    return render_template("adultname.html", adult=select_result, adultcols=column_names)


@app.route('/adultname', methods=['GET'])  # allow the method to get
def getNameadult():
    print(request.args)
    familyname = request.args.get("familyname")
    print(familyname)
    cur = getCursor()
    cur.execute(
        "select * from attendanceadults1 where familyname=%s", (familyname,))
    select_result = cur.fetchall()  # get back all the results from query
    column_names = [desc[0] for desc in cur.description]
    print(f"{column_names}")
    return render_template("adult.html", adult=select_result, adultcols=column_names)


# allow the method to get and post
@app.route('/addnight', methods=['GET', 'POST'])
def addnight():
    if request.method == 'POST':
        # when form is submitted, go through the flask and print information from form
        print(request.form)
        id = genID()  # generate rendom id for activitynightid
        print(id)
        # get the imformation from the form such as groupid and nighttitle
        groupid = request.form.get('groupid')
        nighttitle = request.form.get('nighttitle')
        description = request.form.get('description')
        activitynightdate = request.form.get('activitynightdate')
        cur = getCursor()  # connect with database and insert imformation to activitynight
        cur.execute("insert into activitynight(activitynightid,groupid, nighttitle, description, activitynightdate) VALUES (%s,%s,%s,%s,%s);", (str(
            id), groupid, nighttitle, description, activitynightdate,))
        cur.execute(
            "select * from activitynight where activitynightid=%s", (str(id),))  # display the result for new activitynight
        select_result = cur.fetchall()  # get back all the results from query
        column_names = [desc[0] for desc in cur.description]
        return render_template("activitynight.html", night=select_result, nightcols=column_names)
    else:
        return render_template("addnight.html")


# allow the method to get and post
@app.route('/visitor/update', methods=['GET', 'POST'])
def visitorupdate():
    if request.method == 'POST':
        activitynightid = request.form.get('activitynightid')
        attendancestatus = request.form.get('attendancestatus')
        cur = getCursor()  # after filling out the form, connect to the database and update the selected person's information
        cur.execute("UPDATE attendancekids1 SET attendancestatus=%s where activitynightid=%s",
                    (attendancestatus, activitynightid,))
        cur.execute(
            "select * from attendancekids1 where activitynightid=%s", (activitynightid,))  # display the result for updated kidsinformation
        select_result = cur.fetchall()  # get back all the results from query
        column_names = [desc[0] for desc in cur.description]
        print(f"{column_names}")
        return render_template('kid.html', kid=select_result, kidcols=column_names)
    else:
        return render_template('visitorupdate.html')


# allow the method to get and post
@app.route('/adult/update', methods=['GET', 'POST'])
def adultupdate():
    if request.method == 'POST':
        familyname = request.form.get("familyname")
        firstname = request.form.get("firstname")
        activitynightid = request.form.get('activitynightid')
        attendancestatus = request.form.get(
            'attendancestatus')  # adult need to update the notes
        notes = request.form.get('notes')  # adult need to update the notes
        cur = getCursor()
        cur.execute("UPDATE attendanceadults1 SET attendancestatus=%s,notes=%s where familyname=%s and activitynightid=%s",
                    (attendancestatus, notes, familyname, activitynightid,))
        cur.execute(
            "select * from attendanceadults1 where familyname=%s", (familyname,))
        select_result = cur.fetchall()  # get back all the results from query
        column_names = [desc[0] for desc in cur.description]
        print(f"{column_names}")
        return render_template('adult.html', adult=select_result, adultcols=column_names)
    else:
        return render_template('adultupdate.html')


# allow the method to get and post
@app.route('/leftdate/update', methods=['GET', 'POST'])
def leftdateupdate():
    if request.method == 'POST':
        notes = request.form.get('notes')
        # adult need to update the leftdate
        leftdate = request.form.get('leftdate')
        familyname = request.form.get('familyname')
        firstname = request.form.get('firstname')
        cur = getCursor()
        cur.execute(
            "UPDATE attendanceadults1 SET leftdate=%s where familyname=%s", (leftdate, familyname,))
        cur.execute(
            "SELECT * FROM attendanceadults1 where familyname=%s", (familyname,))
        select_result = cur.fetchall()  # get back all the results from query
        column_names = [desc[0] for desc in cur.description]
        print(f"{column_names}")
        return render_template('adult.html', adult=select_result, adultcols=column_names)
    else:
        return render_template('leftdate.html')
