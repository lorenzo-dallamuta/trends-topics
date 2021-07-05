from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

opts = webdriver.FirefoxOptions()
opts.add_argument('--headless')

with webdriver.Firefox(options=opts) as driver:
    key = 'iphone'
    geo = 'IT'
    driver.get(f'https://trends.google.com/trends/explore?q={key}&geo={geo}')
    driver.get(f'https://trends.google.com/trends/explore?q={key}&geo={geo}')
    assert 'Trends' in driver.title
    assert key in driver.title

    # relatedqueries = WebDriverWait(driver, 3).until(
    #     expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, 'fe-atoms-generic-title')))
    WebDriverWait(driver, 3).until(
        expected_conditions.text_to_be_present_in_element((By.CLASS_NAME, 'fe-atoms-generic-title'), 'Interest by subregion'))
    # WebDriverWait(driver, 3).until(
    #     expected_conditions.text_to_be_present_in_element((By.CLASS_NAME, 'fe-atoms-generic-title'), 'Related topics help_outline'))

    relatedqueries = driver.find_elements_by_class_name('fe-related-queries')
    relatedquery = [rq for rq in relatedqueries if rq.find_element_by_class_name(
        'fe-atoms-generic-title').text.find('Related topics help_outline') > -1][0]
    topics = [
        rq.text for rq in relatedquery.find_elements_by_class_name('label-text')]
    next = relatedquery.find_elements_by_class_name('arrow-right-active')
    while (len(next) > 0):
        next[0].click()
        topics.extend(
            [rq.text for rq in relatedquery.find_elements_by_class_name('label-text')])
        next = relatedquery.find_elements_by_class_name(
            'arrow-right-active')
    print(topics)
