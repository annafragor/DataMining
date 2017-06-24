import urllib.request
import re


main_url = 'https://reestr.minsvyaz.ru/reestr'


class UrlReceiver:
    def __init__(self):
        self.main_url = main_url
        self.html_code = ''
        self.answer = None
        self.urls = []
        self.page_num = 0

    def get_html_code(self, url):
        doc = urllib.request.urlopen(url)
        self.answer = doc.read()
        self.html_code = str(self.answer)

        file = open('site.txt', 'w')
        for i in self.html_code:
            file.write(i)

    def get_urls_from_page(self, page_num):
        p = re.compile('<a href="[\w/.]+">')
        res = p.findall(self.html_code)[4:]  # т.к. первые 4 ссылки это /reestr, /request, /rules, /help
        self.urls += res

        file = open('urls.txt', 'a')
        file.write('Page №' + str(page_num) + '\n')
        for i in res:
            if page_num == 123 or page_num == 156:
                file.write(i + '\n')

            i = self.make_url(i)
            file.write(i + '\n')
        file.close()

    @staticmethod
    def make_url(url):
        p = re.compile('[\d]+/')
        m = p.search(url)
        if m:
            return main_url + '/' + m.group()
        else:
            return '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'

    def get_max_page_num(self):
        p = re.compile('<a class="nav_item" href="/reestr/\?PAGEN_1=[\d]+">[^>]')
        res = p.findall(self.html_code)
        p = re.compile('=[\d]+')
        for i in range(len(res)):
            m = p.search(res[i]).group()
            res[i] = int(m[1:])

        self.page_num = max(res)
        print(self.page_num)

    def main_f(self):

        self.get_html_code(main_url)
        self.get_max_page_num()

        for i in range(self.page_num):
            if i != 0:  # если мы не на первой странице
                self.get_html_code(main_url + '/?PAGEN_1=' + str(i + 1))

            self.get_urls_from_page(i+1)


if __name__ == '__main__':
    file = open('urls.txt', 'w')
    file.close()
    worker = UrlReceiver()
    worker.main_f()
