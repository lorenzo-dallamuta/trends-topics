import re
from time import sleep
from random import randint
from selenium import webdriver
from trends import list_topics
from datetime import datetime

opts = webdriver.FirefoxOptions()
opts.add_argument('--headless')

text = "[3]The Philippine Air Force (PAF; Filipino: Hukbong Himpapawid ng Pilipinas) is the aerial warfare service branch of the Armed Forces of the Philippines. Initially formed as part of the Philippine Army (Philippine Army Air Corps), the PAF is responsible for both defending the Philippine airspace, and conducting aerial operations throughout the Philippines, such as close air support operations, combat air patrols, aerial reconnaissance missions, airlift operations, tactical operations and aerial humanitarian operations. The PAF is headquartered at the Villamor Air Base in Pasay, and is headed by the Chief of the Air Force, who also serves as the branch's highest-raking military officer. The PAF has an estimated strength of over 15,000 personnel and operates 203 aircraft"
text += "In 1656, Dutch scientist Christiaan Huygens invented the first pendulum clock. It had a pendulum length of just under a meter which gave it a swing of one second, and an escapement that ticked every second. It was the first clock that could accurately keep time in seconds. By the 1730s, 80 years later, John Harrison's maritime chronometers could keep time accurate to within one second in 100 days. "
text += """Microsoft Corporation is an American multinational technology company which produces computer software, consumer electronics, personal computers, and related services. Its best known software products are the Microsoft Windows line of operating systems, the Microsoft Office suite, and the Internet Explorer and Edge web browsers. Its flagship hardware products are the Xbox video game consoles and the Microsoft Surface lineup of touchscreen personal computers. Microsoft ranked No. 21 in the 2020 Fortune 500 rankings of the largest United States corporations by total revenue
[3] it was the world's largest software maker by revenue as of 2016.[4] It is considered one of the Big Five companies in the U.S. information technology industry, along with Google, Apple, Amazon, and Facebook.
Microsoft(the word being a portmanteau of "microcomputer software"[5]) was founded by Bill Gates and Paul Allen on April 4, 1975, to develop and sell BASIC interpreters for the Altair 8800. It rose to dominate the personal computer operating system market with MS-DOS in the mid-1980s, followed by Microsoft Windows. The company's 1986 initial public offering(IPO), and subsequent rise in its share price, created three billionaires and an estimated 12, 000 millionaires among Microsoft employees. Since the 1990s, it has increasingly diversified from the operating system market and has made a number of corporate acquisitions, their largest being the acquisition of LinkedIn for $26.2 billion in December 2016, [6] followed by their acquisition of Skype Technologies for $8.5 billion in May 2011.[7]
As of 2015, Microsoft is market-dominant in the IBM PC compatible operating system market and the office software suite market, although it has lost the majority of the overall operating system market to Android.[8] The company also produces a wide range of other consumer and enterprise software for desktops, laptops, tabs, gadgets, and servers, including Internet search(with Bing), the digital services market(through MSN), mixed reality(HoloLens), cloud computing(Azure), and software development(Visual Studio).
Steve Ballmer replaced Gates as CEO in 2000, and later envisioned a "devices and services" strategy.[9] This unfolded with Microsoft acquiring Danger Inc. in 2008, [10] entering the personal computer production market for the first time in June 2012 with the launch of the Microsoft Surface line of tablet computers, and later forming Microsoft Mobile through the acquisition of Nokia's devices and services division. Since Satya Nadella took over as CEO in 2014, the company has scaled back on hardware and has instead focused on cloud computing, a move that helped the company's shares reach its highest value since December 1999.[11][12]
Earlier dethroned by Apple in 2010, in 2018 Microsoft reclaimed its position as the most valuable publicly traded company in the world.[13] In April 2019, Microsoft reached the trillion-dollar market cap, becoming the third U.S. public company to be valued at over $1 trillion after Apple and Amazon respectively.[14] As of 2020, Microsoft has the third-highest global brand valuation.[15] """
stripped_text = re.sub('[^A-Za-z0-9]+', ' ', text)

# keys = [word for word in stripped_text]
keys = stripped_text.split()

times = []
failures = 0
for i in range(len(keys)):
    start = datetime.now()
    if list_topics(key=keys[i], options=opts):
        end = datetime.now()
        time = end - start
        times.append((time).seconds * (10 ** 6) + (time).microseconds)
        print(time, start, end)
    else:
        failures += 1
    with open('benchmark.txt', 'w') as f:
        f.write(f'\n{times}\nsuccess rate: {(i + 1 - failures) / (i + 1)}')
    sleep(randint(30, 60))