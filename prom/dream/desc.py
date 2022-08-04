from xml.dom.minidom import parse
import requests
from time import sleep
from bs4 import BeautifulSoup

def get_dom(name):
    dom = False
    try:
        dom = parse(name)
    except:
        print('Ошибка чтения файла: ', name)
    return dom

def get_desc(xml):
    itemList = xml.getElementsByTagName('item')
    count = 0
    for item in itemList:
        url = item.getElementsByTagName('url')[0].childNodes[0].nodeValue
        # result = requests.get('https://dreamtoys-opt.com.ua/almaznaya-mozaika-3040sm-v-kor-53/').content
        result = requests.get(url).content
        soup = BeautifulSoup(result, 'html.parser')
        print(soup.title.string)
        desc_div = soup.find(attrs={"class": "product-bottom__item tabs__item"})
        print(desc_div.string.lstrip())
        count += 1
        sleep(2)
        if count >= 10:
            break

def main():
    xml = get_dom('dream.xml')
    if not xml:
        return
    get_desc(xml)

if __name__ == '__main__':
    main()
