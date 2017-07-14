#!/usr/bin/env python3
## @package get_urlslist
#  @brief Модуль получения списка ссылок
#  @details С помощью класса [UrlsReceiver](@ref UrlsReceiver.UrlsReceiver) получается список ссылок на программы,
#  зарегистрированные в реестре, которые записываются в файл <b><i>urls.txt</i></b>
import UrlsReceiver as ur

## Ссылка на первую страницу реестра
main_url = 'https://reestr.minsvyaz.ru/reestr'

if __name__ == '__main__':
    file = open('urls.txt', 'w')
    file.close()
    worker = ur.UrlsReceiver(main_url)
    worker.parse_reestr()
