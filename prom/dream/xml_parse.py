from xml.dom.minidom import parse
import os
import re

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

def overprice(dom):
    print('Переоценка...')
    over_pice = 1.87
    desc_begin = '<p>Магазин Никусик порадует вас огромным ассортиментом по доступным ценам! </p><p>'
    desc_end = '</p><p> В нашем магазине обновление товаров - несколько раз в неделю, и вы обязательно подберёте для себя что-нибудь подходящее! А если не знаете, что купить на подарок - звоните или пишите, мы обязательно вам поможем сделать удачный выбор!</p>'
    itemList = dom.getElementsByTagName('item')
    for item in itemList:
        nameItem = item.getElementsByTagName('name')[0]
        name = str(nameItem.childNodes[0].nodeValue).replace('"', '')
        name = name.replace('р/у', 'на радиоуправлении')
        name = re.sub("\(\d*шт\)", "", name)
        nameItem.childNodes[0].nodeValue = name
        price =  item.getElementsByTagName('price')[0]
        value = float(price.childNodes[0].nodeValue)
        price.childNodes[0].nodeValue = round(value * over_pice)
        desc = item.getElementsByTagName('description')[0]
        desc_text = desc.childNodes[0].nodeValue
        desc.childNodes[0].nodeValue = desc_begin + desc_text + desc_end

def save_export(dom):
    f = open('export.xml', 'w')
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
    for item in itemList:
        try:
            new_items.index(item.getAttribute('id'))
        except:
            if item.getAttribute('available'):
                item.setAttribute('available', False)
                itemsList.appendChild(item)
                na_items += 1
    print("Нет в наличии {} позиций.".format(na_items))

def dom_parser():
    dom = parse('dream.xml')
    priceList = dom.getElementsByTagName('price')[0]
    itemList = dom.getElementsByTagName('item')
    print('Total items:', itemList.length)
    for item in itemList:
        price =  item.getElementsByTagName('price')[0]
        value = float(price.childNodes[0].nodeValue)
        price.childNodes[0].nodeValue = round(value * 1.87)
    f = open('export.xml', 'w')
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    priceList.writexml(f)
    f.close()

def main():
    rename_old_price()
    export = get_dom('dream.xml')
    prev = get_dom('prev.xml')
    if export == False:
        return
    overprice(export)
    if prev != False:
        append_na_items(export, prev)
    save_export(export)

if __name__ == '__main__':
    main()