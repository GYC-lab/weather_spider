from Input import *
from Mylibs import *

# 初始化路径
def init_path():
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    if not os.path.exists(figs_path):
        os.mkdir(figs_path)

# 保存网页
def save_html(html):
    with open(data_path+'source_html.html', 'w', encoding='utf-8') as f:
        f.write(html)

# 用format()将结果打印输出
def print_data(final_list):
    
    print("{:^10}\t{:^8}\t{:^8}\t{:^8}\t{:^8}".format('日期', '天气', '最高温度', '最低温度', '风级'))
    
    num = len(final_list)
    for i in range(num):
        final = final_list[i]
        print("{:^10}\t{:^8}\t{:^8}\t{:^8}\t{:^8}".format(final[0], final[1], final[2], final[3], final[4]))

def spilt_temp(temp):
        # 分割字符串
    high_temp, low_temp = temp.split('/')

    # 去除"℃"符号并转换为整数
    high_temp = int(high_temp.replace('℃', ''))
    low_temp = int(low_temp.replace('℃', ''))

    return high_temp, low_temp

# 获取网页信息
def get_html_by_request(url, timeout=30):
    try:
        r = requests.get(url, timeout=timeout)  # 用requests抓取网页信息
        r.raise_for_status()  # 可以让程序产生异常时停止程序
        r.encoding = r.apparent_encoding

        html = r.text
        save_html(html)  # 备份网页
        
        return html
    except:
        return '产生异常'

def get_html_by_selenium(url):

    try:
        # 设置WebDriver路径（例如ChromeDriver）
        driver = webdriver.Chrome(chromedriver_path)

        # 打开网页
        driver.get(url)
        
        # 等待JavaScript加载完成（如果需要）
        driver.implicitly_wait(10)  # 等待10秒

        # 获取页面源码
        html_content = driver.page_source

        # 关闭浏览器
        driver.quit()

        save_html(html_content)  # 备份网页

    except:
        return '产生异常'

    return html_content

# 获取实时天气信息
def get_data_1d(html):

    print('----------------------------------')
    print('实时天气信息：')

    soup = BeautifulSoup(html, 'html.parser')

    # 通过selector定位元素
    element = soup.select_one('#today > div.t > div > div.tem > span')
    temperature = element.text
    element = soup.select_one('#today > div.t > div > p.time > span')
    current_time = element.text[:-2]
    element = soup.select_one('#today > div.t > div > div.zs.w > span')
    wind = element.text
    element = soup.select_one('#today > div.t > div > div.zs.w > em')
    wind_level = element.text

    print('当前时间：', current_time)
    print('当前温度：', temperature)
    print('当前风向：', wind)
    print('当前风级：', wind_level)    

    final_list = []
    temp = [current_time, temperature, wind, wind_level]
    final_list.append(temp)

    return final_list
                            
# 获取7天天气信息
def get_data_7d(html):

    print('----------------------------------')
    print('1~7天天气信息：')

    final_list = []
    soup       = BeautifulSoup(html, 'html.parser')  # 用BeautifulSoup库解析网页
    body       = soup.body
    data       = body.find('div', {'id': '7d'}) # 找到id为7d的div
    ul         = data.find('ul')            # 获取ul(无序列表)部分
    lis        = ul.find_all('li')        # 获取所有的li(列表项)

    # print(lis)

    for day in lis:
        temp_list = []

        date = day.find('h1').string  # 找到日期
        temp_list.append(date)

        info = day.find_all('p')    # 找到所有的p标签
        temp_list.append(info[0].string)

        if info[1].find('span') is None:    # 找到p标签中的第二个值'span'标签——最高温度
            temperature_highest = ' '       # 用一个判断是否有最高温度
        else:
            temperature_highest = info[1].find('span').string
            temperature_highest = temperature_highest.replace('℃', ' ')
            temperature_highest = temperature_highest.replace(' ', '')

        if info[1].find('i') is None:  # 找到p标签中的第二个值'i'标签——最高温度
            temperature_lowest = ' '  # 用一个判断是否有最低温度
        else:
            temperature_lowest = info[1].find('i').string
            temperature_lowest = temperature_lowest.replace('℃', ' ')

        temp_list.append(temperature_highest)  # 将最高气温添加到temp_list中
        temp_list.append(temperature_lowest)  # 将最低气温添加到temp_list中

        wind_scale = info[2].find('i').string  # 找到p标签的第三个值'i'标签——风级，添加到temp_list中
        temp_list.append(wind_scale)

        final_list.append(temp_list)  # 将temp_list列表添加到final_list列表中

    print_data(final_list)
    return final_list

