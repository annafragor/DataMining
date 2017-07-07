#!/usr/bin/env python3
import UrlsReceiver as ur


main_url = 'https://reestr.minsvyaz.ru/reestr'

if __name__ == '__main__':
    file = open('urls.txt', 'w')
    file.close()
    worker = ur.UrlsReceiver(main_url)
    worker.main_f()
