from Mylibs import *

url_1d    = 'http://www.weather.com.cn/weather1d/101181608.shtml'
url_7d    = 'http://www.weather.com.cn/weather/101181608.shtml'
url_15d   = 'http://www.weather.com.cn/weather15d/101181608.shtml'
url_40d   = 'http://www.weather.com.cn/weather40d/101181608.shtml'
data_path = './data/'
figs_path = './figs/'
chromedriver_path = 'chromedriver.exe'

params = {
    'image.origin': 'lower',
    'image.interpolation': 'nearest',
    'figure.autolayout': True,
    'image.cmap': 'magma',
    'axes.grid': False,
    'savefig.dpi': 500,
    'axes.labelsize': 20,
    'axes.titlesize': 20,
    'legend.fontsize': 15,
    'xtick.labelsize': 20,
    'ytick.labelsize': 20,
    'figure.figsize': [18, 6],
    'mathtext.fontset': 'stix',
    'lines.linewidth': 2,
    'font.size': 20,
    'lines.markersize': 6,
    'font.family': 'serif',
    'font.serif': 'SimHei',
    'axes.unicode_minus': False,
}
mpl.rcParams.update(params)