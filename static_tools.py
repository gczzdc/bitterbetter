import numpy as np
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt

gradient = 'coolwarm'


def generate_gradient(gradient_name=gradient, with_text=False, filename = 'static/gradient.png'):
	gradient = np.linspace(0, 1, 256)
	gradient = np.vstack((gradient, gradient))

	figh = 0.32
	plt.figure(figsize=(6.4, figh))
	ax=plt.gca()

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
	f =ax.get_figure()
	f.savefig(filename, bbox_inches="tight", pad_inches=0, transparent=True)
