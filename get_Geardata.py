from bs4 import BeautifulSoup as bfs
import lxml
import requests
from tqdm import tqdm
import json


def main():
	UpdateData(600)
	#developer('https://na.finalfantasyxiv.com/lodestone/playguide/db/item/f44294126eb/')
	#developer('https://na.finalfantasyxiv.com/lodestone/playguide/db/item/b71da5422ab/')


def UpdateData(iLVL):
	All_gear_url = {'Gear 1':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3&min_item_lv={iLVL}",
					'Gear 2': f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3&page=2&min_item_lv={iLVL}",
					'Accessories': f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=4&min_item_lv={iLVL}",
					'Weapons 1': f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=1&min_item_lv={iLVL}",
					'Weapons 2': f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=1&page=2&min_item_lv={iLVL}"}

	with open('All_gear_url.json', 'w') as file:
		json.dump(All_gear_url, file)

	Gear_urls = {'Head':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3&category3=34&min_item_lv={iLVL}",
				'Chest':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3&category3=35&min_item_lv={iLVL}",
				'Hands':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3&category3=37&min_item_lv={iLVL}",
				'Legs':	f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3&category3=36&min_item_lv={iLVL}",
				'Feet':	f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3&category3=38&min_item_lv={iLVL}",
				'Shields':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3&category3=11&min_item_lv={iLVL}",
				'Earrings':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=4&category3=41&min_item_lv={iLVL}",
				'Necklace':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=4&category3=40&min_item_lv={iLVL}",
				'Bracelets':f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=4&category3=42&min_item_lv={iLVL}",
				'Ring': f"https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=4&category3=43&min_item_lv={iLVL}"
				}
	with open('Gear_urls.json', 'w') as file:
		json.dump(Gear_urls, file)

	url_base = "https://na.finalfantasyxiv.com"

	with open('url_base.json', 'w') as file:
		json.dump(url_base, file)

	#---Load urls to all gear---
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

	#---Load data from gear page---
	#url = "https://na.finalfantasyxiv.com/lodestone/playguide/db/item/39b5b3b6f4e/"

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

	with open('database.json', 'w') as file:
		json.dump(database, file)

	print('Update completed, json files updated!')



def developer(url):
	print('Dev testing...')
	source = requests.get(url).text
	soup = bfs(source, 'lxml')

	sockets = str(soup.find('ul', class_='db-view__materia_socket')).count('socket normal')
	print(sockets)

if __name__ == '__main__':
	main()