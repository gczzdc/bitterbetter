from bs4 import BeautifulSoup
from ibu_prediction import bag_of_words_paragraph, best_predictor, get_strongest_and_weakest
from parsers import encode_style
   

def build_results_html(submission,abv,style):
	soup = BeautifulSoup('','html.parser')
	soup.append(soup.new_tag('div'))
	soup.div['style']='margin: 1em auto'
	soup.div.append(soup.new_tag('div'))
	soup.div.div['class']= 'box'

	soup.div.div.append(soup.new_tag('h4'))
	soup.div.div.h4.append('Results')
	
	para = soup.new_tag('div')
	para['style']='text-align: left'
	para.append(soup.new_tag('p'))
	para.p.append(BeautifulSoup(bag_of_words_paragraph(submission),'html.parser'))
	#no verification of safety has been done for submission before passing it to bag_of_words_paragraph

	prediction = best_predictor(submission, abv, style)[0]

	predict_line = soup.new_tag('p')
	predict_line['align']='center'
	predict_line.append('Predicted IBU rating: ')
	predict_line.append(soup.new_tag('strong'))
	#no verification of safety has been done for submission before passing it to best_predictor
	predict_line.strong.append(str(round(prediction,1)))


	contribution=soup.new_tag('p')
	contribution['align']='center'
	content_tag = soup.new_tag('span')
	content_tag['id']='content'
	content_tag['style']='display:inline-block; width:30px'
	contribution.append('Approximate (relative) contribution from selected word: ')
	contribution.append(soup.new_tag('strong'))
	contribution.strong.append(content_tag)

	distribution = soup.new_tag('p')
	distribution.append(soup.new_tag('img'))
	distribution.img['src']='dist_{}--{}.png'.format(encode_style(style),prediction)

	gradient = soup.new_tag('p')
	gradient.append(soup.new_tag('div'))
	gradient.div['class']='imgparent'
	gradient.div.append(soup.new_tag('div'))
	gradient.div.div['style']= 'display:inline-block;width:395px;vertical-align:bottom;line-height:0px;'
	left_p = soup.new_tag('p')
	left_p['class']='alignleft'
	left_p['style']='vertical-align:bottom;line-height:0px'
	left_p.append('less bitter')

	right_p = soup.new_tag('p')
	right_p['class']='alignright'
	right_p.append('more bitter')
	
	gradient.div.div.append(left_p)
	gradient.div.div.append(right_p)


	gradient.div.append(soup.new_tag('img'))
	gradient.div.img['src']='../static/gradient.png'
	gradient.div.img['alt']='gradient legend'


	soup.div.div.append(para)
	soup.div.div.append(predict_line)
	soup.div.div.append(contribution)
	soup.div.div.append(distribution)
	soup.div.div.append(gradient)
	intermezzo = soup.new_tag('div')
	intermezzo['style']='margin-left:auto; margin-right:auto;font-size: 0.8em;'
	intermezzo.append(soup.new_tag('p'))
	intermezzo.p.append('Try changing your description!')
	soup.append(intermezzo)
	return str(soup)

def build_words_table(ordered_tuples):
	tabular_data = BeautifulSoup('','html.parser')
	tabular_data.append(tabular_data.new_tag('table'))
	tabular_data.table.append(tabular_data.new_tag('tr'))
	for tup in ordered_tuples:
		this_row = tabular_data.new_tag('tr')
		gram=tabular_data.new_tag('td')
		gram.append(tup[0])
		weight = tabular_data.new_tag('td')
		weight.append(str(round(tup[1],1)))
		this_row.append(gram)
		this_row.append(weight)
		tabular_data.table.append(this_row)
	return (tabular_data)

def build_bitterness_tables():
	tuples = get_strongest_and_weakest()
	bitter_tuples = (tup for tup in tuples[::-1] if tup[1] > 0)
	nonbitter_tuples = (tup for tup in tuples if tup[1] < 0)
	bitter_table = build_words_table(bitter_tuples)
	nonbitter_table = build_words_table(nonbitter_tuples)

	total_table = BeautifulSoup('','html.parser')
	total_table.append(total_table.new_tag('div'))
	total_table.div['style'] = "margin-left:auto; margin-right:auto; margin-top:20px; margin-bottom:20px; display: table; width:80%;"
	total_table.div.append(total_table.new_tag('div'))
	total_table.div.div['style']="display: table-row"
	
	bitter_cell = total_table.new_tag('div')
	bitter_cell['style']="display: table-cell; width:40%"
	bitter_cell.append(bitter_table)
	total_table.div.div.append(bitter_cell)
	
	nonbitter_cell = total_table.new_tag('div')
	nonbitter_cell['style']="display: table-cell; width:40%"
	nonbitter_cell.append(nonbitter_table)
	total_table.div.div.append(nonbitter_cell)

	return total_table.prettify()


