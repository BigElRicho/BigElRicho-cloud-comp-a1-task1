import datetime
from flask import Flask, render_template, request, session
from google.cloud import datastore

app = Flask(__name__)
app.secret_key = "Julian"

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App 
    # Engine, a webserver process such as Gunicorn will serve the app. 
    # This can be configured by adding an `entrypoint` to app.yaml. 
    # Flask's development server will automatically serve static files in 
    # # the "static" directory. 
    # See: http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed, 
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1',debug=True)

datastore_client = datastore.Client()

@app.route('/') 
def home(): 
    return render_template('home.html') 

@app.route('/login/', methods=['GET','POST'])
def login():
    sessionMsg = session.get('ID')
    userMsg = ""
    pwdMsg = ""
    if session.get('ID') is not None:
        print("session id:" + session['ID'])
        sessionMsg = session['ID']
        userMsg = "Welcome " + getUsername(session['ID'])
        pwdMsg = "already validated."
    elif session.get('ID') is None:
        print("No session ID exists atm.")
    if request.method == 'POST':
        if session.get('ID') is not None:
            return render_template('login.html',
            sessionMsg=sessionMsg,
            userMsg=userMsg,
            pwdMsg=pwdMsg)

        message1 = 'query finished'
        pwdMsg = "unknown"
        #userMsg = "-"
        #sessionMsg = "-"
        loginValid = False
        IDValid = False
        passwordValid = False
        ID = request.form['ID']
        pwd = request.form['password']
        #userID = getID(ID)
        #print("userID: " + ID)
        if ID == "":
            userMsg = "No ID provided."
        else:
            if getID(ID) == None:
                print("UserID not known.")
                userMsg = "UserID not known."
            else:
                print("A matching ID was found.")
                userMsg = "Welcome " + getID(ID)
                IDValid = True
        if pwd == "":
            pwdMsg = "No password given"
        else:
            if doesPasswordMatch(ID,pwd):
                pwdMsg = "password correct."
                passwordValid = True
            else:
                pwdMsg = "password incorrect"
        if(IDValid == True and passwordValid == True):
            print("loginvalid = true")
            loginValid = True
            print(loginValid)
        # Below needs to be replaced with a redirect method.
        if(loginValid==True):
            session['ID'] = ID
            print("session['ID']= " + session['ID'])
            sessionMsg = session['ID']
            return render_template('forum.html')
            # return render_template('login.html', 
            # message1=message1, 
            # userMsg=userMsg, 
            # pwdMsg=pwdMsg,
            # sessionMsg=sessionMsg)
        else:
            # if session['ID']:
            #     print(session['ID'])
            # else:
            #     print ("Session['ID'] is not there.")
            return render_template('login.html', 
            message1=message1, 
            userMsg=userMsg, 
            pwdMsg=pwdMsg,
            sessionMsg=sessionMsg)

    return render_template('login.html', 
    sessionMsg=sessionMsg, 
    userMsg=userMsg,
    pwdMsg=pwdMsg)

@app.route('/register/', methods=['GET','POST'])
def register():
    message = ""
    id = ""
    username = ""
    password = ""
    imgName = ""
    if request.method == "POST":
        id = request.form['ID']
        username = request.form['username']
        password = request.form['password']
        #imgName = request.form['userImage']
        return render_template('register.html',
        message = message,
        ID = id,
        username = username,
        password = password)

    return render_template('register.html',
        message = message,
        ID = id,
        username = username,
        password = password)

@app.route('/forum/', methods=['GET','POST'])
def forum():
    username=""
    if session.get('ID') is not None:
        print("Session['id'] on forum page load: " + session.get('ID'))
        username = getUsername(session['ID'])
        return render_template('forum.html',username=username)

    return render_template('forum.html',username=username)

@app.route('/user/')
def user():
    userMsg = "No user currently logged in."
    if 'ID' in session:
        userID = session.get('ID')
        userMsg = userID
    
    return render_template('user.html',
    userMsg=userMsg)

@app.route('/pageVisits/')
def pageVisits():
     #Store the current access time in Datastore.
    store_time(datetime.datetime.now())

    # fetch the most recent 10 access times from datastore.
    times = fetch_times(10)

    return render_template('pageVisits.html',times=times) 


def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)

def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']
    times = query.fetch(limit=limit)
    return times

def getID(ID):
    query = datastore_client.query(kind='user')
    query.add_filter("ID", "=", ID)
    result = query.fetch()
    for IDs in result:
        #print(IDs['ID'])
        ID=IDs['ID']
    return ID

def getUsername(ID):
    query = datastore_client.query(kind='user')
    query.add_filter("ID", "=", ID)
    result = query.fetch()
    for IDs in result:
        #print(IDs['user_name'])
        username=IDs['user_name']
    return username



def doesPasswordMatch(ID, password):
    query = datastore_client.query(kind="user")
    query.add_filter("ID","=",ID)
    result = query.fetch()
    for IDs in result:
        #print(IDs['ID'] + IDs['password'])
        #print("ID given: "+ ID + " Password given: " + password)
        if IDs['password'] == password:
            return True
        else:
            return False
    
def getIDs():
    query = datastore_client.query(kind="user")
    query.order = ["ID"]
    results = query.fetch()
    return results