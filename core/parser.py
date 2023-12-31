from django.utils import timezone
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, \
    ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from .models import TendersList
from datetime import datetime
import locale


def parse_data():
    edge_options = Options()
    edge_options.add_argument("--headless")
    browser = webdriver.Edge()
    browser.implicitly_wait(10)
    current_page = 1

    browser.get("https://zakupki.okmot.kg/popp/view/order/list.xhtml")

    td_elements = browser.find_elements(By.XPATH, '//td[@role="gridcell"]/span[@class="nameTender"]')

    current_time = timezone.now()

    while len(td_elements) > 0 :
        for i in range(len(td_elements)):
            try:
                td_elements = browser.find_elements(By.XPATH, '//td[@role="gridcell"]/span[@class="nameTender"]')
                WebDriverWait(browser, 10).until(EC.visibility_of(td_elements[i]))
                browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", td_elements[i])
                time.sleep(1)
                try:
                    td_elements[i].click()

                    tender_num_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//div[@class="col-12 col-md-6" and position()=1]/span[@class="text"]'))
                    )
                    WebDriverWait(browser, 10).until(
                        lambda driver: len(tender_num_element.text.strip()) > 0
                    )
                    tender_num = int(tender_num_element.text.strip())
                    if TendersList.objects.filter(tenderNum=tender_num).exists():
                        browser.quit()
                        return

                    tender_name_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//div[@class="col-12 col-md-6" and position()=2]/span[@class="text"]'))
                    )
                    WebDriverWait(browser, 10).until(
                        lambda driver: len(tender_name_element.text.strip()) > 0
                    )
                    tender_name = tender_name_element.text.strip()

                    tender_format_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//div[@class="col-12 col-md-6" and position()=4]/span[@class="text"]'))
                    )
                    WebDriverWait(browser, 10).until(
                        lambda driver: len(tender_format_element.text.strip()) > 0
                    )
                    tender_format = tender_format_element.text.strip()

                    tender_summ_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//div[@class="col-12 col-md-6" and position()=6]/span[@class="text"]'))
                    )
                    WebDriverWait(browser, 10).until(
                        lambda driver: len(tender_summ_element.text.strip()) > 0
                    )
                    tender_summ_text = tender_summ_element.text.replace(" ", "")
                    if ',' in tender_summ_text:
                        tender_summ_text = tender_summ_text.split(',')[0]
                    tender_summ = int(tender_summ_text)

                    tender_srok_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//div[@class="col-12 col-md-6" and position()=9]/span[@class="text"]'))
                    )
                    WebDriverWait(browser, 10).until(
                        lambda driver: len(tender_srok_element.text.strip()) > 0
                    )
                    tender_srok = int(tender_srok_element.text.strip())

                    try:
                        letter_element = WebDriverWait(browser, 10).until(
                            EC.element_to_be_clickable(
                                (By.XPATH,
                                 '//div[@class="container-content"]/div[@class="row"]/'
                                 'div[@class="col-12 col-md-6"][position()=18]/span[@class="text"]/a'))
                        )
                        WebDriverWait(browser, 10).until(
                            lambda driver: len(letter_element.text.strip()) > 0
                        )
                        letter = letter_element.text.strip()
                        letter_url = letter_element.get_attribute("href")
                    except TimeoutException:
                        pass

                    locale.setlocale(locale.LC_TIME, 'ru_RU.utf8')

                    months_dict = {
                        'января': '01',
                        'февраля': '02',
                        'марта': '03',
                        'апреля': '04',
                        'мая': '05',
                        'июня': '06',
                        'июля': '07',
                        'августа': '08',
                        'сентября': '09',
                        'октября': '10',
                        'ноября': '11',
                        'декабря': '12',
                    }

                    tender_start_time_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//div[@class="col-12 col-md-6" and position()=7]/span[@class="text"]'))
                    )
                    WebDriverWait(browser, 10).until(
                        lambda driver: len(tender_start_time_element.text.strip()) > 0
                    )
                    tender_start_time_str = tender_start_time_element.text.strip()


                    for month_name, month_number in months_dict.items():
                        tender_start_time_str = tender_start_time_str.replace(month_name, month_number)
                    new_tender_start_time_str = tender_start_time_str[6:10]
                    new_tender_start_time_str += " " + tender_start_time_str[3:5]
                    new_tender_start_time_str += " " + tender_start_time_str[0:2]
                    new_tender_start_time_str += " "+ tender_start_time_str[11:13]
                    new_tender_start_time_str += " " +tender_start_time_str[14:16]
                    time_elements = new_tender_start_time_str.split()
                    new_tender_start_time_str = f"{time_elements[0]}-{time_elements[1]}-{time_elements[2]} {time_elements[3]}:{time_elements[4]}"

                    start_time = datetime.strptime(new_tender_start_time_str, '%Y-%m-%d %H:%M')
                    start_time = timezone.make_aware(start_time)

                    try:
                        tender_end_time_element = WebDriverWait(browser, 10).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '//div[@class="col-12 col-md-6" and position()=8]/span[@class="text"]'))
                        )
                        WebDriverWait(browser, 10).until(
                            lambda driver: len(tender_end_time_element.text.strip()) > 0
                        )
                        tender_end_time_str = tender_end_time_element.text.strip()

                        for month_name, month_number in months_dict.items():
                            tender_end_time_str = tender_end_time_str.replace(month_name, month_number)
                        new_tender_end_time_str = tender_end_time_str[6:10]
                        new_tender_end_time_str += " " + tender_end_time_str[3:5]
                        new_tender_end_time_str += " " + tender_end_time_str[0:2]
                        new_tender_end_time_str += " " + tender_end_time_str[11:13]
                        new_tender_end_time_str += " " + tender_end_time_str[14:16]
                        end_time_elements = new_tender_end_time_str.split()

                        new_tender_end_time_str = f"{end_time_elements[0]}-{end_time_elements[1]}-{end_time_elements[2]} {end_time_elements[3]}:{end_time_elements[4]}"

                        end_time = datetime.strptime(new_tender_end_time_str, '%Y-%m-%d %H:%M')
                        end_time = timezone.make_aware(end_time)

                        if end_time < current_time:
                            browser.quit()
                            return
                    except TimeoutException:
                        pass

                    organization_name_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//div[@class="col-12 col-md-6" and position()=3]/span[@class="text"]'))
                    )
                    WebDriverWait(browser, 10).until(
                        lambda driver: len(organization_name_element.text.strip()) > 0
                    )
                    organization_name = organization_name_element.text.strip()

                    organization_phone_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH,
                             '//div[@class="container-content"][position()=2]/div[@class="row"]/'
                             'div[@class="col-12 col-md-6"][position()=3]/span[@class="text"]'))
                    )
                    WebDriverWait(browser, 10).until(
                        lambda driver: len(organization_phone_element.text.strip()) > 0
                    )
                    organization_phone = organization_phone_element.text.strip()

                    organization_address_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH,
                             '//div[@class="container-content"][position()=2]/div[@class="row"]/'
                             'div[@class="col-12 col-md-6"][position()=2]/span[@class="text"]'))
                    )
                    WebDriverWait(browser, 10).until(
                        lambda driver: len(organization_address_element.text.strip()) > 0
                    )
                    organization_address = organization_address_element.text.strip()

                    lots = browser.find_elements(By.XPATH, '//div[@class="container-content"][position()=3]')
                    lot_info = []
                    for j in range(len(lots)):
                        lot_name_element = WebDriverWait(browser, 10).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, f'//tr[@data-ri="{j}"]/td[@role="gridcell"][position()=2]/span[@class="bold"]'))
                        )
                        WebDriverWait(browser, 10).until(
                            lambda driver: len(lot_name_element.text.strip()) > 0
                        )
                        lot_price_element = WebDriverWait(browser, 10).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, f'//tr[@data-ri="{j}"]/td[@role="gridcell"][position()=1]/span[@class="bold"]'))
                        )
                        WebDriverWait(browser, 10).until(
                            lambda driver: len(lot_price_element.text.strip()) > 0
                        )

                        lot_info.append(f'{lot_name_element.text.strip()} - {lot_price_element.text.strip()}')
                    lot_info_str = '\n'.join(lot_info)

                    info_url = browser.current_url

                    TendersList.objects.create(
                        tenderNum=tender_num,
                        tenderName=tender_name,
                        tenderFormat=tender_format,
                        tenderSumm=tender_summ,
                        srok=tender_srok,

                        organizationName=organization_name,
                        organizationPhone=organization_phone,
                        organizationAddress=organization_address,

                        dateTimeStart=start_time,
                        dateTimeEnd=end_time,
                        letterFile=letter_url,
                        letterName=letter,

                        lotsInfo=lot_info_str,

                        moreInfo=info_url
                    )
                except ElementClickInterceptedException:
                    pass
                time.sleep(0.1)
                browser.get(f"https://zakupki.okmot.kg/popp/view/order/list.xhtml?first={current_page * 10}")
            except StaleElementReferenceException:
                td_elements = browser.find_elements(By.XPATH, '//td[@role="gridcell"]/span[@class="nameTender"]')
                continue


        current_page += 1
        next_page_button = browser.find_element(By.XPATH, '//a[@class="ui-paginator-next ui-state-default ui-corner-all"]')
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//td[@role="gridcell"]/span[@class="nameTender"]'))
        )

        td_elements = browser.find_elements(By.XPATH, '//td[@role="gridcell"]/span[@class="nameTender"]')

        next_page_button.click()

    browser.quit()