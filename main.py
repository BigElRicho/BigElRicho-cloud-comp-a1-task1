import datetime

from flask import Flask, render_template
#from google.cloud import datastore

app = Flask(__name__)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App 
    # Engine, a webserver process such as Gunicorn will serve the app. 
    # This can be configured by adding an `entrypoint` to app.yaml. 
    # Flask's development server will automatically serve static files in 
    # # the "static" directory. 
    # See: http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed, 
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(debug=True)

#datastore_client = datastore.Client()

@app.route('/') 
def home(): 
    return render_template('home.html') 
    # #Store the current access time in Datastore.
    # store_time(datetime.datetime.now())

    # # fetch the most recent 10 access times from datastore.
    # times = fetch_times(10)

    #return render_template('index.html'),times=times) 

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/register/')
def register():
    return render_template('register.html')

@app.route('/forum/')
def forum():
    return render_template('forum.html')

# @app.route('/user/')
# def user():
#     return render_template('user.html')

# def store_time(dt):
#     entity = datastore.Entity(key=datastore_client.key('visit'))
#     entity.update({
#         'timestamp': dt
#     })

#     datastore_client.put(entity)

# def fetch_times(limit):
#     query = datastore_client.query(kind='visit')
#     query.order = ['-timestamp']

#     times = query.fetch(limit=limit)

#     return times