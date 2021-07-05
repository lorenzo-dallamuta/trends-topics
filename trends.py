
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.headless = True
# driver = webdriver.Chrome(options=chrome_options)

from selenium import webdriver

opts = webdriver.FirefoxOptions()
opts.add_argument('--headless')

with webdriver.Firefox(options=opts) as driver:
    key = 'iphone'
    geo = 'IT'
    driver.get(f'https://trends.google.com/trends/explore?q={key}&geo={geo}')
    driver.get(f'https://trends.google.com/trends/explore?q={key}&geo={geo}')
    assert 'Trends' in driver.title
    assert key in driver.title
