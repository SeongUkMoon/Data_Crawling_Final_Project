from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re



# [CODE 1]
def Yogiyo_Crawler(result, address, category):
    URL = "https://www.yogiyo.co.kr/mobile/#/"
    wd = webdriver.Chrome('./chromedriver/chromedriver.exe')

    wd.get(URL)
    time.sleep(1)  # 웹페이지 연결할 동안 1초 대기

    wd.find_element(By.XPATH, '//input[@name="address_input"]').clear()
    wd.find_element(By.XPATH, '//input[@name="address_input"]').send_keys(address)
    wd.find_element(By.XPATH, '//button[@class="btn btn-default ico-pick"]').click()
    time.sleep(1)

    wd.find_element(By.XPATH, '//button[@id="category-menu"]').click()
    time.sleep(2)

    wd.find_element(By.CSS_SELECTOR, f'ul > li:nth-child({category})').click()
    time.sleep(2)

    wd.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # 스크롤을 가장 아래로 내린다
    time.sleep(2)
    # wd.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # 스크롤을 가장 아래로 내린다
    # time.sleep(2)

    restaurant_list = wd.find_element(By.XPATH, '//div[@class="restaurant-list"]')
    rests = restaurant_list.find_elements(By.XPATH, '//div[@class="item clearfix"]')

    rest_cnt = len(rests)

    for i in range(rest_cnt):
        if i >= 60:
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # 스크롤을 가장 아래로 내린다
            time.sleep(2)
        restaurant_list = wd.find_element(By.XPATH, '//div[@class="restaurant-list"]')
        rests = restaurant_list.find_elements(By.XPATH, '//div[@class="item clearfix"]')
        rests[i].click()
        time.sleep(2)

        html = wd.page_source
        soup = BeautifulSoup(html, 'html.parser')
        title_div = soup.find('span', attrs={'class': 'restaurant-name ng-binding'})
        store_name = list(title_div.strings)[0]

        info_div = soup.find('div', attrs={'class': 'restaurant-content'})
        th_list = info_div.findAll('li')

        rating = float(list(th_list[0].strings)[-1].strip())

        least_pay_str = list(th_list[2].strings)[1]
        least_pay = int(re.sub(r'[^0-9]', '', least_pay_str))

        delivery_time_list = list(th_list[4].strings)[1][:-1].split('~')
        delivery_time_list = list(map(int, delivery_time_list))
        delivery_time = sum(delivery_time_list) // len(delivery_time_list)

        review_a = soup.find('a', attrs={'ng-click': 'toggle_tab("review")'})
        review_cnt = int(list(review_a.strings)[1])

        tip_span = soup.find('span', attrs={'class': 'list-group-item clearfix text-right ng-binding'})

        if tip_span == None:
            wd.back()
            time.sleep(1)
            continue

        tip_str = list(tip_span.strings)[0].strip()
        tip = int(re.sub(r'[^0-9]', '', tip_str))

        print([store_name, category, delivery_time, rating, review_cnt, least_pay, tip])

        result.append([store_name, category, delivery_time, rating, review_cnt, least_pay, tip])

        wd.back()
        time.sleep(3)

    return

"""

    <카테고리 넘버링>
    2   : 전체보기
    3   : 1인분 주문
    4   : 프랜차이즈
    5   : 치킨
    6   : 피자/양식
    7   : 중국집
    8   : 한식
    9   : 일식/돈까스
    10   : 족발/보쌈
    11   : 야식
    12  : 분식
    13  : 카페/디저트
    14  : 편의점/마트

"""


# [CODE 0]
def main():
    result = []
    address = '서울특별시 노원구 상계동 624 상계주공16단지아파트 1603동'
    address = '서울특별시 성북구 장위동 225-127'

    print('요기요 배달비 데이터 웹 브라우저 크롤링 실행 >>>>>>>>>>>>>>>>>>>>>>>')

    for category in range(5, 14):
        Yogiyo_Crawler(result, address, category)  # [CODE 1]

    tbl = pd.DataFrame(result, columns=('가게명', '판매업종', '배달소요시간', '평점', '리뷰수', '배달기준금액', '배달비'))
    tbl.to_csv(f'./YogiyoTip3.csv', encoding='cp949', mode='w', index=False)
    print('요기요 배달팁 데이터 csv 저장 >>>>>>>>>>>>>>>>>>>>>>>')

if __name__ == '__main__':
    main()
