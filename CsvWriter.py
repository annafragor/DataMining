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
        ## Значение - <i><b>Регистрационный номер</b></i>
        self.id = ''

        ## Значение - <i><b>Название продукта</b></i>
        self.title = ''

        ## Значение - <i><b>Другие названия продукта</b></i>
        self.alt_title = ''

        ## Значение - <i><b>Дата геристрации в реестре</b></i>
        self.date = ''

        ## Значение - <i><b>Класс ПО</b></i>
        self.type_app = ''

        ## Значение - <i><b>Наименование заявителя</b></i>
        self.app_title = ''

        ## Значение - <i><b>Сайт проивзодителя</b></i>
        self.app_url = ''

        ## Массив всех строк таблицы, соответствующих одному продукту
        self.product_row = []

        ## Файл, куда производится запись всех данных - <i><b>reestr.csv</b></i>
        self.file = open('reestr.csv', 'w', newline='')

        ## Объект класса <i><b>csv.writer</b></i>, с помощью которого производится запись данных
        #  в <i><b>self.reestr</b></i>
        self.writer = csv.writer(self.file,
                                 quoting=csv.QUOTE_MINIMAL)
        self.writer.writerow(['Идентификатор поля', 'id_txt', 'title', 'title_alter', 'date_start',
                              'type_app', 'applicant_title', 'applicant_url'])
        self.writer.writerow(['Тип поля', 'Число', 'Текст', 'Дата', 'Длинный текст', 'Длинный текст', 'Длинный текст'])
        self.writer.writerow(['Описание поля', 'Регистрационный номер', 'Название продукта',
                              'Другие названия продукта', 'Дата регистрации в реестре', 'Класс ПО',
                              'Наименование заявителя', 'Сайт производителя'])

    ## @brief Заполняет переменные строк начальными стандартными данными
    #  @details Таблица для записываемой программы из реестра после выполнения этой функции выглядит так:
    #  ![Empty table](empty_table.jpg)
    def make_start_pack(self):
        self.product_row = []
        self.id = ''
        self.title = ''
        self.alt_title = ''
        self.date = ''
        self.type_app = ''
        self.app_title = ''
        self.app_url = ''

    ## @brief Метод, добавляющий значение в нужное поле
    #  @param self
    #  @param field_id Идентификатор поля
    #  @param value Значение поля
    def add(self, field_id, value):
        if field_id == 'id_txt':
            self.id = value

        elif field_id == 'title':
            self.title = value

        elif field_id == 'title_alter':
            self.alt_title = value

        elif field_id == 'date_start':
            self.date = value

        elif field_id == 'type_app':
            self.type_app = value

        elif field_id == 'applicant_title':
            self.app_title = value

        elif field_id == 'applicant_url':
            self.app_url = value

        else:
            print('There\'s no field_id with such a name!', file=sys.stderr)

    ## @brief Сохранение данных про данную программу из реестра
    #  @details Все значения записываются в массив [product_row](@ref product_row), после чего записываются
    #  в файл <i><b>reestr.csv</b></i>, а затем обнуляются функцией [make_start_pack()](@ref make_start_pack),
    #  чтобы можно было начать обработку последующей программы из реестра.
    def save_session(self):
        self.product_row = [
            self.id,
            self.title,
            self.alt_title,
            self.date,
            self.type_app,
            self.app_title,
            self.app_url,
        ]
        self.writer.writerow(self.product_row)
        self.make_start_pack()
