from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

category = ['6000201496', '6000188534', '6000188618', '6000188702', '6000188810', '6000188763', '6000190649', '6000200157',
            '6000200158', '6000200159', '6000200160', '6000200161']



options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=kr_KR')
options.add_argument("--disable-popup-blocking")
driver = webdriver.Chrome('./chromedriver', options=options)
df_reply = pd.DataFrame()
replys = []

for s in range (3, len(category)): # 중카테고리 반복 (카테고리 리스트 안에 URL 뒷부분 변수 기입해서 반복문)
    for i in range(1, 6):  # page_count
        url = 'https://www.ssg.com/disp/category.ssg?ctgId={}&page={}'.format(category[s], i)
        driver.get(url)
        for j in range(1, 81): # product_count
            #product 클릭
            try:
                time.sleep(0.5)
                btn_product = '//*[@id="ty_thmb_view"]/ul/li[{}]/div[2]/div[2]/div/a'.format(j) #제품 xpath
                clicked_btn_product = driver.find_element('xpath', btn_product).send_keys(Keys.ENTER)

                try : # 에러창이 나올 시, 3초 기다리고 에러창 끈 후에 이전 URL로 이동
                    WebDriverWait(driver, 1).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    time.sleep(1)
                    driver.get(url)
                    pass

                except: # 에러창 없을 시, 코드 계속 진행
                    continue

            except NoSuchElementException as e:
                try:
                    time.sleep(0.5)
                    btn_product = '//*[@id="ty_thmb_view"]/ul/li[{}]/div[2]/div[2]/div/a/em[1]'.format(j)   #제품 xpath
                    clicked_btn_product = driver.find_element('xpath', btn_product).send_keys(Keys.ENTER)
                    time.sleep(1)

                    try:  # 에러창이 나올 시, 3초 기다리고 에러창 끈 후에 이전 URL로 이동
                        WebDriverWait(driver, 3).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        time.sleep(1)
                        driver.get(url)
                        pass

                    except:  # 에러창 없을 시, 코드 계속 진행
                        continue
                except:
                    print('none')

            for k in range (1, 10):
                try:
                    time.sleep(0.5)
                    btn_reply = '//*[@id="comment_navi_area"]/a[{}]'.format(k)  #k번째 제품들 xpath
                    clicked_btn_reply = driver.find_element('xpath', btn_reply).send_keys(Keys.ENTER)
                    for l in range(1, 20, 2):
                        try:
                            reply = '//*[@id="cdtl_cmt_tbody"]/tr[{}]/td[1]/div/a/div[1]/span'.format(l)    #댓글 xpath
                            reply = driver.find_element('xpath', reply).text
                            print(reply)
                            reply = re.compile('[^가-힣 ]').sub(' ', reply)
                            replys.append(reply)
                            time.sleep(0.5)

                        except NoSuchElementException as e:
                            print('none')
                            pass

                except StaleElementReferenceException as r:
                    print('none')

                except NoSuchElementException as e:
                    print('none')

            driver.back()
            time.sleep(3)

        if i % 2 == 0:  #5번째마다 저장
            df_section_reply = pd.DataFrame(replys, columns=['reply'])
            df_section_reply['category'] = 'fashion'
            df_title = pd.concat([df_reply, df_section_reply], ignore_index=True)
            df_title.to_csv('./crawling_data/crawling_data_{}_To_{}.csv'.format(category[s], i),
                                    index = False)
            replys = []




# btn_product = '//*[@id="ty_thmb_view"]/ul/li[16]/div[2]/div[2]/div/a/em[1]'
#//*[@id="cdtl_cmt_tbody"]/tr[1]/td[1]/div/a/div[1]/span