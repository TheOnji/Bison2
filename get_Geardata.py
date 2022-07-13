from bs4 import BeautifulSoup as bfs
import lxml
import requests
from tqdm import tqdm
import json
import logging
import streamlit as st
import numpy as np

#---------------Logger setup----------------#
logger = logging.getLogger(__name__)

file_handler = logging.FileHandler(f"Bison2.log")
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

#Levels
#NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
logger.setLevel(logging.DEBUG)
file_handler.setLevel(logging.ERROR)
stream_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

#Disable all logging
#logging.disable(logging.CRITICAL)
#-----------Logger setup finished------------#


def main():
    UpdateData(Gear = 600, Food = 580, st_enable = False)
    #developer("https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=5&category3=46&min_item_lv=580")
    #developer('https://na.finalfantasyxiv.com/lodestone/playguide/db/item/b71da5422ab/')


def UpdateData(Gear = 600, Food = 580, Load_area = None, st_enable = True):

    if st_enable:
        with Load_area:
            st.markdown("""---""") 
            st.text('Updating database...')

    #-------------------------URLs-------------------------#

    All_gear_url = {'Gear 1':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3&min_item_lv={Gear}",
                    'Gear 2': f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3&page=2&min_item_lv={Gear}",
                    'Accessories': f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=4&min_item_lv={Gear}",
                    'Weapons 1': f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=1&min_item_lv={Gear}",
                    'Weapons 2': f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=1&page=2&min_item_lv={Gear}"}

    All_food_url = {'Food':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=5&category3=46&min_item_lv={Food}"}

    with open('All_gear_url.json', 'w') as file:
        json.dump(All_gear_url, file)

    with open('All_food_url.json', 'w') as file:
        json.dump(All_food_url, file)

    Gear_urls = {'Head':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3&category3=34&min_item_lv={Gear}",
                'Chest':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3&category3=35&min_item_lv={Gear}",
                'Hands':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3&category3=37&min_item_lv={Gear}",
                'Legs': f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3&category3=36&min_item_lv={Gear}",
                'Feet': f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3&category3=38&min_item_lv={Gear}",
                'Shields':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3&category3=11&min_item_lv={Gear}",
                'Earrings':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=4&category3=41&min_item_lv={Gear}",
                'Necklace':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=4&category3=40&min_item_lv={Gear}",
                'Bracelets':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=4&category3=42&min_item_lv={Gear}",
                'Ring': f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=4&category3=43&min_item_lv={Gear}"
                }
    with open('Gear_urls.json', 'w') as file:
        json.dump(Gear_urls, file)

    url_base = "https://na.finalfantasyxiv.com"

    with open('url_base.json', 'w') as file:
        json.dump(url_base, file)




    #----------------------GEAR---------------------------#
    print('Updating gear database')

    Links = {}
    for key, val in tqdm(All_gear_url.items()):
        source = requests.get(val).text
        soup = bfs(source, 'lxml')
        Gear = soup.find_all('a', class_='db_popup db-table__txt--detail_link')

        for g in Gear: 
            Link = url_base + g.get('href')
            Name = g.text
            Links.update({Name:Link})

    with open('Links.json', 'w') as file:
        json.dump(Links, file)

    if st_enable:
        st.write('Updating Gear')
        waitbar = st.progress(0)
        i = (int(k) for k in np.linspace(0, 100, len(Links)))

    database = {}
    for key, val in tqdm(Links.items()):

        source = requests.get(val).text
        soup = bfs(source, 'lxml')
        data = {}
        
        data.update({'Type':soup.find('p', class_="db-view__item__text__category").text,
                    'iLVL':int(soup.find('div', class_="db-view__item_level").text.split('Item Level ')[1]),
                    'Jobs':soup.find('div', class_="db-view__item_equipment__class").text,
                    'Materia_Sockets': str(soup.find('ul', class_='db-view__materia_socket')).count('socket normal')
                    })
        
        Bonuses = soup.find('ul', class_="db-view__basic_bonus").text
        Split = Bonuses.split('\n')
        Split.pop(0)
        Split.pop(-1)
        
        for info in Split:
            stat, val = info.split(' +')
            data.update({stat:int(val)})
        
        database.update({key:data})

        if st_enable:
            with Load_area:
                waitbar.progress(next(i))

    with open('database.json', 'w') as file:
        json.dump(database, file)




    #------------------------FOOD--------------------------#

    print('Updating food database...')

    All_food_url = {'Food':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=5&category3=46&min_item_lv=580"}
    url_base = "https://na.finalfantasyxiv.com"
    #---Load urls to all food---
    Food_Links = {} 
    for key, val in tqdm(All_food_url.items()):
        source = requests.get(val).text
        soup = bfs(source, 'lxml')
        Gear = soup.find_all('a', class_='db_popup db-table__txt--detail_link')

        for g in Gear: 
            Link = url_base + g.get('href')
            Name = g.text
            Food_Links.update({Name:Link})

    with open('Food_Links.json', 'w') as file:
        json.dump(Food_Links, file)

    if st_enable:
        st.write('Updating Food')
        waitbar = st.progress(0)
        i = (int(k) for k in np.linspace(0, 100, len(Food_Links)))

    Food_database = {}
    for key, val in tqdm(Food_Links.items()):

        source = requests.get(val).text
        soup = bfs(source, 'lxml')
        data = {}

        data.update({'Type':soup.find('p', class_="db-view__item__text__category").text,
                    'iLVL':int((soup.find('div', class_="db-view__item_level").text).split('Item Level ')[1])
                    })

        Food_Bonuses = soup.find('ul', class_="sys_nq_element").text
        Split = Food_Bonuses.split('\n')
        Split.pop(0)
        Split.pop(-1)
        
        for info in Split:
            stat, rest = info.split(' +')
            percentage, _, rest = rest.split(' ')
            statval, _ = rest.split(')')

            percentage = float(percentage.split('%')[0])/100

            data.update({stat:int(statval),
                        'percentage':percentage})

        if 'Craftsmanship' in stat or 'Gathering' in stat:
            continue
        Food_database.update({key:data})

        if st_enable:
            with Load_area:
                waitbar.progress(next(i))


        with open('Food_database.json', 'w') as file:
            json.dump(Food_database, file)

    print('Update completed, json files updated!')

    if st_enable:
        with Load_area:
            st.write('Database updated!')


def developer(url):
    pass

if __name__ == '__main__':
    main()