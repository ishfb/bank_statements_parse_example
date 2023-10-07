# -*- coding: utf-8 -*-

import sys
import re
import argparse

from requests.structures import CaseInsensitiveDict

def change_name(name):
    known_conversions = CaseInsensitiveDict({
        'YANDEX.TAXI MOSCOW RU': 'Яндекс.Такси',
        'YANDEX.TAXI MOSKVA RU': 'Яндекс.Такси',
        'YANDEX.TAXI Gorod Moskva RU': 'Яндекс.Такси',
        'YANDEX.TAXI GOROD MOSKVA RU': 'Яндекс.Такси',
        'yandex.taxi Moskva RU': 'Яндекс.Такси',
        'https://taxi.yandex.ru Moskva RU': 'Яндекс.Такси',
        'HTTPS://TAXI.YANDEX.RU MOSKVA RU': 'Яндекс.Такси',
        'BELKACAR MSK RU': 'Белка Кар',
        'BELKACAR MOSCOW RU': 'Белка Кар',
        'BELKACAR Gorod Moskva RU': 'Белка Кар',
        'YANDEX EDA MOSCOW RU': 'Яндекс.Еда',
        'YANDEX.EDA MOSCOW RU': 'Яндекс.Еда',
        'YANDEX EDA MOSKVA RU': 'Яндекс.Еда',
        'YANDEX.EDA MOSKVA RU': 'Яндекс.Еда',
        'PYATEROCHKA 14635 Sochi RU': 'Продукты в Пятёрочке',
        'PYATEROCHKA 18156 Sochi RU': 'Продукты в Пятёрочке',
        'PYATEROCHKA 19799 SOCHI RU': 'Продукты в Пятёрочке',
        'Urent Yessentuki RU': 'Аренда самоката',
        'UBER.COM Gorod Moskva RU': 'Uber',
        'UBER MOSKVA RU': 'Uber',
        'VKUSVILL 2094 2 MOSCOW RU': 'ВкусВилл',
        'VKUSVILL 2094 4 MOSCOW RU': 'ВкусВилл',
        'VKUSVILL 2094_2 Gorod Moskva RU': 'ВкусВилл',
        'VKUSVILL 2094 3 MOSCOW RU': 'ВкусВилл',
    })
    return known_conversions.get(name, name)

def guess_category(name):
    known_conversions = CaseInsensitiveDict({
        'Telegram Premium': 'Регулярные платежи',
        'Cafe Vstrecha': 'Кафе',
        'Магнит': 'Продукты',
        'YANDEX.TAXI MOSCOW RU': 'Транспорт',
        'Uber': 'Транспорт',
        'Яндекс.Такси': 'Транспорт',
        'Белка Кар': 'Транспорт',
        'Яндекс.Еда': 'Кафе',
    })
    return known_conversions.get(name, '')


def parse_amount(amount):
    return amount.strip().replace('.', ',').replace(' ', '')


def parse_tinkoff(input_file):
    for line in input_file.readlines()[1:]:
        parts = line.strip().split(';')
        date, amount, name = (parts[i][1:-1] for i in (0, 6, -4))

        date = date.split()[0]
        name = change_name(name)
        amount = parse_amount(amount)

        if amount[0] == '-':
            print('{}\t{}\t\t{}\t\t{}'.format(name, date, amount[1:], guess_category(name)))
        else:
            print('{}\t{}\t{}'.format(name, date, amount))

def parse_raiffeisen(input_file):
    for line in input_file.readlines()[1:]:
        parts = line.strip().split(';')
        date, amount, name = (parts[i] for i in (0, 9, 2))

        date = date.split()[0]
        amount = parse_amount(amount)
        name = change_name(name)

        if amount[0] == '-':
            print('{}\t{}\t\t{}\t\t{}'.format(name, date, amount[1:], guess_category(name)))
        else:
            print('{}\t{}\t{}'.format(name, date, amount))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data', nargs='*')
    args = parser.parse_args()

    name_to_func = {
        'raif': parse_raiffeisen,
        'raiffeisen': parse_raiffeisen,
        'tink': parse_tinkoff,
        'tinkoff': parse_tinkoff,
    }

    for data in args.data:
        bank, file = data.strip().split(':')
        with open(file, 'rt', encoding='windows-1251') as f:
            name_to_func[bank](f)

if __name__ == '__main__':
    main()