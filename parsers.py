from math import isnan, isinf

median_abv = 6.0

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

def parse_abv(abv_text):
	try:
		abv_float = float(abv_text)
	except ValueError:
		abv_float = median_abv
	if isnan(abv_float) or isinf(abv_float):
		abv_float = median_abv
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
	else:
		style = 'not specified'
