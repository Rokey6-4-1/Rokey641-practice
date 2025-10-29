import requests 
import json
import csv
# 1. API 키를 지정합니다. 자신의 키로 변경해서 사용  
apikey = "58debd485f85ee5e532f286896bfa328" 
# 2. 날씨를 확인할 도시 지정하기 
cities = [
    "Seoul",
    "Tokyo",
    "Beijing",
    "Singapore",
    "Bangkok",
    "Mumbai",
    "Dubai",
    "London",
    "Paris",
    "Berlin",
    "Madrid",
    "Rome",
    "New York",
    "Toronto",
    "Mexico City",
    "Sao Paulo",
    "Buenos Aires",
    "Cairo",
    "Lagos",
    "Sydney",
] 
# 3. API 지정 
apicur = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"
apifor = "http://api.openweathermap.org/data/2.5/forecast?q={city}&APPID={key}" 
# 4. 켈빈 온도를 섭씨 온도로 변환하는 함수 

k2c = lambda k: k - 273.15

file = open("./current_weather_data.csv", "w", encoding="utf-8")
for city in cities:

    # 5. 도시 정보 추출하기 
    # 6. API의 URL 구성하기 
    url = apicur.format(city=city, key=apikey) 
    # API에 요청을 보내 데이터 추출하기 
    r = requests.get(url) 
    # 7. 결과를 JSON 형식으로 변환하기  
    data = json.loads(r.text)

    temp = k2c(data["main"]["temp"])
    hum = data["main"]["humidity"]
    des = data["weather"][0]["description"]
    file.write(f"{city}, {temp}, {hum}, {des}\n")
file.close()

for city in cities:

    # 5. 도시 정보 추출하기 
    # 6. API의 URL 구성하기 
    url = apifor.format(city=city, key=apikey) 
    # API에 요청을 보내 데이터 추출하기 
    r = requests.get(url) 
    # 7. 결과를 JSON 형식으로 변환하기  
    data = json.loads(r.text)
    print(data['list']['dt'])