## 데이터 출처 - "https://www.data.go.kr/tcs/dss/selectFileDataDetailView.do?publicDataPk=15063273"
##데이터 출처: https://data.seoul.go.kr/dataList/OA-11677/S/1/datasetView.do

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import webbrowser
# import matplotlib.font_manager as fm


origin_Data=pd.read_csv("서울시 코로나19 확진자 현황.csv")
corona_del_col = origin_Data.drop(columns=['국적', '환자정보','조치사항'])#비어있는 column지우기
corona_out_region = corona_del_col.replace({'종랑구': '중랑구', '한국': '기타'}) ##종랑구 오타 및 이상치 데이터 처리

##확진일 'mm.dd'를 month, day column으로 나누어 생성
month = []
day = []
for data in corona_del_col['확진일']:
    month.append(data.split('.')[0])
    day.append(data.split('.')[1])

corona_del_col['month'] = month
corona_del_col['day'] = day

def origin_print():
    print(origin_Data)

def origin_info():
    print(origin_Data.info())

def monthly_data():
    order = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    plt.figure(figsize=(10, 5))
    sns.set(style="darkgrid")
    sns.countplot(x="month", data=corona_del_col, palette="Set2", order=order)
    plt.show()

    # corona_del_col['month'].value_counts().plot(kind='bar')

    print(corona_del_col['month'].value_counts())

def daily_data():
    nmonth = input("월을 입력해 주세요.(1~10)")
    if nmonth not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
        print('1~10월만 조회 가능합니다.')
        return

    order2 = []
    for i in range(1, 32):
        order2.append(str(i))

    plt.figure(figsize=(10, 5))
    sns.set(style="darkgrid")
    sns.countplot(x="day", data=corona_del_col[corona_del_col['month'] == nmonth], palette="rocket_r", order=order2)
    plt.show()

def area_data():
    # font_dirs = ['/usr/share/fonts/truetype/nanum', ]
    # font_files = fm.findSystemFonts(fontpaths=font_dirs)

    # for font_file in font_files:
    #     fm.fontManager.addfont(font_file)
    #폰트

    plt.figure(figsize=(10, 5))
    # # 한글 출력을 위해서 폰트 옵션을 설정합니다.
    # sns.set(font="NanumBarunGothic",
    #         rc={"axes.unicode_minus": False},
    #         style='darkgrid')
    sns.countplot(x="지역", data=corona_out_region, palette="Set2")
    plt.show()

def monthly_area_data():
    nmonth = input("월을 입력해 주세요.(1~10)")
    if nmonth not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
        print('1~10월만 조회 가능합니다.')
        return

    plt.figure(figsize=(20, 10))
    sns.set(font="NanumBarunGothic",
            rc={"axes.unicode_minus": False},
            style='darkgrid')
    ax = sns.countplot(x="지역", data=corona_out_region[corona_del_col['month'] == nmonth], palette="Set2")
    plt.show()

def mapping():
    map_osm = folium.Map(location=[37.529622, 126.984307], zoom_start=11)

    CRS = pd.read_csv("서울시 행정구역 시군구 정보 (좌표계_ WGS1984).csv")

    # corona_out_region의 지역에는 'oo구' 이외로 `타시도`, `기타`에 해당되는 데이터가 존재 합니다.
    # 위 데이터에 해당되는 위도, 경도를 찾을 수 없기에 삭제하여 corona_seoul로 저장합니다.
    corona_seoul = corona_out_region.drop(corona_out_region[corona_out_region['지역'] == '타시도'].index)
    corona_seoul = corona_seoul.drop(corona_out_region[corona_out_region['지역'] == '기타'].index)

    # 서울 중심지 중구를 가운데 좌표로 잡아 지도를 출력합니다. CRS[CRS['시군구명_한글'] == '중구']
    map_osm = folium.Map(location=[37.557945, 126.99419], zoom_start=11)

    # 지역 정보를 set 함수를 사용하여 25개 고유의 지역을 뽑아냅니다.
    for region in set(corona_seoul['지역']):
        # 해당 지역의 데이터 개수를 count에 저장합니다.
        count = len(corona_seoul[corona_seoul['지역'] == region])
        # 해당 지역의 데이터를 CRS에서 뽑아냅니다.
        CRS_region = CRS[CRS['시군구명_한글'] == region]

        # CircleMarker를 사용하여 지역마다 원형마커를 생성합니다.
        marker = folium.CircleMarker([CRS_region['위도'], CRS_region['경도']],  # 위치
                                     radius=count / 10 + 10,  # 범위
                                     color='#3186cc',  # 선 색상
                                     fill_color='#3186cc',  # 면 색상
                                     popup=' '.join((region, str(count), '명')))  # 팝업 설정

        # 생성한 원형마커를 지도에 추가합니다.
        marker.add_to(map_osm)

    map_osm.save('example.html')
    webbrowser.open("example.html")


while 1:
    print("--------------------------------------------")
    print("2020.01~2020.10 서울시 코로나 확진자 데이터(5748명) ")
    print("데이터 분석을 위한 프로젝트입니다.")
    print("원하는 데이터의 번호를 입력해주세요.(종료 : q)")
    print("1. 원본 데이터 내역")
    print("2. 원본 데이터 정보")
    print("3. 월별 확진자 수(표 + 그래프)")
    print("4. 특정 월의 일별 확진자 수(그래프)")
    print("5. 지역별 확진자 수(그래프)")
    print("6. 월별 지역 확진자 수(그래프)")
    print("7. 확진자 분포 확인(지도)")

    n = input()
    if n == '1':
        origin_print()
    elif n == '2':
        origin_info()
    elif n == '3':
        monthly_data()
    elif n == '4':
        daily_data()
    elif n == '5':
        area_data()
    elif n == '6':
        monthly_area_data()
    elif n == '7':
        mapping()
    elif n == 'q':
        break
    else:
        print("올바른 값을 입력해 주세요")

