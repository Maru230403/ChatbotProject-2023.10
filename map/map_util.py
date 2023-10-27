import requests, json, os, folium
import numpy as np
import pandas as pd
from urllib.parse import quote

def get_station_map(root_path, stations):

    # CSV 파일에서 데이터 읽기
    data = pd.read_csv('data/서울부동산.csv')  # CSV 파일 이름을 적절하게 변경하세요


    # CSV 파일의 각 행을 반복하며 지도에 마커 추가
    for index, row in data.iterrows():
        folium.Marker(location=[row['위도'], row['경도']], popup=row['CMP_NM']).add_to(m)

    # 지도를 HTML 파일로 저장
    m.save('map.html')

    # HTML 파일을 웹 브라우저로 열거나 웹 애플리케이션에 통합할 수 있습니다.

    # map 그리기
    map = folium.Map(location=[data.위도.mean(), data.경도.mean()], zoom_start=14)  # Center position
    for i in data.index:
        folium.Marker(
            location=[data.위도[i], data.경도[i]],       
            tooltip=data.CMP_NM[i],
            popup=folium.Popup(data.ADDRESS[i], max_width=200)
        ).add_to(map)   
    filename = os.path.join(root_path, 'img/map.html')
    map.save(filename)
