import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import colors

feature_coef_dic = {}

#would be better if seismic were not hard-coded here and below but rather a global variable

def colors_from_coef(coef, vmin = -40, vmax = 40, cmap = cm.seismic, cutoffs = [-6,6]):
    norm = colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    if coef < cutoffs[0] or coef > cutoffs[1]:
        normalized_coef = norm(coef)
        mapped_color = cmap(normalized_coef)
        hex_color = colors.to_hex(mapped_color)
        return hex_color
    else:
        return False


def build_colors_plt(text, feature_coef_dic):
    words = text.split()
    ans_dic ={}    
    for word in words:
        if word in feature_coef_dic:
            coef = feature_coef_dic[word]
            hex_col = colors_from_coef(coef)
            if hex_col:
                ans_dic[word]={'hex_color':hex_col, 'coefficient':coef}
    return ans_dic


def bag_of_words_paragraph(text,features_coef_dic=feature_coef_dic):
    working_dic = build_colors_plt(text,feature_coef_dic)
    words = text.split()
    para = []
    style = []
    counter = 1
    for word in words:
        if word not in working_dic:
            para.append(word)
            para.append(' ')
        else:
            para.append('<span ')
            para.append('class="tooltip"')
            para.append('style="background: ')
            para.append(working_dic[word]['hex_color'])
            para.append('"')
            para.append('>')
            para.append(word)
            para.append('<span ')
            para.append('class="tooltiptext" ')
            para.append('style="color: ')
            para.append(working_dic[word]['hex_color'])           
            para.append('"')
            para.append('>')
            coef = working_dic[word]['coefficient']
            if coef > 0:
                para.append('+')    
            para.append(str(int(coef)))
            para.append('</span >')
            para.append('</span >')
            para.append(' ')
            counter+=1
    final= ''.join(para)
    return final


def best_predictor(text, abv=None, style=None):
	return 35

def generate_gradient(gradient_name='seismic', with_text=True, filename = 'static/gradient.png'):
	gradient = np.linspace(0, 1, 256)
	gradient = np.vstack((gradient, gradient))

	figh = 0.72
	plt.figure(figsize=(6.4, figh))
	ax=plt.gca()

    # axes[0].set_title(cmap_category + ' colormaps', fontsize=14)

	ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(gradient_name))
	if with_text:
		ax.text(.2, 1.3, 'less bitter', 
				va='center', 
				ha='right', 
				fontsize=16, 
				fontname="arial",
				transform=ax.transAxes) 
		ax.text(1, 1.3, 'more bitter', 
				va='center', 
				ha='right', 
				fontsize=16, 
				fontname="arial",
				transform=ax.transAxes) 
    
	ax.set_axis_off()
	# plt.show()

	f =ax.get_figure()
	f.savefig(filename, bbox_inches="tight", transparent=True)