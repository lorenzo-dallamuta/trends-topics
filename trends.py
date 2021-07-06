import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

import logging
from datetime import datetime
date = datetime.now()
logging.basicConfig(filename=f'{date}.log',
                    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s in [%(module)s:%(funcName)s:%(lineno)d]', datefmt='%Y-%m-%d,%H:%M:%S', encoding='utf-8', level=logging.INFO)


def list_topics(key='', geo='IT', top=False, options=webdriver.FirefoxOptions()):
    with webdriver.Firefox(options=options) as driver:
        try:
            driver.get(
                f'https://trends.google.com/trends/explore?q={key}&geo={geo}')
            driver.get(
                f'https://trends.google.com/trends/explore?q={key}&geo={geo}')
            assert 'Trends' in driver.title
            assert key in driver.title

            WebDriverWait(driver, 3).until(
                expected_conditions.text_to_be_present_in_element((By.CLASS_NAME, 'fe-atoms-generic-title'), 'Interest by subregion'))

            relatedqueries = driver.find_elements_by_class_name(
                'fe-related-queries')
            relatedquery = [rq for rq in relatedqueries if rq.find_element_by_class_name(
                'fe-atoms-generic-title').text.find('Related topics help_outline') > -1][0]
            topics = [
                rq.text for rq in relatedquery.find_elements_by_class_name('label-text')]
            if top:
                return topics
            next = relatedquery.find_elements_by_class_name(
                'arrow-right-active')
            while (len(next) > 0):
                next[0].click()
                topics.extend(
                    [rq.text for rq in relatedquery.find_elements_by_class_name('label-text')])
                next = relatedquery.find_elements_by_class_name(
                    'arrow-right-active')
            return topics

        except AssertionError as e:
            print(
                f'the query for {key} was timed out by the source')
            logging.exception(repr(e), exc_info=True)
            return None
        except IndexError as e:
            print(
                f'the query for {key} couldn\'t find the target element')
            logging.error(repr(e), exc_info=True)
            return None
        except Exception as e:
            print(
                f'the query for {key} failed for an unknown reason')
            logging.error(repr(e), exc_info=True)
            return None


if __name__ == '__main__':
    key = sys.argv[1] if len(sys.argv) > 1 else ''
    geo = sys.argv[2] if len(sys.argv) > 2 else 'IT'
    top = sys.argv[3] if len(sys.argv) > 3 else False

    opts = webdriver.FirefoxOptions()
    opts.add_argument('--headless')

    topics = list_topics(key, geo, top, options=opts)
    print(topics)
