import flask
from build_results_html import build_results_html

app = flask.Flask(__name__)

@app.route('/')
@app.route('/index',methods=['GET','POST'])
def index():
	keywords = {'submission': '',
				'error_message': ''}

	if flask.request.method == 'POST':
		submission=flask.request.form['submission']
		keywords['submission']=submission
		#submission has not been cleaned or marked safe but flask will do that here for us

		try:
			#submission is not safe and is being passed back as safe so this requires handling
			keywords['full_results'] = flask.Markup(build_results_html(submission))
			#should add abv and style
		except Exception:
			raise
			### fix this error handling
			keywords['error_message']= 'unknown error'
	return (flask.render_template('index.html',**keywords))


if __name__ == '__main__':
	app.run(debug=True)