from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time




# [CODE 1]
def BaedalTip_Crawler(result, month):
    URL = "https://www.consumer.go.kr/user/ftc/consumer/dlvrpc/980/selectDlvrList.do"
    wd = webdriver.Chrome('./chromedriver/chromedriver.exe')

    wd.get(URL)
    time.sleep(1)  # 웹페이지 연결할 동안 1초 대기

    wd.find_element(By.XPATH, f"//*[@id='dlvrPcMtS']/option[text()='{month}']").click()
    wd.find_element(By.XPATH, f"//*[@id='searchBtn']").click()

    time.sleep(1)  # 스크립트 실행할 동안 1초 대기

    html = wd.page_source
    soupBT = BeautifulSoup(html, 'html.parser')
    table_BT = soupBT.find('tbody', attrs={'id': 'selectable'})
    th_list = table_BT.findAll('th')
    td_list = table_BT.findAll('td')

    distance_data = []
    highlow_data = []
    for i, th in enumerate(th_list):
        if i % 3 == 0:
            distance_data.append(str(list(th.strings)[0]))
            distance_data.append(str(list(th.strings)[0]))
        else:
            highlow_data.append(str(list(th.strings)[0]))

    tip_data = []
    for td in td_list:
        tmp = str(list(td.strings)[0]).strip()
        tmp = tmp.replace(',', '')
        if tmp == '-':
            tmp = 0
        tip_data.append(int(tmp))

    for i , (dis, hl) in enumerate(zip(distance_data, highlow_data)):
        bamin = tip_data[5*i + 0]
        bamin_one = tip_data[5*i + 1]
        yogiyo = tip_data[5*i + 2]
        yogiyo_ex = tip_data[5*i + 3]
        coupangeats = tip_data[5*i + 4]
        result.append([2022] + [month] + [dis] + [hl] + [bamin] + [bamin_one] + [yogiyo] + [yogiyo_ex] + [coupangeats])

    return


# [CODE 0]
def main():
    result = []
    months = ['5월', '6월', '7월', '8월', '9월', '10월', '11월']
    #months = ['5월']

    print('배달비 데이터 웹 브라우저 크롤링 실행 >>>>>>>>>>>>>>>>>>>>>>>')


    for month in months:
        BaedalTip_Crawler(result, month)  # [CODE 1]


    BT_tbl = pd.DataFrame(result, columns=('년도', '월', '거리구간', '빈도', '배달의민족', '배민1', '요기요', '요기요익스', '쿠팡이츠'))
    BT_tbl.to_csv(f'./BaedalTip_22.csv', encoding='cp949', mode='w', index=False)
    print('배달비 데이터 csv 저장 >>>>>>>>>>>>>>>>>>>>>>>')

if __name__ == '__main__':
    main()
