from bs4 import BeautifulSoup
from ibu_prediction import bag_of_words_paragraph, best_predictor


def build_results_html(submission,abv,style):
	soup = BeautifulSoup('','html.parser')
	soup.append(soup.new_tag('div'))
	soup.div.append(soup.new_tag('div'))
	soup.div.div['class']= 'choice box'
	soup.div.div['style']= 'min-height:280px'
	first_para = soup.new_tag('p')
	#no verification of safety has been done for submission before passing it to bag_of_words_paragraph
	first_para.append(BeautifulSoup(bag_of_words_paragraph(submission),'html.parser'))
	second_para = soup.new_tag('p')
	second_para['align']='center'
	second_para.append('Predicted IBU rating: ')
	second_para.append(soup.new_tag('strong'))
	#no verification of safety has been done for submission before passing it to best_predictor
	second_para.strong.append(str(round(best_predictor(submission, abv, style)[0],1)))
	third_para = soup.new_tag('p')
	third_para.append(soup.new_tag('div'))
	third_para.div['class']='imgparent'
	third_para.div.append(soup.new_tag('div'))
	third_para.div.div['style']= 'display:inline-block;width:395px;vertical-align:bottom;line-height:0px;'
	left_p = soup.new_tag('p')
	left_p['class']='alignleft'
	left_p['style']='vertical-align:bottom;line-height:0px'
	left_p.append('less bitter')

	right_p = soup.new_tag('p')
	right_p['class']='alignright'
	right_p.append('more bitter')
	
	third_para.div.div.append(left_p)
	third_para.div.div.append(right_p)


	third_para.div.append(soup.new_tag('img'))
	third_para.div.img['src']='../static/gradient.png'
	third_para.div.img['alt']='gradient legend'
	soup.div.div.append(first_para)
	soup.div.div.append(second_para)
	soup.div.div.append(third_para)
	return soup.prettify()

