import urllib.request
import ssl
import re


## @brief Получатель списка ссылок
#  @details Класс, с помощью которого можно получить список ссылок на все российские прораммы
#  для ЭВМ и БД из единого реестра <i><b>https://reestr.minsvyaz.ru/reestr/</b></i>
class UrlsReceiver:
    ## @brief Конструктор
    #  @param self
    #  @param main_url Ссылка на первую страницу реестра, с которой потом будет осуществляться
    #  переход на остальные страницы
    def __init__(self, main_url):
        ## Ссылка, которой инициализируется класс
        self.main_url = main_url

        ## Текст, обрабатываемой страницы
        self.html_code = ''

        ## Массив ссылок с одной страницы реестра
        self.urls = []

        ## Количество страниц в реестре
        self.page_num = 0

        ## Переменная, для запросов к страницам
        self.context = ssl._create_unverified_context()

    ## @brief Метод, получающий <i><b>html</b></i>-кода страницы
    #  @param self
    #  @param url Ссылка на страницу, html-код которой необходимо получить
    #  @details html-код страницы получается с помощью библиотеки <i><b>urllib.request</b></i>. Далее он
    #  записывается в поле <i><b>self.html_code</b></i>.
    def get_html_code(self, url):
        doc = urllib.request.urlopen(url, context=self.context)
        # self.answer = doc.read()
        answer = doc.read()
        # self.html_code = str(self.answer)
        self.html_code = str(answer)

    ## @brief Метод, собирающий ссылки с одной страницы
    #  @param self
    #  @param page_num Номер страницы реестра, с которой получается список ссылок
    #  @details Внутри метода составлено регулярное выражение, по которому выбираются все ссылки в
    #  html-коде страницы, после чего записываются в файл <i><b>urls.txt</b></i>. После обработки очередной
    #  страницы в стандартный вывод пишется ее номер.
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

    ## @brief Метод, приводящий в нормальный вид ссылку, полученную из html-кода страницы
    #  @param url Строка вида <i><b>/reestr/123456/</b></i>
    #  @return Ссылку вида <i><b>https://reestr.minsvyaz.ru/reestr/123456</b></i>
    def make_url(self, url):
        p = re.compile('[\d]+/')
        m = p.search(url)
        if m:
            return self.main_url + '/' + m.group()
        else:
            return 'Mistake!'

    ## @brief Метод, получающий количество страниц в реестре
    #  @details В переменную <i><b>self.page_num</b></i> записывается число страниц в реестре с ссылками на
    #  ПО
    def get_max_page_num(self):
        p = re.compile('<a class="nav_item" href="/reestr/\?PAGEN_1=[\d]+">[^>]')
        res = p.findall(self.html_code)
        p = re.compile('=[\d]+')
        for i in range(len(res)):
            m = p.search(res[i]).group()
            res[i] = int(m[1:])

        self.page_num = max(res)

    ## @brief Главный метод
    #  @details Метод, после запуска которого последовательно обходятся все страницы с ссылками реестра,
    #  с которых в файл <i><b>urls.txt</b></i> записываются ссылки на продукты, каждую из которых впоследствии
    #  надо будет обработать и составить <i><b>.csv</b></i>-файл
    def parse_reestr(self):
        self.get_html_code(self.main_url)
        self.get_max_page_num()

        print('Начинаем получение списка ссылок со всех ', self.page_num, ' страниц реестра.')
        for i in range(self.page_num):
            if i != 0:  # если мы не на первой странице
                self.get_html_code(self.main_url + '/?PAGEN_1=' + str(i + 1))

            self.get_urls_from_page(i+1)
