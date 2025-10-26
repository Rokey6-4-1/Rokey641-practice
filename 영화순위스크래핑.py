import requests
from bs4 import BeautifulSoup
import re 
from openpyxl import Workbook




url = "https://www.moviechart.co.kr"

response = requests.get(url) 

soup = BeautifulSoup(response.content, 'html.parser')

 
name = soup.find_all('div',class_ = 'visual_ranking_txt')
names = str(name)


movie = re.findall("<p>(.+)</p>", names)
ticket = re.findall("<span>(.+)</span>",names)
wb = Workbook()
sheet = wb.active

sheet['A1'] = "영화제목"
sheet['B1'] = "예매율"
for i in range(len(movie)):
    print(movie[i],ticket[i])
    
    sheet['A'+str(i+2)] = movie[i]
    sheet['B'+str(i+2)] = ticket[i]
    

wb.save('영화순위스크래핑.xlsx')
