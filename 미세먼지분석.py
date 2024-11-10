import pandas as pd
import matplotlib.pyplot as plt
plt.rc('font', family='Gulim')

file_path = r'C:\\Users\\guddn\\OneDrive\\바탕 화면\\2024-2학기\\인공지능개론\\서울시 대기질 자료 제공_2022.csv'
data = pd.read_csv(file_path, encoding='euc-kr')

# '일시'를 datetime 형식으로 변환하고 시간 추출
data['일시'] = pd.to_datetime(data['일시'])
data['시간'] = data['일시'].dt.hour
data['날짜'] = data['일시'].dt.date
data['요일'] = data['일시'].dt.weekday
# 주말과 평일 구분 (주말: 5, 6 -> 일요일, 토요일 / 평일: 0-4)
data['주말/평일'] = data['요일'].apply(lambda x: '주말' if x >= 5 else '평일')

# '구분'을 기준으로 그룹화하여 각 구의 평균, 중앙값, 최댓값, 최솟값, 표준편차 계산
grouped_stats = data.groupby('구분')[['미세먼지(PM10)', '초미세먼지(PM2.5)']].agg({
    '미세먼지(PM10)': ['mean', 'median', 'max', 'min', 'std'],
    '초미세먼지(PM2.5)': ['mean', 'median', 'max', 'min', 'std']
})

# 시간대별 미세먼지(PM10)와 초미세먼지(PM2.5)의 평균 계산
hourly_avg_pm = data.groupby('시간')[['미세먼지(PM10)', '초미세먼지(PM2.5)']].mean()

# 가장 높은 미세먼지, 초미세먼지 농도를 기록한 지역 찾기
worst_pm = data.loc[data['미세먼지(PM10)'].idxmax()]
worst_pm2 = data.loc[data['초미세먼지(PM2.5)'].idxmax()]

# 결과 출력
print("각 구별 미세먼지와 초미세먼지의 통계:\n")
print(grouped_stats.round(2))

# 가장 높은 미세먼지
print("\n가장 높은 미세먼지을 기록한 지역:\n")
print(worst_pm.round(2))

print("\n가장 높은 초미세먼지을 기록한 지역:\n")
print(worst_pm2.round(2))

#초과 기준치 비율
pm10_threshold = 100
pm25_threshold = 35

pm10_exceed_ratio = (data['미세먼지(PM10)'] > pm10_threshold).mean()
pm25_exceed_ratio = (data['초미세먼지(PM2.5)'] > pm25_threshold).mean()

print(f"\n미세먼지 초과 기준치 비율: {pm10_exceed_ratio * 100:.2f}%")
print(f"초미세먼지 초과 기준치 비율: {pm25_exceed_ratio * 100:.2f}%")

# 지역별 미세먼지 평균 농도를 기준으로 오염도가 높은 구와 낮은 구 순위
pm_avg_by_district = data.groupby('구분')[['미세먼지(PM10)', '초미세먼지(PM2.5)']].mean()

# 미세먼지 평균을 기준으로 정렬 (내림차순)
pm_avg_by_district_sorted = pm_avg_by_district.sort_values(by='미세먼지(PM10)', ascending=False)

print("\n미세먼지 평균 농도를 기준으로 오염도가 높은 구 순위:\n")
print(pm_avg_by_district_sorted[['미세먼지(PM10)']].round(2))

# 초미세먼지 평균을 기준으로 정렬 (내림차순)
pm_avg_by_district_sorted_pm25 = pm_avg_by_district.sort_values(by='초미세먼지(PM2.5)', ascending=False)

print("\n초미세먼지 평균 농도를 기준으로 오염도가 높은 구 순위:\n")
print(pm_avg_by_district_sorted_pm25[['초미세먼지(PM2.5)']].round(2))

# 주말과 평일의 차이 분석
weekend_weekday_pm = data.groupby('주말/평일')[['미세먼지(PM10)', '초미세먼지(PM2.5)']].mean()
print("\n주말과 평일의 미세먼지 농도 차이:\n")
print(weekend_weekday_pm.round(2))  # 소수점 2자리로 출력

# 월별 미세먼지 농도 분석
data['월'] = data['일시'].dt.month  # 월을 추출
monthly_pm = data.groupby('월')[['미세먼지(PM10)', '초미세먼지(PM2.5)']].mean()
print("\n월별 미세먼지 농도:\n")
print(monthly_pm.round(2))

# 시간대별 미세먼지 농도 변화 분석
print("\n시간대별 미세먼지 농도:\n")
print(hourly_avg_pm.round(2))

# 미세먼지 기준으로 정렬한 바 차트
plt.figure(figsize=(12, 6))
plt.bar(pm_avg_by_district_sorted.index, pm_avg_by_district_sorted['미세먼지(PM10)'], color='blue')
plt.title('지역별 미세먼지 평균 농도')
plt.xlabel('구')
plt.ylabel('농도 (㎍/㎥)')
plt.xticks(rotation=90)
plt.show()

# 초미세먼지 기준으로 정렬한 바 차트
plt.figure(figsize=(12, 6))
plt.bar(pm_avg_by_district_sorted_pm25.index, pm_avg_by_district_sorted_pm25['초미세먼지(PM2.5)'], color='red')
plt.title('지역별 초미세먼지 평균 농도')
plt.xlabel('구')
plt.ylabel('농도 (㎍/㎥)')
plt.xticks(rotation=90)
plt.show()

# 월별 미세먼지 평균 농도
plt.figure(figsize=(10, 6))
plt.bar(monthly_pm.index, monthly_pm['미세먼지(PM10)'], color='blue')
plt.title('월별 미세먼지 평균 농도')
plt.xlabel('월')
plt.ylabel('농도 (㎍/㎥)')
plt.xticks(monthly_pm.index)
plt.show()

# 월별 초미세먼지 평균 농도
plt.figure(figsize=(10, 6))
plt.bar(monthly_pm.index, monthly_pm['초미세먼지(PM2.5)'], color='red')
plt.title('월별 초미세먼지 평균 농도')
plt.xlabel('월')
plt.ylabel('농도 (㎍/㎥)')
plt.xticks(monthly_pm.index)
plt.show()


