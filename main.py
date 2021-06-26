import datetime

from flask import Flask, render_template, request, flash
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
    app.run(debug=True)

datastore_client = datastore.Client()

@app.route('/') 
def home(): 
    return render_template('home.html') 

        
@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        message1 = 'query finished'
        userList = getIDs()
        # for entity in userList:
        #     if entity.
        return render_template('login.html', message1=message1, userList=userList)
            # ID = request.form['ID']
            # message1 = "ID exists."
            # message2 =  "No ID found"

            # if ID == None:
            #     return render_template('login.html')
            # elif ID != None and isID(ID):
            #     return render_template('login.html', message1=message1)
            # elif ID != None and isID(ID) == False:
            #     return render_template('login.html', message1=message2)
            
                
            # message1 = "You said " + ID
            # message2 = 'Thanks for the greeting!'
            # if ID == 'yo':
            #     return render_template('login.html', message1=message1, message2=message2)
            # elif ID == 'fuck you':
            #     message1 = 'hey thats not nice'
            #     message2 = 'maybe try typing something nicer'
            #     return render_template('login.html', message1=message1, message2=message2)
            # elif ID == None:
            #     return render_template('login.html')

    return render_template('login.html')

@app.route('/register/')
def register():
    return render_template('register.html')

@app.route('/forum/')
def forum():
    return render_template('forum.html')

@app.route('/user/')
def user():
    return render_template('user.html')

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

def isID(ID):
    query = datastore_client.query(kind='user')
    query.add_filter("ID", "=", ID)
    if query.fetch(ID):
        return True
    else:
        return False

def getIDs():
    query = datastore_client.query(kind="user")
    results = list(query.fetch())
    return results