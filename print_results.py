#!/usr/bin/env python3

if __name__ == '__main__':
    file = open('reestr.csv')
    for line in file:
        print(line, end='')
