import requests
import pandas as pd
import flask


app = flask.Flask(__name__)

@app.route('/')
@app.route('/index',methods=['GET','POST'])
def index():
	keywords = {'submission': '',
				'error_message': ''}

	if flask.request.method =='GET':
		return (flask.render_template('get.html',**keywords))

	elif flask.request.method == 'POST':

		keywords['submission']=flask.request.form['submission']

		try:
			### update keywords
		except Exception:
			### fix this error handling
			keywords['error_message']= 'unknown error'
			return (flask.render_template('get.html',**keywords))
		return (flask.render_template('post.html'),**keywords)


if __name__ == '__main__':
	app.run(debug=True)