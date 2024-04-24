from bs4 import BeautifulSoup
import requests
import os
import re
import csv
import PyPDF2
from autocorrect import Speller
from pdfminer.high_level import extract_text

folder_path = 'downloads'
listRow = []
with open("anotations.csv", encoding='utf-8') as r_file:
    # Создаем объект reader, указываем символ-разделитель ","
    file_reader = csv.reader(r_file, delimiter = ",")
    # Счетчик для подсчета количества строк и вывода заголовков столбцов
    count = 0
    # Считывание данных из CSV файла
    for row in file_reader:
        if count == 0:
            print(f'Файл содержит столбцы: {", ".join(row)}')
        else:
            listRow.append(row)
        count += 1
    print(f'Всего в файле {count} строк.')

csv_file = open('anotations_full.csv', 'w', newline="", encoding="utf-8")
writer = csv.writer(csv_file)
writer.writerow(["filename","abstract title","summary of the content","bill number","content of the bill"])

for r in listRow:
    print(r[3])
    link = "https://sozd.duma.gov.ru/bill/" + r[3]
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'lxml')

    href_block = soup.find_all(class_='opch_r')
    if len(href_block) == 0:
        break  # Если блок новостей пуст, прерываем цикл
    for post in href_block:
        if post.find("a"):
            url = "https://sozd.duma.gov.ru" + post.find("a").get("href")
    print(url)
    test = requests.get(url)
    file_name = r[3] + ".pdf"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'wb') as file:
        file.write(test.content)
    text = extract_text(file_path)
    writer.writerow([r[0],r[1],r[2],r[3],text])