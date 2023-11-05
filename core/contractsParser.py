import re

from bs4 import BeautifulSoup
from django.utils import timezone
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, \
    ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from .models import TendersList, ContractsList
from datetime import datetime, date
import locale


def parse_data2():
    edge_options = Options()
    edge_options.add_argument("--headless")
    browser = webdriver.Edge()
    browser.implicitly_wait(10)
    current_page = 1

    browser.get("http://zakupki.gov.kg/popp/view/order/winners.xhtml")

    td_elements = browser.find_elements(By.XPATH, '//*[@id="table_data"]/tr[@role="row"]')

    while len(td_elements) > 0:
        for i in range(len(td_elements)):
            try:
                td_elements = browser.find_elements(By.XPATH, '//*[@id="table_data"]/tr[@role="row"]')
                WebDriverWait(browser, 10).until(EC.visibility_of(td_elements[i]))
                browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", td_elements[i])
                time.sleep(1)
                try:
                    tender_num_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, f'/html/body/div[3]/div/div[2]/form/div/div[1]/table/tbody/tr[{i+1}]/td[2]'))
                    )

                    tender_num_html = tender_num_element.get_attribute("outerHTML")
                    soup = BeautifulSoup(tender_num_html, 'html.parser')
                    tender_num = int(''.join(soup.find('td').find_all(text=True, recursive=False)).strip())

                    tender_name_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, f'/html/body/div[3]/div/div[2]/form/div/div[1]/table/tbody/tr[{i+1}]/td[3]'))
                    )
                    tender_name_html = tender_name_element.get_attribute("outerHTML")
                    soup = BeautifulSoup(tender_name_html, 'html.parser')
                    tender_name = ''.join(soup.find('td').find_all(text=True, recursive=False)).strip()

                    winner_name_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, f'/html/body/div[3]/div/div[2]/form/div/div[1]/table/tbody/tr[{i+1}]/td[4]'))
                    )
                    winner_name_html = winner_name_element.get_attribute("outerHTML")
                    soup = BeautifulSoup(winner_name_html, 'html.parser')
                    winner_name = ''.join(soup.find('td').find_all(text=True, recursive=False)).strip()

                    date_contract_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, f'/html/body/div[3]/div/div[2]/form/div/div[1]/table/tbody/tr[{i+1}]/td[10]'))
                    )

                    date_contract_html = date_contract_element.get_attribute("outerHTML")
                    soup = BeautifulSoup(date_contract_html, 'html.parser')
                    date_contract_str = ''.join(soup.find('td').find_all(text=True, recursive=False)).strip()
                    date_contract = datetime.strptime(date_contract_str, '%Y-%m-%d').date()

                    contract_num_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, f'/html/body/div[3]/div/div[2]/form/div/div[1]/table/tbody/tr[{i+1}]/td[9]'))
                    )
                    contract_num_html = contract_num_element.get_attribute("outerHTML")
                    soup = BeautifulSoup(contract_num_html, 'html.parser')
                    contract_num = ''.join(soup.find('td').find_all(text=True, recursive=False)).strip()

                    lots_info_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, f'/html/body/div[3]/div/div[2]/form/div/div[1]/table/tbody/tr[{i+1}]/td[5]'))
                    )
                    lots_info_html = lots_info_element.get_attribute("outerHTML")
                    soup = BeautifulSoup(lots_info_html, 'html.parser')
                    lots_info = ''.join(soup.find('td').find_all(text=True, recursive=False)).strip()

                    prices_on_tender_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, f'/html/body/div[3]/div/div[2]/form/div/div[1]/table/tbody/tr[{i+1}]/td[7]'))
                    )
                    prices_on_tender_html = prices_on_tender_element.get_attribute("outerHTML")
                    soup = BeautifulSoup(prices_on_tender_html, 'html.parser')

                    prices_on_tender = ''.join(soup.find('td').find_all(text=True, recursive=False)).strip()

                    prices_on_contract_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, f'/html/body/div[3]/div/div[2]/form/div/div[1]/table/tbody/tr[{i+1}]/td[8]'))
                    )

                    prices_on_contract_html = prices_on_contract_element.get_attribute("outerHTML")
                    soup = BeautifulSoup(prices_on_contract_html, 'html.parser')
                    prices_on_contract = ''.join(soup.find('td').find_all(text=True, recursive=False)).strip()

                    # Преобразуем строку с цифрами в число
                    # prices_on_contract = prices_on_contract_str

                    # Теперь можешь использовать переменную prices_on_contract
                    print(prices_on_contract)


                    if ContractsList.objects.filter(lotsInfo=lots_info).exists() and ContractsList.objects.filter(tenderNum=tender_num).exists():
                        browser.quit()
                        return

                    ContractsList.objects.create(
                        tenderNum=tender_num,
                        tenderName=tender_name,

                        winnerName=winner_name,

                        dateContract=date_contract,
                        contractNum=contract_num,

                        lotsInfo=lots_info,
                        pricesOnTender=prices_on_tender,
                        pricesOnContract=prices_on_contract,
                    )
                except ElementClickInterceptedException:
                    pass
                time.sleep(0.1)
                browser.get(f"http://zakupki.gov.kg/popp/view/order/winners.xhtml?first={current_page * 10}")
                i = 0
            except StaleElementReferenceException:
                td_elements = browser.find_elements(By.XPATH, '//*[@id="table_data"]/tr[@role="row"]')
                continue

        current_page += 1
        next_page_button = browser.find_element(By.XPATH,
                                                '/html/body/div[3]/div/div[2]/form/div/div[2]/a[3]')
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="table_data"]/tr[@role="row"]'))
        )

        td_elements = browser.find_elements(By.XPATH, '//*[@id="table_data"]/tr[@role="row"]')

        next_page_button.click()

    browser.quit()
