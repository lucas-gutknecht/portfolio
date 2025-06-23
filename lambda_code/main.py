from flask import Flask, render_template
import serverless_wsgi

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/this-website')
def this_website():
    return render_template('this_website.html')

@app.route('/googleea6f05e89766f111.html')
def google_search():
    return render_template('googleea6f05e89766f111.html')

def lambda_handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)

app.run(debug=True)