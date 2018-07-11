import requests
from bs4 import BeautifulSoup
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from browser_util import wait_for_page_load
from browser_util import PageController


class KiprisSearch:

    def __init__(self):
        self.prev_query = ''
        self.data = {
            'remoconExpression': '',
            'remoconDocsFound': '',
            'remoconSelectedArticles': '',
            'remoconByBookMark': '',
            'piField': '',
            'piValue': '',
            'piSearchYN': 'N',
            'queryText': '',
            'searchInResultCk': 'undefined',
            'next': 'SimpleListTM',
            'passwd': '',
            'expression': 'KW=[]',
            'beforeExpression': 'KW=[]',
            'query': 'KW=[]',
            'rights': 'TM',
            'userId': '',
            'config': 'G11111111111111111SX11111110011111100',
            'sortField': '',
            'sortState': '',
            'configChange': 'N',
            'searchInTrans': 'N',
            'searchInResut': 'N',
            'searchInComplate': 'N',
            'searchWithSoundex': '',
            'strstat': 'TOP|KW',
            'paging': '0',
            'maxCount': '0',
            'numPageLinks': '10',
            'currentPage': '10',
            'natlCD': 'null',
            'docsFound': '0',
            'bookMarkScreen': '',
            'bookMark': '',
            'bookMarkCnt': '0',
            'NWBOOKMARK': '',
            'BOOKMARK': '',
            'FROM': '',
            'collections': '',
            'myMerchandises': '',
            'numPerPage': '30',
            'sortState1': '',
            'sortState2': '',
            'sortField1': '',
            'sortField2': '',
            'submitFlag': 'N',
            'searchFg': 'Y',
            'SEL_PAT': 'TM',
            'searchKeyword': '',
            'merchandiseString': 'td40,td41,td42,td43,td44,td45,td47,td48,tdmd,',
            'measureString': 'A,B,C,F,G,I,J,R,',
            'patternString': 'NAKletter,NAKfigure,NAKlmixed,NAKfmixed,NAKsounds,NAKfragre,TPDcommon,TPDcolors,TPDcolor,TPDdimens,TPDcmixed,TPDdimcol,TPDhologr,TPDaction,TPDvisual,TPDinvisible,',
            'collectionValues': '',
            'selectedLang': '',
            'lang': '',
            'searchInTransCk': 'undefined'
        }

    def __make_query_data(self, query_text, class_text):
        if class_text != '':
            class_text = class_text.replace(', ', '+', 10)
            class_text = class_text.replace('-', '+', 10)
            query = 'TN=[' + query_text + ']*TC=[' + class_text + ']'
        else:
            query = 'TN=[' + query_text + ']'

        self.data['queryText'] = query
        self.data['expression'] = query
        self.data['query'] = query
        self.data['beforeExpression'] = self.prev_query
        self.prev_query = query
        print(' - send query: ' + query)

    def __send_request_and_get_total(self):
        response = requests.post('http://kdtj.kipris.or.kr/kdtj/grrt1000a.do?method=searchTM', data=self.data)
        bs = BeautifulSoup(response.text, 'html.parser')
        total_elem = bs.find('span', attrs={'class': 'total'})
        # print(total_elem.text)
        if total_elem is None:
            return '0'
        else:
            return total_elem.text

    def request_get_total(self, query_text, class_text):
        if query_text == '':
            return ''

        self.__make_query_data(query_text, class_text)
        return self.__send_request_and_get_total()


class KiprisCrawler:

    def __init__(self, sleep_time):
        self.per_page = 30
        self.data = []
        self.sleep_time = sleep_time

    def __enter__(self):
        # open browser
        self.browser = webdriver.Chrome(executable_path='chromedriver')
        self.browser.get('http://kdtj.kipris.or.kr/kdtj/searchLogina.do?method=loginTM')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.quit()

    def __wait_for_page(self):
        sleep(self.sleep_time)

    def __load_page(self, page_num):
        # with wait_for_page_load(self.browser):
        page_script = 'SetPageAjax(' + str(page_num) + ')'
        self.browser.execute_script(page_script)
        self.__wait_for_page()

    def __crawling(self):
        content_element = self.browser.find_element_by_id('listForm')

        articles = content_element.find_elements_by_tag_name('article')
        # print(len(articles))

        for article in articles:
            title = article.find_element_by_class_name('stitle').text
            content = article.find_element_by_class_name('search_info_list').text
            self.data.append([title, content])

    def __get_items_count(self):
        try:
            content_element = self.browser.find_element_by_id('listForm')
        except NoSuchElementException as exception:
            print('no data')
            return 0

        str_num = content_element.find_element_by_class_name('total').text
        str_num = str_num.replace(',', '', 1)
        return int(str_num)

    def __get_pages_count(self, item_count):
        page_count = item_count / self.per_page
        if item_count % self.per_page > 0:
            page_count = int(page_count) + 1
        return page_count

    def execute(self, query_text):

        # search
        self.browser.find_element_by_id('queryText').clear()
        self.browser.find_element_by_id('queryText').send_keys(query_text)
        self.browser.execute_script('DoSearch()')
        self.__wait_for_page()

        item_count = self.__get_items_count()
        if item_count == 0:
            return -1

        print('items : ' + str(item_count))
        page_count = self.__get_pages_count(item_count)
        print('pages : ' + str(page_count))

        # recursively page load
        for page_num in range(1, page_count + 1):
            print('page number : ' + str(page_num))
            self.__load_page(page_num)
            self.__crawling()


# with KiprisCrawler() as crawler:
#     crawler.execute('abcd')
#     sleep(10)
#     print('abcd')

# kip = KiprisSearch(3)
# print(kip.request_get_total('abcd'))
# print(kip.request_get_total('temp'))
