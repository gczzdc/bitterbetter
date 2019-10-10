import requests
import pandas as pd
import flask


app = flask.Flask(__name__)

@app.route('/')
@app.route('/index',methods=['GET','POST'])
def index():
	default_keywords = {'result_paragraph': 'Hello World'}
	if flask.request.method =='GET':
		return (flask.render_template('get.html',**default_keywords))
	elif flask.request.method == 'POST':
		try:
			keywords={} 
		except Exception:
			keywords = default_keywords
			keywords['error_message']= 'unknown error'
			return (flask.render_template('get.html',**keywords))
		return (flask.render_template('post.html'),**keywords)


if __name__ == '__main__':
	app.run(debug=True)