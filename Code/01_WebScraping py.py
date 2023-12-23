# ==============================================================================
# Autor(es): Juan Felipe Agudelo Rios                                         |                                                             |
# Fecha creación: 10/09/2022                                                  |
# Fecha última modificación: 14/09/2022                                       |
# ==============================================================================

"""
Description:
This script performs web scraping of star data, downloads and processes the data, and then merges it into a single DataFrame.
The code includes error handling for timeouts and missing elements during the scraping process.
The resulting DataFrame is saved as a pickle file for further analysis.
"""

import glob
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import random
from distutils.core import setup

df=pd.read_csv("C:/Users/j.agudelo/OneDrive - Universidad de los Andes/scientificProject1/data/DF_Links.csv")
def generara_url(df):
    ra = str(df["ra"])
    dec = str(df["D"])
    url_base = "http://ned.ipac.caltech.edu/extinction_calculator?in_csys=Equatorial&in_equinox=J2000.0&obs_epoch=2000.0&ra=%CAMPOOBJETIVORA%&dec=%CAMPOOBJETIVODEC%"
    url_base = url_base.replace("%CAMPOOBJETIVORA%", ra)
    url_base = url_base.replace("%CAMPOOBJETIVODEC%", dec)
    url_transformada = url_base
    return url_transformada

df["URL_objetivo"] = df.apply(generara_url,axis=1)

def op1():
    links=list(df["URL_objetivo"])
    links_done = []
    options = webdriver.ChromeOptions()
    #options.add_argument('--no-sandbox')
    #options.add_argument('--headless')
    #prefs = {"download.default_directory": "C:/Users/j.agudelo/OneDrive - Universidad de los Andes/scientificProject1/models/"}
    #options.add_experimental_option("prefs", prefs)
    Chrome_driver_binary = "C:/Users/j.agudelo/OneDrive - Universidad de los Andes/scientificProject1/data/chromedriver.exe"
    driver = webdriver.Chrome(Chrome_driver_binary, options=options)
    for link in links:
        try:
            RA_DEC=link.split("&")

            DEC=RA_DEC[-1]
            RA=RA_DEC[-2]

            DEC = [i for i in DEC if i.isdigit() or i == "."]
            DEC=''.join([str(elem) for elem in DEC])

            RA=[i for i in RA if i.isdigit() or i == "."]
            RA = ''.join([str(elem) for elem in RA])

            driver.set_page_load_timeout(random.randint(50, 60))
            driver.get(link)
            time.sleep(random.randint(10,15))
            boton_descarga = driver.find_element(By.XPATH,
                                                 "/html/body/div[1]/div[2]/section/form/div/div/div[1]/div/div/div/div/div[1]/div[3]/div[3]")
            boton_descarga.click()
            time.sleep(random.randint(3, 5))
            Nombre_archivo=driver.find_element(By.XPATH,
                                               '//*[@id="dialogRootDiv"]/div/div/div[1]/div/div/div[2]/div/div[1]/div/div[2]/input')
           
            time.sleep(random.randint(3, 5))

            Nombre_archivo.send_keys(f"_RA{RA}_DEC{DEC}")

            time.sleep(random.randint(4, 5))

            boton_save = driver.find_element(By.XPATH,
                                             "/html/body/div[3]/div/div/div[1]/div/div/div[2]/div/div[2]/div[1]/div[1]/div/button")
            boton_save.click()
            time.sleep(random.randint(1, 2))
            links_done.append(link)

        except TimeoutException as ex:
            isrunning = 0
            print("Exception has been thrown. " + str(ex))
        except NoSuchElementException:
            print("NO SE ENCONTRO LA TABLA ")
        
    return  links_done

links_done=op1()


def merge():
    main_df = pd.DataFrame()
    archivos = glob.glob("C:/Users/j.agudelo/OneDrive - Universidad de los Andes/scientificProject1/models/*.tbl")
    for archivo in archivos:
        df = pd.read_table(
            archivo,
            comment='\\', delim_whitespace=True, skiprows=11)
        df.columns.values
        df["Bandpass"] = df["|"] + df["|.1"]
        df = df.drop(["|", "|.1"], axis=1)
        df.dropna()
        df.columns = ["Um", "Mag", "Refcode", "Bandpass"]
        df.set_index("Bandpass")
        RA_DEC = archivo.split("_")
        DEC = RA_DEC[-1]
        RA = RA_DEC[-2]
        DEC = [i for i in DEC if i.isdigit() or i == "."]
        DEC = ''.join([str(elem) for elem in DEC])
        RA = [i for i in RA if i.isdigit() or i == "."]
        RA = ''.join([str(elem) for elem in RA])
        df["RA"]=[RA for i in range(len(list(df["Um"])))]
        df["DEC"] = [DEC for i in range(len(list(df["Um"])))]

        main_df = pd.concat([main_df, df])
        print("DONE")
    return main_df



main_df=merge()

def quitar_elpunto(i):
    i=str(i)
    i=i[:-1]
    return i 

main_df["DEC"]=main_df["DEC"].apply(quitar_elpunto)

main_df.to_pickle("C:/Users/j.agudelo/OneDrive - Universidad de los Andes/scientificProject1/DataFrameRafael.pkl")


print("DONE")
