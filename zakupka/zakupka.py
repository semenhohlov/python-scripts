from xml.dom.minidom import parse, getDOMImplementation
import datetime

def get_dom(name):
    dom = False
    try:
        dom = parse(name)
    except:
        print('Ошибка чтения файла: ', name)
    return dom

def save_export(dom):
    f = open('export_zakupka.xml', 'w')
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<!DOCTYPE yml_catalog SYSTEM "shops.dtd">\n')
    dom.writexml(f)
    # dom.writexml(f, '', '    ', '\n')
    f.close()
    print('Файл export_zakupka.xml готов для загрузки.')

def minus_cats(dom):
    print('Загрузка категорий.')
    cats = get_dom('categories_minus.xml')
    if not cats:
        print('Ошибка загрузки файла с категориями...')
        return
    minus = []
    catsItems = cats.getElementsByTagName('category')
    for item in catsItems:
        minus.append(str(item.getAttribute('id')))
    impl = getDOMImplementation()
    newdoc = impl.createDocument(None, "offers", None)
    offers = newdoc.documentElement
    itemsList = dom.getElementsByTagName('offer')
    print('Всего позиций:', len(itemsList))
    newItems = 0
    for item in itemsList:
        try:
            catId = str(item.getElementsByTagName('categoryId')[0].childNodes[0].nodeValue)
            minus.index(catId)
        except:
            offers.appendChild(item)
            newItems += 1
    print('Новых позиций:', newItems)
    return offers

def main():
    export = get_dom('zakupka.xml')
    prev = get_dom('prev.xml')
    if not export:
        return
    newItems = minus_cats(export)
    impl = getDOMImplementation()
    newdoc = impl.createDocument(None, "yml_catalog", None)
    yml = newdoc.documentElement
    yml.setAttribute('date', datetime.datetime.now().strftime('{%Y-%m-%d %H:%M}'))
    newdoc = impl.createDocument(None, "shop", None)
    shop = newdoc.documentElement
    yml.appendChild(shop)
    newdoc = impl.createDocument(None, "name", None)
    name = newdoc.documentElement
    name.appendChild(newdoc.createTextNode('Игрушки Никусик - изобилие детского счастья'))
    newdoc = impl.createDocument(None, "company", None)
    company = newdoc.documentElement
    company.appendChild(newdoc.createTextNode('Игрушки Никусик - изобилие детского счастья'))
    newdoc = impl.createDocument(None, "url", None)
    url = newdoc.documentElement
    url.appendChild(newdoc.createTextNode('https://nikusiktoys.prom.ua'))
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
    save_export(yml)

if __name__ == '__main__':
    main()