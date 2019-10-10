import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def bag_of_words_paragraph(text):
	return ''


def best_predictor(text, abv=None, style=None):
	return 35

def generate_gradient(gradient_name, with_text=True, filename = 'static/gradient.png'):
	gradient = np.linspace(0, 1, 256)
	gradient = np.vstack((gradient, gradient))

	figh = 0.72
	plt.figure(figsize=(6.4, figh))
	ax=plt.gca()

    # axes[0].set_title(cmap_category + ' colormaps', fontsize=14)

	ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap('coolwarm'))
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