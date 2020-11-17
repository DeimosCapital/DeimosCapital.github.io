import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pytrends.request import TrendReq
import time
from time import sleep
from datetime import datetime
from selenium.webdriver.support.select import Select
import pandas as pd
import pyautogui
import re
g_trends_fetches_since_start = 0
lastG_trends_fetch_time = 0
startTime = time.time()


#region Setting WebDriver options
#Setting chrome driver options
pytrend = TrendReq(hl='en-US', tz=360,retries=10, backoff_factor=0.5)
DRIVER_PATH = 'chromedriver.exe'
chrome_options = Options()
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver.exe")
# chrome_options.headless = True
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920x1080")
# chrome_options.add_argument("--disable-notifications")
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_experimental_option("prefs", {
#         "download.default_directory": "C:\\Users\\Pierce\\Desktop\\deimoscapital_github_site\\DeimosCapital.github.io\\temp_data",
#         "download.prompt_for_download": False,
#         "download.directory_upgrade": True,
#         "safebrowsing_for_trusted_sources_enabled": False,
#         "safebrowsing.enabled": False
# })
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--disable-software-rasterizer')

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver.exe")
download_dir = "C:\\Users\\Pierce\\Desktop\\deimoscapital_github_site\\DeimosCapital.github.io\\temp_data"
g_trends_keywords = ["BTC", "ETH", "Bitcoin", "Cryptocurrency", "blockchain", "ethereum"]
network_traffick_links_BTC =[("https://coinmetrics.io/charts/#assets=btc_left=BlkSizeByte_zoom=1279411200000,1605484800000", "blk_size_bytes", "bytes"), ("https://coinmetrics.io/charts/#assets=btc_left=HashRate_zoom=1279411200000,1605484800000", "hash_rate", "TH/s"), ("https://coinmetrics.io/charts/#assets=btc_left=NVTAdj_zoom=1279411200000,1605484800000", "NVT", "units"), ("https://coinmetrics.io/charts/#assets=btc_left=NVTAdj90_zoom=1231632000000,1605484800000","NVTadj90MA", "units"), ("https://coinmetrics.io/charts/#assets=btc_left=AdrActCnt", "Active Addresses", "active addresses"), ("https://coinmetrics.io/charts/#assets=btc_left=DiffMean_zoom=1230940800000,1605484800000", "Mean difficulty", "T")]
network_traffick_links_ETH =[("https://coinmetrics.io/charts/#assets=eth_left=BlkSizeByte_zoom=1230940800000,1605484800000", "blk_size_bytes", "bytes"), ("https://coinmetrics.io/charts/#assets=eth_left=HashRate_zoom=1230940800000,1605484800000", "hash_rate", "TH/s"), ("https://coinmetrics.io/charts/#assets=eth_left=NVTAdj_zoom=1230940800000,1605484800000", "NVT", "units"), ("https://coinmetrics.io/charts/#assets=eth_left=NVTAdj90_zoom=1230940800000,1605484800000","NVTadj90MA", "units"), ("https://coinmetrics.io/charts/#assets=eth_left=AdrActCnt_zoom=1230940800000,1605484800000", "Active Addresses", "active addresses"), ("https://coinmetrics.io/charts/#assets=eth_left=DiffMean_zoom=1230940800000,1605484800000", "Mean difficulty", "T")]
#network_traffick_links_BTC =[("https://coinmetrics.io/charts/#assets=btc_left=BlkSizeByte_zoom=1279411200000,1605484800000", "blk_size_bytes", "bytes")]
#endregion


def NumericFilter(string_to_filter):
    numeric_string = re.sub(r'[^\d.]+', '', string_to_filter)
    return numeric_string

def GetGoogleTrendsData(driver, g_trends_fetches_since_start):
    import time
    from time import sleep
    google_trends_url = 'https://trends.google.com/trends/?geo=US'
    g_trends_keywords = ["BTC", "ETH", "Bitcoin", "Cryptocurrency", "blockchain", "ethereum"]
    slopeaverages = []
    #get daily search trends index
    for kw in g_trends_keywords:
        driver.get(google_trends_url)
        kw_input = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/ng-include/div/div[2]/autocomplete/md-autocomplete/md-autocomplete-wrap/input')
        if kw_input != None:
            kw_input.click()
        kw_input.send_keys(kw)
        kw_input.send_keys("\n")
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/header/div/div[3]/ng-transclude/div[2]/div/div/custom-date-picker/ng-include/md-select/md-select-value').click()
        setOptionElement = driver.find_element_by_css_selector('md-option[id="select_option_16"]')
        setOptionElement.click()
        time.sleep(2)
        button = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/md-content/div/div/div[1]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]')
        button.click()
        with open(r"C:\Users\Pierce\Desktop\deimoscapital_github_site\DeimosCapital.github.io\temp_data\multiTimeline.csv") as readfile:
            rf = readfile.read()
            rf_split = rf.split("\n")
            rf_split_refined = rf_split[3:]
            rf_split_refined = rf_split_refined[0:len(rf_split_refined)-2]
            datapoints = []
            for line in rf_split_refined:
                # print(line)
                splitline = line.split(",")
                poi = int(splitline[1])
                datapoints.append(poi)
            
            slopes = []
            count = 0

            for point in datapoints:
                if count < len(datapoints)-1:
                    difference = (datapoints[count+1] - point)/2
                    slopes.append(difference)
                    count = count+1
            slopesum = 0
            for slope in slopes:
                slopesum = slopesum + slope
            
            slopeaverage = slopesum/len(slopes)
            slopeaverages.append(slopeaverage)
            # print("Daily change in " + kw + " slope average = " + str(slopeaverage))
            readfile.close()
        
    slopeavsum = 0
    for slopeav in slopeaverages:
        slopeavsum = slopeavsum + slopeav

    slopeav_av = slopeavsum/len(slopeaverages)

    now = datetime.now() # current date and time

    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    clock_time = now.strftime("%H:%M:%S")
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    print("Total Search Trend Index (Daily) = " + str(slopeav_av))
    with open("search_trends_daily.csv", "a+") as writefile:
        writefile.write(date_time + ", " + str(slopeav_av))
        writefile.close()

    #get hourly search trends index
    for kw in g_trends_keywords:
        driver.get(google_trends_url)
        kw_input = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/ng-include/div/div[2]/autocomplete/md-autocomplete/md-autocomplete-wrap/input')
        if kw_input != None:
            kw_input.click()
        kw_input.send_keys(kw)
        kw_input.send_keys("\n")
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/header/div/div[3]/ng-transclude/div[2]/div/div/custom-date-picker/ng-include/md-select/md-select-value').click()
        setOptionElement = driver.find_element_by_css_selector('md-option[id="select_option_14"]')
        setOptionElement.click()
        button = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/md-content/div/div/div[1]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]')
        button.click()
        time.sleep(2)
        with open(r"C:\Users\Pierce\Desktop\deimoscapital_github_site\DeimosCapital.github.io\temp_data\multiTimeline.csv") as readfile:
            rf = readfile.read()
            rf_split = rf.split("\n")
            rf_split_refined = rf_split[3:]
            rf_split_refined = rf_split_refined[0:len(rf_split_refined)-2]
            datapoints = []
            for line in rf_split_refined:
                # print(line)
                splitline = line.split(",")
                poi = int(splitline[1])
                datapoints.append(poi)
            
            slopes = []
            count = 0

            for point in datapoints:
                if count < len(datapoints)-1:
                    difference = (datapoints[count+1] - point)/2
                    slopes.append(difference)
                    count = count+1
            slopesum = 0
            for slope in slopes:
                slopesum = slopesum + slope
            
            slopeaverage = slopesum/len(slopes)
            slopeaverages.append(slopeaverage)
            # print("Daily change in " + kw + " slope average = " + str(slopeaverage))
            readfile.close()
        
    slopeavsum = 0
    for slopeav in slopeaverages:
        slopeavsum = slopeavsum + slopeav

    slopeav_av = slopeavsum/len(slopeaverages)

    now = datetime.now() # current date and time

    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    clock_time = now.strftime("%H:%M:%S")
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    print("Total Search Trend Index (Hourly) = " + str(slopeav_av))
    with open("search_trends_hourly.csv", "a+") as writefile:
        writefile.write(date_time + ", " + str(slopeav_av))
        writefile.close()
    g_trends_fetches_since_start = g_trends_fetches_since_start + 1




