from xml.dom.minidom import parse, getDOMImplementation
import os
import re
import datetime
import json

def load_config():
    try:
        f = open('config.json', 'r')
        config = json.load(f)
        f.close()
        print('Загрузка файла конфигурации "config.json"')
        return config
    except:
        print('Ошибка загрузки файла конфигурации "config.json"')
        return False

def rename_old_price():
    if os.path.exists('export.xml'):
        os.rename('export.xml', 'prev.xml')
        print('Переименовую предыдущий export.xml в prev.xml.')

def get_dom(name):
    dom = False
    try:
        dom = parse(name)
    except:
        print('Ошибка чтения файла: ', name)
    return dom

def overprice(dom, config):
    print('Переоценка...')
    impl = getDOMImplementation()
    # over_pice = 2.20
    # discount = 0.75
    newdoc = impl.createDocument(None, "items", None)
    items = newdoc.documentElement
    itemList = dom.getElementsByTagName('item')
    total = len(itemList)
    percent = int(total / 100)
    current = 1
    tmp = 0
    for item in itemList:
        # prefix + id
        itemId = config['prefix'] + str(item.getAttribute('id'))
        item.setAttribute('id', itemId)
        # price
        price =  item.getElementsByTagName('price')[0]
        value = float(price.childNodes[0].nodeValue)
        value = round(value * config['over_price'])
        if value < config['min_price']:
            tmp += 1
            continue
         # pos_name
        nameItem = item.getElementsByTagName('name')[0]
        name = str(nameItem.childNodes[0].nodeValue).replace('"', '')
        name = name.replace('р/у', 'на радиоуправлении')
        name = name.replace('р.у.', 'на радиоуправлении')
        name = re.sub("\(\d*шт\)", "", name)
        nameItem.childNodes[0].nodeValue = name

        # newdoc = impl.createDocument(None, "oldprice", None)
        # oldprice = newdoc.documentElement
        # oldvalue = newdoc.createTextNode(str(value))
        # oldprice.appendChild(oldvalue)
        # item.appendChild(oldprice)
        price.childNodes[0].nodeValue = value
        items.appendChild(item)
        tmp += 1
        if tmp > percent:
            tmp = 0
            current += 1
            print('\r{}%'.format(current), end='')
    print()
    return items

def save_export(dom):
    f = open('export.xml', 'w')
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    dom.writexml(f)
    f.close()
    print('Файл export.xml готов для загрузки.')

def append_na_items(export, prev):
    print('Нет в наличии...')
    new_items = []
    na_items = 0
    itemsList = export.getElementsByTagName('items')[0]
    itemList = export.getElementsByTagName('item')
    for item in itemList:
        new_items.append(item.getAttribute('id'))
    itemList = prev.getElementsByTagName('item')
    total = len(itemList)
    percent = int(total / 100)
    current = 1
    tmp = 0
    for item in itemList:
        try:
            new_items.index(item.getAttribute('id'))
        except:
            if item.getAttribute('available'):
                item.setAttribute('available', "false")
                itemsList.appendChild(item)
                na_items += 1
        tmp += 1
        if tmp > percent:
            tmp = 0
            current += 1
            print('\r{}%'.format(current), end='')
    print()
    print("Нет в наличии {} позиций.".format(na_items))

def main():
    config = load_config()
    rename_old_price()
    export = get_dom('dream.xml')
    prev = get_dom('prev.xml')
    if export == False:
        return
    newItems = overprice(export, config)
    impl = getDOMImplementation()
    newdoc = impl.createDocument(None, "price", None)
    price = newdoc.documentElement
    price.setAttribute('date', datetime.datetime.now().strftime('{%Y-%m-%d %H:%M}'))
    newdoc = impl.createDocument(None, "name", None)
    name = newdoc.documentElement
    name.appendChild(newdoc.createTextNode('Дримтойс'))
    newdoc = impl.createDocument(None, "company", None)
    company = newdoc.documentElement
    company.appendChild(newdoc.createTextNode('Дримтойс'))
    newdoc = impl.createDocument(None, "url", None)
    url = newdoc.documentElement
    url.appendChild(newdoc.createTextNode('https://dreamtoys-opt.com.ua'))
    newdoc = impl.createDocument(None, "currencies", None)
    currencies = newdoc.documentElement
    newdoc = impl.createDocument(None, "currency", None)
    currency = newdoc.documentElement
    currency.setAttribute('id', 'UAH')
    currency.setAttribute('rate', '1')
    currencies.appendChild(currency)
    price.appendChild(name)
    price.appendChild(company)
    price.appendChild(url)
    price.appendChild(currencies)
    cats = export.getElementsByTagName('categories')[0]
    price.appendChild(cats)
    price.appendChild(newItems)

    if prev != False:
        append_na_items(price, prev)
    save_export(price)

if __name__ == '__main__':
    main()