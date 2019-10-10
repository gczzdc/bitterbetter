import requests
import pandas as pd
import flask
from ibu_prediction import bag_of_words_paragraph, best_predictor




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

		#clean submission for safety

		try:
			### update keywords
				keywords['result_paragraph'] = bag_of_words_paragraph()
				keywords['prediction'] = 35
		except Exception:
			raise
			### fix this error handling
			keywords['error_message']= 'unknown error'
			return (flask.render_template('get.html',**keywords))
		return (flask.render_template('post.html',**keywords))


if __name__ == '__main__':
	app.run(debug=True)