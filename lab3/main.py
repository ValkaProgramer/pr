import re
import requests
from bs4 import BeautifulSoup
from homework import homework
from in_class import inClass

# Replace with the URL you want to GET
url = "https://999.md/ru/list/computers-and-office-equipment/cases-and-power-supplies-ups"


# def info(url):
#     try:
#         response = requests.get(url)

#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')

#             general_info_div = soup.body.find('div', class_='adPage__content__features')
            
#             lists = general_info_div.find_all('ul')
#             raw_list_items = [item.find_all('li') for item in lists]
#             list_items = []
#             for item in raw_list_items[0]:
#                 list_items.append(item)
            
#             information = []
#             for item in list_items:
#                 # print(item)
#                 key = item.find('span', class_='adPage__content__features__key')
#                 value = item.find('span', 'adPage__content__features__value')
#                 value = value.find('a').string if not value.string else value
#                 information.append([key.string, value.string])
#             for item in information:
#                 print(item)

#         else:
#             print(f"GET request failed with status code: {response.status_code}")

#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")

#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")


# def webcrawler(url, list, pages):

#     try:
#         response = requests.get(url)

#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')

#             if url.find('page') == -1:
#                 url += '?page=1'

#             no_top_bottom_boosters = soup.body.find_all('ul', class_='ads-list-photo')[0]
#             raw_list_items = no_top_bottom_boosters.find_all('li', class_="ads-list-photo-item")
#             list_items = []
#             for item in raw_list_items:
#                 if not ('is-adsense' in item.get('class')) or ('js-booster-inline' in item.get('class')):
#                     list_items.append(item)
#             for item in list_items:
#                 if not item.find('div', class_="ads-list-photo-item-thumb"):
#                     print(item)
#                     print(item.get('class'))

#             divs = [item.find('div', class_="ads-list-photo-item-thumb") for item in list_items]

#             for item in divs:
#                 list.append('https://999.md' + item.find('a', href=True).get('href'))

#             li = soup.body.find('nav', class_='paginator').find_all('li')
#             for item in li:
#                 if item.get('class') == ['current']:
#                     is_last = len(li) == li.index(item) + 1
#             new_url = url.partition("=")[0] + '=' + str(int(url.partition("=")[2]) + 1)
#             if( (pages == None or int(url.partition("=")[2]) < pages) and not is_last):
#                 webcrawler(new_url, list, pages)
#         else:
#             print(f"GET request failed with status code: {response.status_code}")

#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")

#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

some_list = []
inClass(url, some_list, 1)

ready_list = []
for item in some_list:
    # homework(item)
    if item.find('booster') == -1:
        ready_list.append(item)

f = open("links.txt", "w")

for item in ready_list:
    f.write(item + '\n')
# for item in ready_list:
#     f.write(item)
#     for props in homework(item):
#         for prop in props:
#             f.write(prop)
#     f.write('\n')

f.close()