# 获取15天天气信息
def get_data_15d(html):

    print('----------------------------------')
    print('8~15天天气信息：')

    soup       = BeautifulSoup(html, 'html.parser')  # 用BeautifulSoup库解析网页
    body       = soup.body
    data       = body.find('div', {'id': '15d'})
    ul         = data.find('ul')
    lis        = ul.find_all('li')

    # 找到所有的<li>标签
    weather_data = []
    for li in lis:
        date        = li.find('span', class_='time').text   # 日期
        weather     = li.find('span', class_='wea').text    # 天气
        temperature = li.find('span', class_='tem').text    # 温度

        high_temp, low_temp = spilt_temp(temperature)       # 分割字符串

        wind        = li.find('span', class_='wind').text   # 风向
        wind_level  = li.find('span', class_='wind1').text  # 风级

        # 保存提取的数据
        weather_data.append([date, weather, high_temp, low_temp, wind_level])

    print_data(weather_data)
    return weather_data

# 获取40天天气信息
def get_data_40d(html):

    print('----------------------------------')
    print('40天天气信息：')
    
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html, 'html.parser')

    final_list = []

    # 提取历史天气信息（
    weather_rows = soup.find_all('td', class_='history')

    # 遍历每行提取数据
    for row in weather_rows:
        # 提取阳历日期和农历日期
        solar_date = row.find('span', class_='nowday').text
        lunar_date = row.find('span', class_='nongli').text

        # 提取温度信息
        temperatures = row.find('div', class_='w_xian').p
        max_temp     = temperatures.find('span', class_='max').text
        min_temp     = temperatures.find('span', class_='min').text[1:].replace('℃', '')

        # 打印提取的数据
        print(f"日期：{solar_date} ({lunar_date})，温度：{max_temp}/{min_temp}")
        temp = [solar_date, lunar_date, max_temp, min_temp]
        final_list.append(temp)

    weather_rows = soup.find_all('td', class_='obs')

    for row in weather_rows:
        # 提取阳历日期和农历日期
        solar_date = row.find('span', class_='nowday').text
        lunar_date = row.find('span', class_='nongli').text

        # 提取温度信息
        temperatures = row.find('div', class_='w_xian').p
        max_temp = temperatures.find('span', class_='max').text
        min_temp = temperatures.find('span', class_='min').text[1:].replace('℃', '')

        print(f"日期：{solar_date} ({lunar_date})，温度：{max_temp}/{min_temp}")
        temp = [solar_date, lunar_date, max_temp, min_temp]
        final_list.append(temp)

    weather_rows = soup.find_all('td', class_='d15')

    for row in weather_rows:
        # 提取阳历日期和农历日期
        solar_date = row.find('span', class_='nowday').text
        lunar_date = row.find('span', class_='nongli').text

        # 提取温度信息
        temperatures = row.find('div', class_='w_xian').p
        max_temp = temperatures.find('span', class_='max').text
        min_temp = temperatures.find('span', class_='min').text[1:].replace('℃', '')

        print(f"日期：{solar_date} ({lunar_date})，温度：{max_temp}/{min_temp}")
        temp = [solar_date, lunar_date, max_temp, min_temp]
        final_list.append(temp)

    # print('----------------------------------')
    
    weather_rows = soup.find_all('td', class_='next')[1:]

    for row in weather_rows:

        # 提取阳历日期和农历日期
        solar_date = row.find('span', class_='nowday').text
        lunar_date = row.find('span', class_='nongli').text

        # 提取温度信息
        temperatures = row.find('div', class_='w_xian').p
        max_temp = temperatures.find('span', class_='max').text
        min_temp = temperatures.find('span', class_='min').text[1:].replace('℃', '')

        # 打印提取的数据
        print(f"日期：{solar_date} ({lunar_date})，温度：{max_temp}/{min_temp}")
        temp = [solar_date, lunar_date, max_temp, min_temp]
        final_list.append(temp)

    return final_list

