from xml.dom.minidom import parse, getDOMImplementation
import os

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

def overprice(dom):
    print('Переоценка...')
    impl = getDOMImplementation()
    over_pice = 2.20
    discount = 0.75
    itemList = dom.getElementsByTagName('offer')
    for item in itemList:
        price =  item.getElementsByTagName('price')[0]
        value = float(price.childNodes[0].nodeValue)
        value = round(value * over_pice)
        newdoc = impl.createDocument(None, "oldprice", None)
        oldprice = newdoc.documentElement
        oldvalue = newdoc.createTextNode(str(value))
        oldprice.appendChild(oldvalue)
        price.childNodes[0].nodeValue = round(value * discount)
        item.appendChild(oldprice)

def save_export(dom):
    f = open('export_mult.xml', 'w')
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
    for item in itemList:
        try:
            new_items.index(item.getAttribute('id'))
        except:
            if item.getAttribute('available'):
                item.setAttribute('available', False)
                itemsList.appendChild(item)
                na_items += 1
    print("Нет в наличии {} позиций.".format(na_items))

def main():
    rename_old_price()
    export = get_dom('mult.xml')
    prev = get_dom('prev.xml')
    if export == False:
        return
    overprice(export)
    if prev != False:
        append_na_items(export, prev)
    save_export(export)

if __name__ == '__main__':
    main()