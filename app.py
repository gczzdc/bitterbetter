import flask
from build_results_html import build_results_html, build_bitterness_tables
from parsers import parse_abv, parse_style, median_abv, decode_parsed_style
from graphic_tools import build_distplot_with_line

defined_examples = range(10,16)

app = flask.Flask(__name__)

@app.route('/')
@app.route('/index',methods=['GET','POST'])
def index():
	keywords = {'submission': '',
				'selected_not_specified': 'selected="selected"',
				'abv': str(median_abv)}

	if flask.request.method == 'POST':
		try:
			submission = flask.request.form['submission']
		except KeyError:
			submission = ''
		if len(submission)> 10000:
			submission = submission[:10000]

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
	elif flask.request.method==	'GET':
		example_number = flask.request.args.get('example',None, type=int)
		if example_number in defined_examples:
			with open('static/example_{}'.format(example_number)) as f:
				example_data = f.read()
			example_lines = example_data.split('\n')
			keywords['abv'] = example_lines[0]
			keywords['submission'] = '\n'.join(example_lines[2:])
			parse_style(keywords, example_lines[1])
	return (flask.render_template('index.html',**keywords))


@app.route('/dist_<data>.png')
def dist(data):
	raw_split = data.split('--')
	predicted_ibu = float(raw_split[1])
	style = decode_parsed_style(raw_split[0])
	return flask.send_file(build_distplot_with_line(style,predicted_ibu), attachment_filename='dist_{}.png'.format(data), mimetype='image/png')

@app.route('/about.html',methods=['GET',])
@app.route('/about',methods=['GET',])
def about():
	keywords={}
	keywords['tables']=flask.Markup(build_bitterness_tables())
	return flask.render_template('about.html',**keywords)

if __name__ == '__main__':
	app.run()