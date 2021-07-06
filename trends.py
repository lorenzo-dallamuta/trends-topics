import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

import concurrent.futures
import threading

import logging
from datetime import datetime
date = datetime.now()
logging.basicConfig(filename=f'logs/{date.strftime("%m-%d-%Y_%H-%M-%S")}.log',
                    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s in [%(module)s:%(funcName)s:%(lineno)d]', datefmt='%Y-%m-%d,%H:%M:%S', encoding='utf-8', level=logging.INFO)


topics_lock = threading.Lock()


def list_topics(res, key='', geo='IT', full=False, options=webdriver.FirefoxOptions(), capabilities=None, profile=None, lock=topics_lock):
    topics = []
    try:
        with webdriver.Firefox(options=options, capabilities=capabilities) as driver:
            # print(driver.execute_script("return navigator.userAgent"))
            try:
                driver.get(
                    f'https://trends.google.com/trends/explore?q={key}&geo={geo}')
                driver.get(
                    f'https://trends.google.com/trends/explore?q={key}&geo={geo}')
                assert 'Trends' in driver.title
                assert key in driver.title

                # WebDriverWait(driver, 5).until(
                #     expected_conditions.text_to_be_present_in_element((By.CLASS_NAME, 'fe-atoms-generic-title'), 'Interest by subregion'))
                # relatedquery = WebDriverWait(driver, 5).until(
                #     expected_conditions.custom_presence_of_all_elements_located((By.CLASS_NAME, 'fe-atoms-generic-title'), 'Related topics'))
                relatedqueries = WebDriverWait(driver, 5).until(
                    expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, 'fe-related-queries')))

                # relatedqueries = driver.find_elements_by_class_name(
                #     'fe-related-queries')
                relatedquery = [rq for rq in relatedqueries if rq.find_element_by_class_name(
                    'fe-atoms-generic-title').text.find('Related topics help_outline') > -1][0]
                topics = [
                    rq.text for rq in relatedquery.find_elements_by_class_name('label-text')]
                # this could be checked more throughly, but it's probably just this and the html structure for no results is different than the one for results found
                if len(topics) < 1:
                    full = False
                    topics.append(['the search found no results'])
                if full:
                    next = relatedquery.find_elements_by_class_name(
                        'arrow-right-active')
                    while (len(next) > 0):
                        next[0].click()
                        topics.extend(
                            [rq.text for rq in relatedquery.find_elements_by_class_name('label-text')])
                        next = relatedquery.find_elements_by_class_name(
                            'arrow-right-active')
                print(f'the query for {key} was successful')
                logging.info(
                    f'the query for {key} was successful')

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
    except Exception as e:
        print(
            f'the webdriver failed to open')
        logging.error(repr(e), exc_info=True)
        return None
    finally:
        with lock:
            if len(topics < 1):
                topics.append(['there was an error'])
            all_topics = res
            all_topics.append(topics)
            res = all_topics


if __name__ == '__main__':
    keys = sys.argv[1].split(',') if len(sys.argv) > 1 else [
        'first', 'second', 'third']
    geo = sys.argv[2] if len(sys.argv) > 2 else 'IT'
    full = sys.argv[3] if len(sys.argv) > 3 else False

    opts = webdriver.FirefoxOptions()
    opts.add_argument('--headless')

    all_topics = []

    # list_topics(all_topics, key=keys[0], geo=geo, full=full, options=opts)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(lambda key: list_topics(all_topics, key=key,
                     geo=geo, full=full, options=opts), keys)

    print(len(all_topics))
    print(all_topics)


# class custom_presence_of_all_elements_located(object):
#     def __init__(self, locator, text_):
#         self.locator = locator
#         self.text = text_

#     def __call__(self, driver):
#         try:
#             elements = _find_elements(driver, self.locator)
#             for element in elements:
#                 if self.text in element.text:
#                     return element
#             else:
#                 return False
#         except StaleElementReferenceException:
#             return False
