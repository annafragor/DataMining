#!/usr/bin/env python3
## @package print_results
#  @brief Модуль вывода результатов в консоль из файла <b><i>reestr.csv</i></b>

if __name__ == '__main__':
    file = open('reestr.csv')
    for line in file:
        print(line, end='')
