import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


driver_path = os.getenv("DRIVER_PATH")
driver = webdriver.Chrome(driver_path)
browser = driver.get("http://localhost:5000/")

@pytest.fixture(scope='session', autouse=True)
def integration_tests():
    yield 
    driver.close()
    driver.quit()
    print("donedonedone")

def test_artists_link():
    table_type = "artists"
    _test_link(table_type)
    _test_link_click_result(table_type, 2)

def _test_link(table_type):
    link = driver.find_element_by_id(f"{table_type}Link")
    link.click()

def _test_link_click_result(table_type, num_of_columns):
    try:
        datatable = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located(
            (By.ID, f"{table_type}Table_wrapper")
            ))
    except Exception as e:
        assert datatable
    columns = driver.find_elements(By.XPATH, f"//table[@id=\"{table_type}Table\"]/thead/tr/th")
    assert len(columns) == num_of_columns

    driver.implicitly_wait(3)
    rows = driver.find_elements(By.XPATH, f"//table[@id=\"{table_type}Table\"]/tbody/tr")
    assert len(rows)

def test_artwork_link():
    table_type = "artwork"
    _test_link(table_type)
    _test_link_click_result(table_type, 4)

def test_neighbourhood_dropdown():
    neighbourhood = driver.find_element_by_id("neighbourhoodCollapseButton")
    neighbourhood.click()
    neighbourhoodCollapse= driver.find_element_by_id("neighbourhoodCollapse")
    assert neighbourhoodCollapse.is_displayed()

def test_neighbourhood_link():
    link = driver.find_element_by_xpath('//*[@id="neighbourhoodCollapse"]/ul/li/a[2]')
    link.click()
    _test_link_click_result("Downtown", 4)

def test_pagination():
    table_type = "artists"
    _test_link(table_type)
    page = driver.find_element_by_xpath(f"//*[@id=\"{table_type}Table_paginate\"]/ul/li[4]/a")
    page.click()
    driver.implicitly_wait(3)
    rows = driver.find_elements(By.XPATH, f"//table[@id=\"{table_type}Table\"]/tbody/tr")
    assert len(rows)

def test_search():
    table_type = "artists"
    _test_link(table_type)
    search = driver.find_element_by_xpath(f"//*[@id=\"{table_type}Table_filter\"]/label/input")
    search.send_keys("art")
    driver.implicitly_wait(3)
    rows = driver.find_elements(By.XPATH, f"//table[@id=\"{table_type}Table\"]/tbody/tr")
    assert len(rows)