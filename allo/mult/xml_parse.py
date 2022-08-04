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
    if os.path.exists('export_mult.xml'):
        os.rename('export_mult.xml', 'prev.xml')
        print('Переименовую предыдущий export_mult.xml в prev.xml.')

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
    newdoc = impl.createDocument(None, "offers", None)
    offers = newdoc.documentElement
    itemList = dom.getElementsByTagName('offer')
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
        name = name.replace('&qout;', '')
        name = name.replace('&amp;qout;', '')
        name = name.replace('БТ Холодильник', 'Игрушка Холодильник')
        name = re.sub("\(\d*шт\)", "", name)
        nameItem.childNodes[0].nodeValue = name

        # newdoc = impl.createDocument(None, "oldprice", None)
        # oldprice = newdoc.documentElement
        # oldvalue = newdoc.createTextNode(str(value))
        # oldprice.appendChild(oldvalue)
        # item.appendChild(oldprice)
        price.childNodes[0].nodeValue = value
        offers.appendChild(item)
        tmp += 1
        if tmp > percent:
            tmp = 0
            current += 1
            print('\r{}%'.format(current), end='')
    print()
    return offers

def save_export(dom):
    f = open('export_mult.xml', 'w')
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    dom.writexml(f)
    f.close()
    print('Файл export_mult.xml готов для загрузки.')

def append_na_items(export, prev):
    print('Нет в наличии...')
    new_items = []
    na_items = 0
    itemsList = export.getElementsByTagName('offers')[0]
    itemList = export.getElementsByTagName('offer')
    for item in itemList:
        new_items.append(item.getAttribute('id'))
    itemList = prev.getElementsByTagName('offer')
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
    export = get_dom('mult.xml')
    prev = get_dom('prev.xml')
    if export == False:
        return
    newItems = overprice(export, config)

    impl = getDOMImplementation()
    newdoc = impl.createDocument(None, "yml_catalog", None)
    yml = newdoc.documentElement
    yml.setAttribute('date', datetime.datetime.now().strftime('{%Y-%m-%d %H:%M}'))
    newdoc = impl.createDocument(None, "shop", None)
    shop = newdoc.documentElement
    yml.appendChild(shop)
    newdoc = impl.createDocument(None, "name", None)
    name = newdoc.documentElement
    name.appendChild(newdoc.createTextNode('Мультитойз'))
    newdoc = impl.createDocument(None, "company", None)
    company = newdoc.documentElement
    company.appendChild(newdoc.createTextNode('Мультитойз\n'))
    newdoc = impl.createDocument(None, "url", None)
    url = newdoc.documentElement
    url.appendChild(newdoc.createTextNode('http://multitoys.com.ua\n'))
    newdoc = impl.createDocument(None, "currencies", None)
    currencies = newdoc.documentElement
    newdoc = impl.createDocument(None, "currency", None)
    currency = newdoc.documentElement
    currency.setAttribute('id', 'UAH')
    currency.setAttribute('rate', '1')
    currencies.appendChild(currency)
    shop.appendChild(name)
    shop.appendChild(company)
    shop.appendChild(url)
    shop.appendChild(currencies)
    cats = export.getElementsByTagName('categories')[0]
    shop.appendChild(cats)
    shop.appendChild(newItems)

    if prev != False:
        append_na_items(yml, prev)
    save_export(yml)

if __name__ == '__main__':
    main()