# 爬取实时天气信息
def spider_1d(url):

    # 获取网页信息
    html       = get_html_by_selenium(url)

    # 获取天气信息
    final_list = get_data_1d(html)

    # 保存数据
    df = pd.DataFrame(final_list)
    df.columns = ['当前时间', '当前温度', '当前风向', '当前风级']
    df.to_csv(data_path+'data_1d.csv')

# 爬取7天天气信息
def spider_7d(url):

    # 获取网页信息
    html       = get_html_by_request(url)

    # 获取天气信息
    final_list = get_data_7d(html)

    # 保存数据
    df = pd.DataFrame(final_list)
    df.columns = ['日期', '天气', '最高温度', '最低温度', '风级']
    df.to_csv(data_path+'data_7d.csv')

# 爬取15天天气信息
def spider_15d(url):

    # 获取网页信息
    html       = get_html_by_request(url)

    # 获取天气信息
    final_list = get_data_15d(html)

    # 保存数据
    df = pd.DataFrame(final_list)
    df.columns = ['日期', '天气', '最高温度', '最低温度', '风级']
    df.to_csv(data_path+'data_15d.csv')

# 爬取40天天气信息
def spider_40d(url):

    # 获取网页信息
    html       = get_html_by_selenium(url)

    # 获取天气信息
    final_list = get_data_40d(html)

    # 保存数据
    df = pd.DataFrame(final_list)
    df.columns = ['日期', '农历日期', '最高温度', '最低温度']
    df.to_csv(data_path+'data_40d.csv')

# 画图 - 7天天气
def weather_7d():
    # 读取数据
    df = pd.read_csv(data_path+'data_7d.csv')

    high_temp = np.array(df['最高温度'][1:], dtype=int)
    low_temp  = np.array(df['最低温度'])
    days = np.linspace(1, len(low_temp), len(low_temp))
    days_less = np.linspace(2, len(high_temp)+1, len(high_temp))

    # 画图
    plt.figure(figsize=(10, 6))
    plt.plot(days_less, high_temp,'ro-', label='最高温度')
    plt.plot(days, low_temp ,'bo-', label='最低温度')
    plt.xlabel('日期')
    plt.ylabel('温度')
    plt.xticks(days, df['日期'], rotation=45)
    # plt.ylim(0, 20)

    plt.title('温度变化')
    plt.legend()
    # plt.show()
    plt.savefig(figs_path+'7天天气.png')

# 画图 - 8~15天天气
def weather_15d():
    
    # 读取数据
    df = pd.read_csv(data_path+'data_15d.csv')
    df['日期'] = df['日期'].apply(lambda x: x.split('（')[1][:-1])
    high_temp = df['最高温度']
    low_temp  = df['最低温度']

    days = np.linspace(1, len(high_temp), len(high_temp))
    
    # 画图
    plt.figure(figsize=(10, 6))

    plt.plot(days, high_temp,'ro-', label='最高温度')
    plt.plot(days, low_temp, 'bo-', label='最低温度')
    
    plt.xlabel('日期')
    plt.ylabel('温度')
    plt.xticks(days, df['日期'], rotation=45)
    
    plt.title('温度变化')
    plt.legend()
    
    # plt.show()
    plt.savefig(figs_path+'8到15天天气.png')

# 画图 - 40天天气
def weather_40d():
    
    # 读取数据
    df = pd.read_csv(data_path+'data_40d.csv')
    high_temp = df['最高温度']
    low_temp  = df['最低温度']

    days = np.linspace(1, len(high_temp), len(high_temp))
    
    # 画图
    plt.figure(figsize=(10, 6))

    plt.plot(days, high_temp,'ro-', label='最高温度')
    plt.plot(days, low_temp,'bo-', label='最低温度')
    
    plt.xlabel('日期')
    plt.ylabel('温度')
    plt.xticks(days, df['日期'], rotation=45)
    
    plt.title('温度变化')
    plt.legend()
    
    # plt.show()
    plt.savefig(figs_path+'40天天气.png')
