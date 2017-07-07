import csv
import sys


class CsvWriter:
    def __init__(self):
        self.id_row = []
        self.title_row = []
        self.alt_title_row = []
        self.date_row = []
        self.type_app_row = []
        self.app_title_row = []
        self.app_url_row = []
        self.session_rows = []
        self.make_start_pack()

        self.file = open('reestr.csv', 'w', newline='')
        self.writer = csv.writer(self.file,
                                 # quotechar='|',
                                 quoting=csv.QUOTE_MINIMAL)
        self.writer.writerow(['Идентификатор поля',
                              'Тип поля',
                              'Описание поля',
                              'Значение поля'])

    def make_start_pack(self):
        self.session_rows = []
        self.id_row = ['id_txt', 'Число', 'Регистрационный номер', '']
        self.title_row = ['title', 'Текст', 'Название продукта', '']
        self.alt_title_row = ['title_alter', 'Текст', 'Другие названия продукта', '']
        self.date_row = ['date_start', 'Дата', 'Дата регистрации в реестре', '']
        self.type_app_row = ['type_app', 'Текст', 'Класс ПО', '']
        self.app_title_row = ['applicant_title', 'Текст', 'Наименование заявителя', '']
        self.app_url_row = ['applicant_url', 'Текст', 'Сайт производителя', '']

    @staticmethod
    def field_type(value):
        if len(value) > 15:
            return 'Длинный текст'
        else:
            return 'Текст'

    def add(self, field_id, value):
        result_row = []
        if field_id == 'id_txt':
            self.id_row[1] = self.field_type(value)
            self.id_row[-1] = value

        elif field_id == 'title':
            self.title_row[1] = self.field_type(value)
            self.title_row[-1] = value

        elif field_id == 'title_alter':
            self.alt_title_row[1] = self.field_type(value)
            self.alt_title_row[-1] = value

        elif field_id == 'date_start':
            self.date_row[1] = self.field_type(value)
            self.date_row[-1] = value

        elif field_id == 'type_app':
            self.type_app_row[1] = self.field_type(value)
            self.type_app_row[-1] = value

        elif field_id == 'applicant_title':
            self.app_title_row[1] = self.field_type(value)
            self.app_title_row[-1] = value

        elif field_id == 'applicant_url':
            self.app_url_row[1] = self.field_type(value)
            self.app_url_row[-1] = value

        else:
            print('There\'s no field_id with such a name!', file=sys.stderr)
            result_row = []

        if result_row:
            result_row.append(value)

    def save_session(self):
        self.session_rows = [
            self.id_row,
            self.title_row,
            self.alt_title_row,
            self.date_row,
            self.type_app_row,
            self.app_title_row,
            self.app_url_row,
            []
        ]
        self.writer.writerows(self.session_rows)
        self.make_start_pack()
