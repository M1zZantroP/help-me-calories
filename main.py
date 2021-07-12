import os
import sys
import time
from selenium import webdriver
import requests
import csv
from bs4 import BeautifulSoup
import lxml
import json

import getch
import keyboard


URL = 'https://www.tablycjakalorijnosti.com.ua/tablytsya-yizhyi'
# URL = 'https://www.tablycjakalorijnosti.com.ua/molochni-produkty-ta-jajtsja/johurt'
DOMAIN = 'https://www.tablycjakalorijnosti.com.ua/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.177',
		   'Accept': '*/*'}
PARAMS = {'format': 'json', 'limit': 30, 'type': 0, 'min': 0, 'max': 3800, 'sliderType': 0, 'page': 1}


def get_page(url, params=None):
	r = requests.get(url, headers=HEADERS, params=PARAMS)
	return r.text


def get_links():
	html = get_page(URL)
	soup = BeautifulSoup(html, 'lxml')
	items = soup.find_all('md-option', class_='select-option-bg')

	links = {}

	for item in items:
		links[item.get_text(strip=True)] = DOMAIN + item.find_next().get('href')[1:]

	return links


def get_products_database():
	# *** CREATE AND PARSE ALL THE DATA FROM SERVER TO {data.json}
	# ***

	# products = []
	# for i in range(1292):
	# 	URL = f'https://www.tablycjakalorijnosti.com.ua/foodstuff/filter-list?format=json&page={i}&limit=30&query=&type=0&brand=&min=0&max=3800&sliderType=0'
	# 	temp = requests.get(URL)
	# 	products.extend(temp.json()['data'])
	#
	# keywords = ['title', 'url', 'energy', 'protein', 'carbohydrate', 'fat']

	# with open('data.json', 'w', encoding='utf-8') as f:
	# 	json.dump(products, f, ensure_ascii=False, indent=4)


	# *** FILTER IMPORTANT DATA AND WRITE TO {product.json}
	# ***
	with open('products.json', 'a', encoding='utf-8') as f:
		with open('data.json', 'r', encoding='utf-8') as d:
			dictionary = json.load(d)
			temp = []
			for item in dictionary:
				temp.append({
					'Назва': str(item.get('title')).replace('"', '').title(),
					'URL': 'https://www.tablycjakalorijnosti.com.ua/stravy/' + str(item.get('url')),
					'Енергія': float(item.get('energy').replace(',', '.')) if item.get('energy') else 0,
					'Білки': float(item.get('protein').replace(',', '.')) if item.get('protein') else 0,
					'Вуглеводи': float(item.get('carbohydrate').replace(',', '.')) if item.get('carbohydrate') else 0,
					'Жири': float(item.get('fat').replace(',', '.')) if item.get('fat') else 0,
					'Волокна': float(item.get('fiber').replace(',', '.')) if item.get('fiber') else 0
				})

			json.dump(temp, f, ensure_ascii=False, indent=4)

	return 'Done! Products parsed' if os.path.getsize('products.json') > 0 else 'Something wrong...'


def get_products_link():
	"""
	This function's reading information from *product.json*
	get product links
	and write links to file *links.txt*
	"""


	f = open('products.json', 'r')
	data = json.load(f)
	products_links = []

	for i in data:
		products_links.append(i['URL'])

	with open('links.txt', 'w') as li:
		for i in products_links:
			li.write(str(i) + '\n')

	return 'links.txt created successfully!' if os.path.getsize('links.txt') else 'Something wrong...'


def search_product():
	"""
	It's the console-search that update view after press a new letter.
	Finally its give you a list of filtered products
	"""


	tmp = json.load(open('products.json'))
	temp_d = list(x['Назва'] for x in tmp)
	a = ''
	while True:
		# print(a, end='')
		list_to_choise = [x for x in temp_d if a in x]
		tmp = keyboard.read_key()

		if tmp == 'backspace':

			a = a[:-1]
			os.system('cls') if sys.platform == 'win32' else os.system('clear')
			print(a, end='')
			list_to_choise = [x for x in temp_d if a in x]
			if len(list_to_choise) < 10:
				for i in temp_d:
					if a in i:
						print(i)
			else:
				print(f'\n[INFO] Find {len(list_to_choise)} elems')


		#
		elif keyboard.is_pressed(tmp) and tmp[0] in 'qazxswedcvfrtgbnhyujmkiolpйфячіцувсмакепитрнгоьблшщдюжзхєїґ':
			a += tmp[0]
			os.system('cls') if sys.platform == 'win32' else os.system('clear')
			list_to_choise = [x for x in temp_d if a in x]
			if len(list_to_choise) > 100:
				os.system('cls') if sys.platform == 'win32' else os.system('clear')
				print(f'\n[INFO] Find {len(list_to_choise)} elems')
			else:
				os.system('cls') if sys.platform == 'win32' else os.system('clear')
				print(f'\n[INFO] Find {len(list_to_choise)} elems')
				count = 0
				for i in list_to_choise:
					print(f'[{count}] ', i)
					count += 1
			print(a, end='')
		elif tmp[0] in '1234567890':
			choice = list_to_choise[int(tmp[0])]
			os.system('cls') if sys.platform == 'win32' else os.system('clear')
			with open('products.json') as p:
				file = json.load(p)
				index_catch = temp_d.index(choice)
				print('\n\t[PRODUCT INFO]\n',
					  	' __________________________________________________________________________________________\n',
						f'|  Назва     |  {file[index_catch]["Назва"]}\n',
						f'|  Посилання |  {file[index_catch]["URL"]}\n',
						f'|  Енергія   |  {file[index_catch]["Енергія"]} (ккал.)\n',
						f'|  Білки     |  {file[index_catch]["Білки"]} (гр.)\n',
						f'|  Вуглеводи |  {file[index_catch]["Вуглеводи"]} (гр.)\n',
						f'|  Жири      |  {file[index_catch]["Жири"]} (гр.)\n',
						f'|  Волокна   |  {file[index_catch]["Волокна"]} (гр.)\n',
						' ------------------------------------------------------------------------------------------')



		elif keyboard.is_pressed(tmp) and tmp == 'esc':
			print('Finish')
