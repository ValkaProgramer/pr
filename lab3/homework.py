import re
import requests
from bs4 import BeautifulSoup

def homework(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            general_info_div = soup.body.find('div', class_='adPage__content__features')
            
            lists = general_info_div.find_all('ul')
            raw_list_items = [item.find_all('li') for item in lists]
            list_items = []
            for item in raw_list_items[0]:
                list_items.append(item)
            
            information = []
            for item in list_items:
                # print(item)
                key = item.find('span', class_='adPage__content__features__key')
                value = item.find('span', 'adPage__content__features__value')
                value = value.find('a').string if not value.string else value
                information.append([key.string, value.string])
            for item in information:
                print(item)

        else:
            print(f"GET request failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")