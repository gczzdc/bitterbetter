import flask
from build_results_html import build_results_html

app = flask.Flask(__name__)

@app.route('/')
@app.route('/index',methods=['GET','POST'])
def index():
	keywords = {'submission': '',
				'error_message': '',
				'selected_not_specified': 'selected="selected"'}

	if flask.request.method == 'POST':
		submission=flask.request.form['submission']
		abv = flask.request.form['abv']
		style = flask.request.form['style']
		#do something to make sure these exist

		keywords['submission']=submission
		keywords['abv']=abv
		keywords['selected_not_specified']=''
		selected_tag = style
		selected_tag = selected_tag.replace(' ','_')
		selected_tag = selected_tag.replace('/','_')
		selected_tag = selected_tag.replace('-','_')
		keywords[selected_tag]='selected="selected"'

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