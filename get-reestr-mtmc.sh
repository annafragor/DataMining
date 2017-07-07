#!/usr/bin/env bash

python3 get_urlslist.py
scrapy crawl reestr
python3 print_results.py
