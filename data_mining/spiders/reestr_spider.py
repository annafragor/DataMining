# -*- coding: utf-8 -*-
## @package reestr_spider
# Паук для страницы реестра
import CsvWriter as cw
import scrapy
import re


## @brief Функция, получающая список ссылок
#  @return Список ссылок на страницы реестра, которые считываются из файла 'urls.txt'
def get_urls():
    file = open('urls.txt')
    result = []
    for line in file:
        print('line=', line)
        result.append(line)

    return result

## @brief Объект класса CsvWriter
#  Объект класса CsvWriter, с помощью которого класс ReestrSpider сохраняет полученные
#  со страниц реестра данные в формате .csv
csv_worker = cw.CsvWriter()


## @brief Класс паука
#  @details Класс, который парсит все страницы реестра, вычленяя необходимые данные с каждой из них
class ReestrSpider(scrapy.Spider):
    ## Уникальное название, идентифицирующее паука
    name = "reestr"

    ## @brief Генератор запросов
    #  @return Итерируемый объект, содержащий список объектов scrapy.Request
    def start_requests(self):
        urls = get_urls()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    ## @brief Метод, удаляющий лишние пробельные символы в строке
    #  @param line Строка, которую надо изменить
    #  @return Очищенная от лишних пробелов строка
    #  Этот метод используется для того, чтобы удалять лишние пробелы и символы табуляции,
    #  которые могут встретиться в тексте html-кода страницы, полученного в ответ от сервера.
    @staticmethod
    def delete_spaces(line):
        line = str(line)
        line_cpy = line[:]
        try:
            line = re.sub('\s+', ' ', line)
            line = re.sub('^\s|\s$', '', line)
        except BaseException:
            return line_cpy
        else:
            return line

    ## @brief Парсер ответа с сервера
    #  @param response Объект класса scrapy.http.TextResponse, внутри которого находится содержимое страницы и методы
    #  для дальнейшей обработки ответа сервера.
    #  @details Метод, который вызывается для обработки ответа, получаемого после каждого запроса.
    def parse(self, response):
        divs = response.xpath('//div')

        for i in divs:
            if i.xpath('span/text()').extract_first() == 'Альтернативные наименования:':
                title_alter = i.re('.+</span>\s*(.*)\s*</div>')[0]
                title_alter = self.delete_spaces(title_alter).split('<br>')

                res_title_alter = ''
                if len(title_alter) == 1:  # то есть альтернативное название одно
                    res_title_alter = title_alter[0]

                else:
                    for a in title_alter:
                        res_title_alter = res_title_alter + str(a) + '\n'
                    res_title_alter = res_title_alter[:-2]

                csv_worker.add('title_alter', res_title_alter)

            elif i.xpath('span/text()').extract_first() == 'Дата регистрации:':
                date_start = i.re('.+</span>\s*(.*)\s*</div>')[0]
                csv_worker.add('date_start', self.delete_spaces(date_start))

            elif i.xpath('span/text()').extract_first() == 'Рег. номер ПО:':
                id_txt = i.re('.+</span>\s*(.*)\s*</div>')[0]
                csv_worker.add('id_txt', self.delete_spaces(id_txt))

            elif i.xpath('span/text()').extract_first() == 'Сайт производителя:':
                app_url = i.xpath('.//a/text()').extract_first()
                csv_worker.add('applicant_url', self.delete_spaces(app_url))

            elif i.xpath('span/text()').extract_first() == 'Класс ПО:':
                type_app = i.css('font').xpath('@title').extract()
                res_type_app = ''
                for a in type_app:
                    res_type_app = res_type_app + self.delete_spaces(a) + '\n'

                csv_worker.add('type_app', res_type_app[:-1])

            title = response.css('title::text').extract_first()
            csv_worker.add('title', self.delete_spaces(title))

            app_title = response.xpath('//a[contains(@title, "Все продукты организации")]/text()').extract_first()
            csv_worker.add('applicant_title', self.delete_spaces(app_title))

        csv_worker.save_session()