def GetCryptoNetworkTrafficData(driver, network_traffick_links_BTC,network_traffick_links_ETH):
    now = datetime.now()
    timestamp = now.strftime("%m/%d/%Y, %H:%M:%S")
    timestamp_data = timestamp.split(",")
    btc_network_data = [timestamp_data[0], timestamp_data[1]]
    for link in network_traffick_links_BTC:
        driver.get(link[0])
        driver.maximize_window()
        action = webdriver.common.action_chains.ActionChains(driver)
        time.sleep(2)
        chart_div_xpath = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/article/div/div/div[3]/div/div/div/div/div/div[1]/div[3]/div[1]/div')
        chart_ytd_button_xpath = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/article/div/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[2]/div[4]')
        chart_dygraph_legend_xpath = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/article/div/div/div[3]/div/div/div/div/div/div[1]/div[3]/div[1]/div/div[20]')
        action.move_to_element_with_offset(chart_ytd_button_xpath, 0, 0)
        action.click()
        action.perform()
        time.sleep(1)
        pyautogui.moveTo(x=1000, y=582)
        time.sleep(0.1)
        pyautogui.moveTo(x=1546, y=582)
        time.sleep(1)
        chart_dygraph_legend = driver.find_element_by_class_name('dygraph-legend')
        underlying_spans = chart_dygraph_legend.find_elements_by_tag_name("span")
        if len(underlying_spans) > 0:
            string_data = underlying_spans[0].text
            string_data_filtered = NumericFilter(string_data)
            print(link[1] + " found: " + str(string_data_filtered) + " " + link[2])
            btc_network_data.append(string_data_filtered)

    timestamp = now.strftime("%m/%d/%Y, %H:%M:%S")
    timestamp_data = timestamp.split(",")
    eth_network_data = [timestamp_data[0], timestamp_data[1]]
    for link in network_traffick_links_ETH:
        driver.get(link[0])
        driver.maximize_window()
        action = webdriver.common.action_chains.ActionChains(driver)
        time.sleep(2)
        chart_div_xpath = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/article/div/div/div[3]/div/div/div/div/div/div[1]/div[3]/div[1]/div')
        chart_ytd_button_xpath = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/article/div/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[2]/div[4]')
        chart_dygraph_legend_xpath = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/article/div/div/div[3]/div/div/div/div/div/div[1]/div[3]/div[1]/div/div[20]')
        action.move_to_element_with_offset(chart_ytd_button_xpath, 0, 0)
        action.click()
        action.perform()
        time.sleep(1)
        pyautogui.moveTo(x=1000, y=582)
        time.sleep(0.1)
        pyautogui.moveTo(x=1546, y=582)
        time.sleep(1)
        chart_dygraph_legend = driver.find_element_by_class_name('dygraph-legend')
        underlying_spans = chart_dygraph_legend.find_elements_by_tag_name("span")
        if len(underlying_spans) > 0:
            string_data = underlying_spans[0].text
            string_data_filtered = NumericFilter(string_data)
            print(link[1] + " found: " + str(string_data_filtered) + " " + link[2])
            eth_network_data.append(string_data_filtered)
    
    return_data = [btc_network_data, eth_network_data]
    return return_data




def ExecuteDataFetching():

    #update network data
    current_timestamp_network_data = GetCryptoNetworkTrafficData(driver, network_traffick_links_BTC, network_traffick_links_ETH)
    stringconcatbtc = ""
    for point in current_timestamp_network_data[0]:
        stringconcatbtc = stringconcatbtc + point + ","
    stringconcatbtc = stringconcatbtc[:-1]

    stringconcateth = ""
    for point in current_timestamp_network_data[1]:
        stringconcateth = stringconcateth + point + ","
    stringconcateth = stringconcateth[:-1]

    with open("btc_network_data.csv", "a+") as writefile:
        writefile.write("\n" + stringconcatbtc)
        writefile.close()

    with open("eth_network_data.csv", "a+") as writefile:
        writefile.write("\n" + stringconcateth)
        writefile.close()
    
    #update gtrends data
    GetGoogleTrendsData(driver, g_trends_fetches_since_start)

    #update price data
