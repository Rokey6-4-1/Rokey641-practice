import requests 
import json

apikey = "58debd485f85ee5e532f286896bfa328" 
 
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

apicur = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"
apifor = "http://api.openweathermap.org/data/2.5/forecast?q={city}&APPID={key}" 
# 켈빈 온도를 섭씨 온도로 변환하는 함수 
k2c = lambda k: k - 273.15

# current weather
file = open("./current_weather.csv", "w", encoding="utf-8")
file.write("City, Temperature, Humidity, Weather\n")
for city in cities:

    url = apicur.format(city=city, key=apikey) 
    r = requests.get(url) 
    data = json.loads(r.text)

    temp = k2c(data["main"]["temp"])
    hum = data["main"]["humidity"]
    des = data["weather"][0]["description"]
    file.write(f"{city}, {temp:.1f}, {hum}, {des}\n")
file.close()


# forecast
file = open("./forecast.csv", "w", encoding="utf-8")

url = apifor.format(city=cities[0], key=apikey) 
r = requests.get(url) 
data = json.loads(r.text)

file.write("City, ")
for i in range(40):
    file.write(f"{data['list'][i]['dt_txt']}, ") # UTC
file.write("\n")

for city in cities:
    
    url = apifor.format(city=city, key=apikey) 
    r = requests.get(url) 
    data = json.loads(r.text)
    
    file.write(f"{city}, ")
    for i in range(40):
        temp = k2c(data['list'][i]['main']['temp'])
        des = data['list'][i]['weather'][0]['description']
        file.write(f"{temp:.1f} {des}, ")
    file.write("\n")
file.close()