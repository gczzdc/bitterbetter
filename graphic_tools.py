import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib import colors, cm
import seaborn as sns
import io

def color_from_coef(coef, vmin = -40, vmax = 40, cmap = cm.coolwarm, cutoffs = [-6,6]):
    norm = colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    if coef < cutoffs[0] or coef > cutoffs[1]:
        normalized_coef = norm(coef)
        mapped_color = cmap(normalized_coef)
        hex_color = colors.to_hex(mapped_color)
        return hex_color
    else:
        return False

#would be better if color map were not hard-coded but rather a global variable

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



def build_distplot_with_line(style, xval, bins=40, linewidth=3):
    plt.clf()

    ibu_style_df = pd.read_csv('ibu_style_df.csv')
    if style != 'not specified':
        ibu_style_df = ibu_style_df[ibu_style_df['style']==style]
    upper_cap = ibu_style_df['ibu'].quantile(.95)+10
    bin_size = max(1,upper_cap // 19)
    bins = np.arange((-bin_size-1)//2-.5, upper_cap+bin_size,bin_size)
    dist = sns.distplot(ibu_style_df['ibu'], bins=bins, kde_kws={'clip':(0,upper_cap)}, label='style distribution')
    vline = dist.axvline(x=xval, linewidth=linewidth, color='black', label='predicted IBU: {}'.format(round(xval,1)))
    dist.set(yticks=[])
    dist.legend()
    fig = dist.get_figure()
    fig.set_size_inches(8,2)

    img = io.BytesIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    return img