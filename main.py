from Mylibs import *
from Funcs import *
from Input import *

# 模块一 - 爬虫
def spider():

    spider_1d(url_1d)
    spider_7d(url_7d)
    spider_15d(url_15d)
    spider_40d(url_40d)

# 模块二 - 数据可视化
def visualize():

    # weather_7d()    
    weather_15d()
    # weather_40d()

if __name__ == '__main__':
    
    init_path() # 初始化路径
    spider()    # 爬虫
    visualize() # 数据可视化
