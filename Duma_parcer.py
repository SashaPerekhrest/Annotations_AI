from bs4 import BeautifulSoup
import requests
import os
import csv
from autocorrect import Speller
from pdfminer.high_level import extract_text
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize  
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *

folder_path = 'downloads'
listRow = []
count = 0
with open("anotations.csv", encoding='utf-8') as r_file:
    file_reader = csv.reader(r_file, delimiter = ",")
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

for counter in range(0, count - 1):
    print(listRow[counter][3])
    print(counter)
    link = "https://sozd.duma.gov.ru/bill/" + listRow[counter][3]
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'lxml')

    url = "none"
    href_block = soup.find_all(class_='opch_r')
    if len(href_block) == 0:
        print(url)
        continue  
    for post in href_block:
        if post.find("a"):
            url = "https://sozd.duma.gov.ru" + post.find("a").get("href")
    print(url)
    if url == "none":
        continue
    test = requests.get(url)
    file_name = listRow[counter][3] + ".pdf"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'wb') as file:
        file.write(test.content)
    result = ""
    try:
        text = extract_text(file_path)
        stemmer = PorterStemmer()
        tokens = word_tokenize(text, "russian")
        stemed_tokens = []
        for word in tokens:
            stemed_tokens.append(stemmer.stem(word))
        lemmatizer = WordNetLemmatizer()
        nltk_lemma_list = []
        for word in stemed_tokens:
            nltk_lemma_list.append(lemmatizer.lemmatize(word))
        normalized_tokens = []  
        nltk_stop_words = set(stopwords.words("russian"))
        for w in nltk_lemma_list:  
            if w not in nltk_stop_words:  
                normalized_tokens.append(w)
        result = ' '.join(normalized_tokens)
    except:
        continue
    writer.writerow([listRow[counter][0],listRow[counter][1],listRow[counter][2],listRow[counter][3],result])