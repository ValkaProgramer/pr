import re
import requests
from bs4 import BeautifulSoup

def inClass(url, list, pages):

    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            if url.find('page') == -1:
                url += '?page=1'

            no_top_bottom_boosters = soup.body.find_all('ul', class_='ads-list-photo')[0]
            raw_list_items = no_top_bottom_boosters.find_all('li', class_="ads-list-photo-item")
            list_items = []
            for item in raw_list_items:
                if not ('is-adsense' in item.get('class')) or ('js-booster-inline' in item.get('class')):
                    list_items.append(item)
            for item in list_items:
                if not item.find('div', class_="ads-list-photo-item-thumb"):
                    print(item)
                    print(item.get('class'))

            divs = [item.find('div', class_="ads-list-photo-item-thumb") for item in list_items]

            for item in divs:
                list.append('https://999.md' + item.find('a', href=True).get('href'))

            li = soup.body.find('nav', class_='paginator').find_all('li')
            for item in li:
                if item.get('class') == ['current']:
                    is_last = len(li) == li.index(item) + 1
            new_url = url.partition("=")[0] + '=' + str(int(url.partition("=")[2]) + 1)
            if( (pages == None or int(url.partition("=")[2]) < pages) and not is_last):
                inClass(new_url, list, pages)
        else:
            print(f"GET request failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")