import csv
import sys


## @brief Класс, пишущий данные в `.csv` формат
#  @details Каждая программа из реестра записывается в файл <i><b>reestr.csv</b></i>, и ее описание выглядит
#  следующим образом:
#  ![Table](example_table.jpg)
class CsvWriter:
    ## @brief Конструктор
    #  @details Все переменные, соответствующие строкам таблицы, заполняются функцией
    #  [make_start_pack()](@ref make_start_pack)
    def __init__(self):
        ## Строка таблицы - <i><b>Регистрационный номер</b></i>
        self.id_row = []

        ## Строка таблицы - <i><b>Название продукта</b></i>
        self.title_row = []

        ## Строка таблицы - <i><b>Другие названия продукта</b></i>
        self.alt_title_row = []

        ## Строка таблицы - <i><b>Дата геристрации в реестре</b></i>
        self.date_row = []

        ## Строка таблицы - <i><b>Класс ПО</b></i>
        self.type_app_row = []

        ## Строка таблицы - <i><b>Наименование заявителя</b></i>
        self.app_title_row = []

        ## Строка таблицы - <i><b>Сайт проивзодителя</b></i>
        self.app_url_row = []

        ## Массив всех строк таблицы, соответствующих одному продукту
        self.session_rows = []

        self.make_start_pack()

        ## Файл, куда производится запись всех данных - <i><b>reestr.csv</b></i>
        self.file = open('reestr.csv', 'w', newline='')

        ## Объект класса <i><b>csv.writer</b></i>, с помощью которого производится запись данных
        #  в <i><b>self.file</b></i>
        self.writer = csv.writer(self.file,
                                 quoting=csv.QUOTE_MINIMAL)
        self.writer.writerow(['Идентификатор поля',
                              'Тип поля',
                              'Описание поля',
                              'Значение поля'])

    ## @brief Заполняет переменные строк начальными стандартными данными
    #  @details Таблица для записываемой программы из реестра после выполнения этой функции выглядит так:
    #  ![Empty table](empty_table.jpg)
    def make_start_pack(self):
        self.session_rows = []
        self.id_row = ['id_txt', 'Число', 'Регистрационный номер', '']
        self.title_row = ['title', 'Текст', 'Название продукта', '']
        self.alt_title_row = ['title_alter', 'Текст', 'Другие названия продукта', '']
        self.date_row = ['date_start', 'Дата', 'Дата регистрации в реестре', '']
        self.type_app_row = ['type_app', 'Текст', 'Класс ПО', '']
        self.app_title_row = ['applicant_title', 'Текст', 'Наименование заявителя', '']
        self.app_url_row = ['applicant_url', 'Текст', 'Сайт производителя', '']

    ## @brief Метод, определяющий тип поля
    #  @details Если длина содержимого больше 15 символов, то тип поля будет <i><b>Длинный текст</b></i>,
    #  иначе - <i><b>Текст</b></i>
    @staticmethod
    def field_type(value):
        if len(value) > 15:
            return 'Длинный текст'
        else:
            return 'Текст'

    ## @brief Метод, добавляющий строку с данными
    #  @param self
    #  @param field_id Идентификатор поля
    #  @param value Значение поля
    def add(self, field_id, value):
        # result_row = []
        if field_id == 'id_txt':
            # self.id_row[1] = self.field_type(value)
            self.id_row[-1] = value

        elif field_id == 'title':
            self.title_row[1] = self.field_type(value)
            self.title_row[-1] = value

        elif field_id == 'title_alter':
            self.alt_title_row[1] = self.field_type(value)
            self.alt_title_row[-1] = value

        elif field_id == 'date_start':
            # self.date_row[1] = self.field_type(value)
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

        # if result_row:
        #     result_row.append(value)

    ## @brief Сохранение данных про данную программу из реестра
    #  @details Все строки записываются в массив [session_rows](@ref session_rows), после чего записываются
    #  в файл <i><b>reestr.csv</b></i>, а затем обнуляются функцией [make_start_pack()](@ref make_start_pack),
    #  чтобы можно было начать обработку последующей программы из реестра.
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
