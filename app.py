import requests
import pandas as pd
import flask


app = flask.Flask(__name__)

@app.route('/')
@app.route('/index',methods=['GET','POST'])
def index():
	if flask.request.method in ['GET','POST']:
		keywords = {'result_paragraph': 'Hello World'}
		return (flask.render_template('index.html',**keywords))

if __name__ == '__main__':
	app.run(debug=True)