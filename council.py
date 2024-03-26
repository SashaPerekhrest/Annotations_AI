from bs4 import BeautifulSoup
import requests
import os
import re

PAGE_COUNT = 10

folder_path = 'downloads'

# Сбор ссылок аннотаций
def save_annotations(page_soup):
    annotation_links = []    

    regex = re.compile(r'^http://council.gov.ru/media/files/')
    a_elements = page_soup.find_all('a', href=regex)

    for a in a_elements:
        if a.text.rstrip() == 'Аннотации к ФЗ':
            annotation_links.append(a['href'])

    print(annotation_links)
    return annotation_links


# Скачивание pdf файлов
def save_pdf(links):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for link in links:
        file_name = link.split('/')[-1]
        file_path = os.path.join(folder_path, file_name)

        response = requests.get(link)

        with open(file_path, 'wb') as file:
            file.write(response.content)


for page_number in range(PAGE_COUNT):
    url = f'http://council.gov.ru/activity/meetings/page/{page_number + 1}/'
    print('\nURL: ', url + '\n')
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    links = save_annotations(soup)
    save_pdf(links)
