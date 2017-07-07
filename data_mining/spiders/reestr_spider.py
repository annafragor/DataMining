# -*- coding: utf-8 -*-
import scrapy
import re
import CsvWriter as cw


def get_urls():
    file = open('urls.txt')
    result = []
    for line in file:
        print('line=', line)
        result.append(line)

    return result

csv_worker = cw.CsvWriter()


class ReestrSpider(scrapy.Spider):
    name = "reestr"

    def start_requests(self):
        urls = get_urls()
        print(urls)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    @staticmethod
    def _delete_spaces(line):
        line = re.sub('\s+', ' ', line)
        return re.sub('^\s|\s$', '', line)

    def parse(self, response):
        divs = response.xpath('//div')

        for i in divs:
            if i.xpath('span/text()').extract_first() == 'Альтернативные наименования:':
                title_alter = i.re('.+</span>\s*(.*)\s*</div>')[0]
                title_alter = self._delete_spaces(title_alter).split('<br>')

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
                csv_worker.add('date_start', self._delete_spaces(date_start))

            elif i.xpath('span/text()').extract_first() == 'Рег. номер ПО:':
                id_txt = i.re('.+</span>\s*(.*)\s*</div>')[0]
                csv_worker.add('id_txt', self._delete_spaces(id_txt))

            elif i.xpath('span/text()').extract_first() == 'Сайт производителя:':
                app_url = i.xpath('.//a/text()').extract_first()
                csv_worker.add('applicant_url', self._delete_spaces(app_url))

            elif i.xpath('span/text()').extract_first() == 'Класс ПО:':
                type_app = i.css('font').xpath('@title').extract()
                res_type_app = ''
                for a in type_app:
                    res_type_app = res_type_app + self._delete_spaces(a) + '\n'

                csv_worker.add('type_app', res_type_app[:-1])

            title = response.css('title::text').extract_first()
            csv_worker.add('title', self._delete_spaces(title))

            app_title = response.xpath('//a[contains(@title, "Все продукты организации")]/text()').extract_first()
            csv_worker.add('applicant_title', self._delete_spaces(app_title))

        csv_worker.save_session()
