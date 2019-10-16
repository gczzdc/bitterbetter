import flask
from build_results_html import build_results_html
from parsers import parse_abv, parse_style, median_abv


app = flask.Flask(__name__)

@app.route('/')
@app.route('/index',methods=['GET','POST'])
def index():
	keywords = {'submission': '',
				'error_message': '',
				'selected_not_specified': 'selected="selected"',
				'abv': str(median_abv)}

	if flask.request.method == 'POST':
		try:
			submission = flask.request.form['submission']
		except KeyError:
			submission = ''
		if len(submission)> 10000:
			submission = ''

		try:
			abv_text = flask.request.form['abv']
		except KeyError:
			abv_text = str(median_abv)
		
		try:	
			style = flask.request.form['style']
		except KeyError:
			style = 'not specified'

		keywords['submission']=submission		

		abv = parse_abv(abv_text)
		keywords['abv'] = str(abv)

		parse_style(keywords, style)
		#submission has not been cleaned or marked safe but flask will do that 
		#for these three fields

		#submission is not safe and is being passed back as safe so 
		#the submission field requires handling
		keywords['full_results'] = flask.Markup(build_results_html(submission, abv, style))
		
	return (flask.render_template('index.html',**keywords))


@app.route('/about.html',methods=['GET',])
@app.route('/about',methods=['GET',])
def about():
	return flask.render_template('about.html')

if __name__ == '__main__':
	app.run(debug=True)