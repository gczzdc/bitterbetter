import flask
from build_results_html import build_results_html
from math import isnan, isinf

mean_abv = 5.0

app = flask.Flask(__name__)

@app.route('/')
@app.route('/index',methods=['GET','POST'])
def index():
	keywords = {'submission': '',
				'error_message': '',
				'selected_not_specified': 'selected="selected"'}

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
			abv_text = str(mean_abv)
		try:	
			style = flask.request.form['style']
		except KeyError:
			style = 'not specified'
		if style not in style_list:
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


def parse_abv(abv_text):
	try:
		abv_float = float(abv_text)
	except ValueError:
		abv_float = mean_abv
	if isnan(abv_float) or isinf(abv_float):
		abv_float = mean_abv
	return abv_float


def parse_style(keyword_dic, style):
	selected_tag = style
	if style in style_list:
		selected_tag = selected_tag.replace(' ','_')
		selected_tag = selected_tag.replace('/','_')
		selected_tag = selected_tag.replace('-','_')
		selected_tag = 'selected_'+selected_tag
		keyword_dic['selected_not_specified']=''
		keyword_dic[selected_tag]='selected="selected"'


style_list = ["not specified", 
			"Pale Ale - American / APA", 
			"Belgian Ale - Pale / Golden", 
			"Witbier / Belgian White Ale", 
			"IPA - Hazy / NEIPA", 
			"Weissbier - Hefeweizen", 
			"IPA - Black/Brown/Cascadian Dark", 
			"Blonde Ale / Golden Ale", 
			"Brown Ale", 
			"IIPA - Imperial / Double IPA", 
			"IPA", 
			"Red Ale / Intl Amber Ale", 
			"Saison / Farmhouse / Grisette", 
			"ISA - Session IPA", 
			"Wheat Ale", 
			"Stout - Milk / Sweet", 
			"Stout - Imperial", 
			"Pilsener / Pils / Pilsner", 
			"Porter", 
			"Stout", 
			"Sour / Wild Beer"]
			
if __name__ == '__main__':
	app.run(debug=True)