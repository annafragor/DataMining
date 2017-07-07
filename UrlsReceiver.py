import urllib.request
import ssl
import re


class UrlsReceiver:
    def __init__(self, main_url):
        self.main_url = main_url
        self.html_code = ''
        self.answer = None
        self.urls = []
        self.page_num = 0
        self.context = ssl._create_unverified_context()

    def get_html_code(self, url):
        doc = urllib.request.urlopen(url, context=self.context)
        self.answer = doc.read()
        self.html_code = str(self.answer)

    def get_urls_from_page(self, page_num):
        p = re.compile('<a href="/reestr/[\d]+/">')
        res = p.findall(self.html_code)
        self.urls += res

        file = open('urls.txt', 'a')
        for i in res:
            i = self.make_url(i)
            file.write(i + '\n')
        print('Страница №' + str(page_num) + ' обработана.')
        file.close()

    def make_url(self, url):
        p = re.compile('[\d]+/')
        m = p.search(url)
        if m:
            return self.main_url + '/' + m.group()
        else:
            return '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'

    def get_max_page_num(self):
        p = re.compile('<a class="nav_item" href="/reestr/\?PAGEN_1=[\d]+">[^>]')
        res = p.findall(self.html_code)
        p = re.compile('=[\d]+')
        for i in range(len(res)):
            m = p.search(res[i]).group()
            res[i] = int(m[1:])

        self.page_num = max(res)

    def main_f(self):

        self.get_html_code(self.main_url)
        self.get_max_page_num()

        print('Начинаем получение списка ссылок со всех ', self.page_num, ' страниц реестра.')
        for i in range(self.page_num):
            if i != 0:  # если мы не на первой странице
                self.get_html_code(self.main_url + '/?PAGEN_1=' + str(i + 1))

            self.get_urls_from_page(i+1)
