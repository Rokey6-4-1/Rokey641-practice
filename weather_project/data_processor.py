# data_processor.py

import pandas as pd
import json

# Current_Weather_data 목록 추가
path1 = r"C:\rokey\Rokey641-practice\weather_project\current_weather.csv"
df1 = pd.read_csv(path1)
# print(df1)
data = {'City' : [], 'Weather' : [], 'Temperature' : [] ,'Latitude' : [], 'longitude' : []}
for i in range(len(df1)):
    city = df1.iloc[i]["City"]
    city_Weather = df1.iloc[i][" Weather"]
    city_Temperature = df1.iloc[i][" Temperature"]
    city_Latitude = df1.iloc[i][" Latitude"]
    city_longitude = df1.iloc[i][" longitude"]


    # 도시, 날씨, 온도, 위도, 경도를 data 딕셔너리에 추가 
    data['City'].append(city)
    data['Weather'].append(city_Weather)
    data['Temperature'].append(city_Temperature)
    data['Latitude'].append(city_Latitude)
    data['longitude'].append(city_longitude)
 

# 데이터프레임 생성
pd_Ll = pd.DataFrame(data)
pd_Ll.sort_values(by=['City'], inplace=True)
print(pd_Ll)

# 도시, 위도, 경도 데이터프레임을 .json 파일로 변경 후 저장
path1 = r"C:\rokey\Rokey641-practice\weather_project\pd_li.json"
pd_Ll.to_json(path1,orient='records', indent=4)

path2 = r"C:\rokey\Rokey641-practice\weather_project\forecast.csv"
df2 = pd.read_csv(path2)
# print(df2)

df_melted = df2.reset_index(drop=True).melt(
    id_vars=['City'], 
    var_name='Time', 
    value_name='Data'
)
# print(df_melted)

# 데이터 온도와 날씨 split 함수로 구분
split_data = df_melted['Data'].str.strip().str.split(' ', n=1, expand=True)
df_melted['Temperature'] = split_data[0]
# print(df_melted['Temperature'])

df_melted['Temperature'] = pd.to_numeric(df_melted['Temperature'], errors='coerce')

df_melted['Time'] = df_melted['Time'].str.strip()
df_melted['Time'] = pd.to_datetime(df_melted['Time'])
df_melted['Date'] = df_melted['Time'].dt.date

df_clean = df_melted.dropna(subset=['Temperature'])

# Max, Min, Avg 온도 계산
df_summary = df_clean.groupby(['City','Date'])['Temperature'].agg(
    Min_Temp='min',
    Max_Temp='max',
    Avg_Temp='mean'
).reset_index()
df_summary['Date'] = df_summary['Date'].astype(str)

print("### 도시와 날짜별 최소, 최대, 평균 온도 ###")
df_summary.sort_values(by=['City', 'Date'], inplace=True)
# print(df_summary)
# print(type(df_summary))

# .json 파일로 변환 후 저장
path2 = r"C:\rokey\Rokey641-practice\weather_project\df_summary.json"
df_summary.to_json(path2,orient='records',date_format='iso', indent=4)


