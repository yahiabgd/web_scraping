from os import write
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import requests
import csv
from itertools import zip_longest

name=list()
place =list()
prices=list()
time=list()
Phones=[]
Page_num =1
n =input('entrez le nombre de page a lire : ')
n=int(n)


while Page_num<n+1 :
    fhand = urllib.request.urlopen(f'https://www.ouedkniss.com/informatique/{Page_num}').read()
    soup = BeautifulSoup(fhand,'html.parser')
    products = soup.find_all("div", {"class":"annonce annonce_store","class":"annonce"})
    links = soup .find_all("a",{"itemprop":"url"})
    i=-1

    for product in products : 
        try:
            name.append(product.find("h2",{"itemprop":"name"}).text)
        except:
            continue
        place.append(product.find("span",{"class":"titre_wilaya"}).text)
        time.append(product.find("p",{"class":"annonce_date"}).text)
        i=i+1
        links[i]= 'https://www.ouedkniss.com/'+links[i].attrs["href"]
        try:
            prices.append(product.find("span",{"itemprop":"price"}).text)
        except:
            prices.append('no price')
    for link in links :
        result = requests.get(link)
        src = result.content
        soup=BeautifulSoup(src,"html.parser")
        try:
            phone = soup.find("p",{"class":"Phone"}).text
        except : phone='none'
        phone=phone.replace('Cliquer pour afficher','')
        #n= phone.find('C')
        #phone=phone[:n]
        #print(phone)
        try:
            Phones.append(phone)
        except :Phones.append('error')
    Page_num= Page_num+1
    if Page_num ==n+1 :
        print('fin')
    else:
        print('page switched to ',Page_num)

file_list =[name,place,prices,Phones,time]
exported = zip_longest(*file_list)
with open("C:/Users/Yahia/OneDrive/Bureau/files/web_scraping/testf.csv","w", newline='') as myfile :
    wr = csv.writer(myfile , delimiter=';')
    wr.writerow(["titre","location","price","Phone","time"])
    wr.writerows(exported)



